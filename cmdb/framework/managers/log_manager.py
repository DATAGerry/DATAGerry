# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
Manager of logs
"""
from typing import Union, List
from datetime import datetime, timezone

from cmdb.framework import CmdbLog, CmdbMetaLog
from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.manager.managers import ManagerQueryBuilder, ManagerBase
from cmdb.framework.utils import PublicID

from cmdb.framework.results.iteration import IterationResult
from cmdb.manager import ManagerGetError, ManagerIterationError, ManagerDeleteError, ManagerInsertError, \
    ManagerUpdateError
from cmdb.framework.models.log import LOGGER, LogAction, CmdbObjectLog
from cmdb.search import Query, Pipeline
from cmdb.security.acl.builder import LookedAccessControlQueryBuilder
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel
from cmdb.utils.error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #
#                                                LogQueryBuilder - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #

class LogQueryBuilder(ManagerQueryBuilder):
    """TODO: document"""
    def __init__(self):
        super().__init__()


    def build(self, filter: Union[List[dict], dict], limit: int, skip: int, sort: str, order: int,
              user: UserModel = None, permission: AccessControlPermission = None, *args, **kwargs) -> \
            Union[Query, Pipeline]:
        """
        Converts the parameters from the call to a mongodb aggregation pipeline
        Args:
            filter: dict or list of dict query/queries which the elements have to match.
            limit: max number of documents to return.
            skip: number of documents to skip first.
            sort: sort field
            order: sort order
            user: request user
            permission: AccessControlPermission
            *args:
            **kwargs:

        Returns:
            The `LogQueryBuilder` query pipeline with the parameter contents.
        """
        self.clear()
        self.query = Pipeline([])

        if isinstance(filter, dict):
            self.query.append(self.match_(filter))
        elif isinstance(filter, list):
            for pipe in filter:
                self.query.append(pipe)

        if user and permission:
            self.query += (LookedAccessControlQueryBuilder().build(group_id=PublicID(user.group_id), permission=permission))

        if limit == 0:
            results_query = [self.skip_(limit)]
        else:
            results_query = [self.skip_(skip), self.limit_(limit)]

        self.query.append(self.sort_(sort=sort, order=order))
        self.query += results_query

        return self.query


    def count(self, filter: Union[List[dict], dict], user: UserModel = None,
              permission: AccessControlPermission = None) -> Union[Query, Pipeline]:
        """
        Count the number of documents in the stages
        Args:
            filter: filter requirement
            user: request user
            permission: acl permission

        Returns:
            Query with count stages.
        """
        self.clear()
        self.query = Pipeline([])

        if isinstance(filter, dict):
            self.query.append(self.match_(filter))
        elif isinstance(filter, list):
            for pipe in filter:
                self.query.append(pipe)

        if user and permission:
            self.query += (LookedAccessControlQueryBuilder().build(group_id=PublicID(user.group_id), permission=permission))

        self.query.append(self.count_('total'))

        return self.query

# -------------------------------------------------------------------------------------------------------------------- #
#                                                CmdbLogManager - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #

class CmdbLogManager(ManagerBase):
    """
    Manager for the CmdbLog module. Manages the CRUD functions of the logs and the iteration over the collection.
    """

    def __init__(self, database_manager: DatabaseManagerMongo):
        """
        Constructor of `CmdbLogManager`

        Args:
            database_manager: Connection to the database class.
        """
        self.log_builder = LogQueryBuilder()
        super().__init__(CmdbMetaLog.COLLECTION, database_manager=database_manager)


    def get(self, public_id: Union[PublicID, int]) -> Union[CmdbMetaLog, CmdbObjectLog]:
        cursor_result = self._get(self.collection, filter={'public_id': public_id}, limit=1)
        for resource_result in cursor_result.limit(-1):
            return CmdbLog.from_data(resource_result)

        raise ManagerGetError(f'Log with ID: {public_id} not found!')


    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int,
                user: UserModel = None, permission: AccessControlPermission = None, *args, **kwargs):
        """
        Iterate over a collection of object logs resources.

        Args:
            filter: match requirements of field values
            limit: max number of elements to return
            skip: number of elements to skip first
            sort: sort field
            order: sort order

        Returns:
            IterationResult: Instance of IterationResult with generic CmdbObjectLog.
        """
        try:
            query: Query = self.log_builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order,
                                                  user=user, permission=permission)
            count_query: Pipeline = self.log_builder.count(filter=filter, user=user, permission=permission)
            aggregation_result = list(self._aggregate(self.collection, query))
            total_cursor = self._aggregate(self.collection, count_query)
            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']
        except ManagerGetError as err:
            raise ManagerIterationError(err) from err

        try:
            iteration_result: IterationResult[CmdbMetaLog] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbObjectLog)
        except ManagerGetError as err:
            raise ManagerGetError(err) from err
        return iteration_result


    def insert(self, action: LogAction, log_type: str, *args, **kwargs) -> int:
        """TODO: document"""
        # Get possible public id
        log_init = {}
        available_id = self._database_manager.get_next_public_id(collection=CmdbMetaLog.COLLECTION)
        log_init['public_id'] = available_id

        # set static values
        log_init['action'] = action.value
        log_init['action_name'] = action.name
        log_init['log_type'] = log_type
        log_init['log_time'] = datetime.now(timezone.utc)
        log_data = {**log_init, **kwargs}

        try:
            new_log = CmdbLog(**log_data)
            ack = self._insert(CmdbMetaLog.COLLECTION, new_log) #new_log.to_database(), but it is error
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise LogManagerInsertError(err) from err
        return ack


    def update(self, data) -> int:
        raise NotImplementedError


    def delete(self, public_id: Union[PublicID, int]) -> Union[CmdbMetaLog, CmdbObjectLog]:
        """
        Delete a existing log by its PublicID.

        Args:
            public_id (int): PublicID of the log in the system.

        Returns:
            CmdbMetaLog: The deleted log as its model.
        """
        raw_log: Union[CmdbMetaLog, CmdbObjectLog] = self.get(public_id=public_id)
        delete_result = self._delete(self.collection, filter={'public_id': public_id})
        if delete_result.deleted_count == 0:
            raise ManagerDeleteError(err='No log matched this public id')
        return raw_log


class LogManagerGetError(ManagerGetError):
    """TODO:document"""
    def __init__(self, err):
        super(LogManagerGetError, self).__init__(err)


class LogManagerInsertError(ManagerInsertError):
    """TODO:document"""
    def __init__(self, err):
        super(LogManagerInsertError, self).__init__(err)


class LogManagerUpdateError(ManagerUpdateError):
    """TODO:document"""
    def __init__(self, err):
        super(LogManagerUpdateError, self).__init__(err)


class LogManagerDeleteError(ManagerDeleteError):
    """TODO:document"""
    def __init__(self, err):
        super(LogManagerDeleteError, self).__init__(err)
