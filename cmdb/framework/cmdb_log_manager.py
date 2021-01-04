# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from datetime import datetime

from cmdb.framework import CmdbLog, CmdbMetaLog
from cmdb.database.managers import DatabaseManagerMongo
from cmdb.framework.managers.framework_manager import FrameworkManager

from cmdb.framework.results.iteration import IterationResult
from cmdb.manager import ManagerGetError, ManagerIterationError, ManagerDeleteError, ManagerInsertError, ManagerUpdateError
from cmdb.framework.cmdb_log import CMDBError, LOGGER, LogAction
from cmdb.search import Query


class CmdbLogManager(FrameworkManager):
    """
        Manager for the CmdbLog module. Manages the CRUD functions of the logs and the iteration over the collection.
        """

    def __init__(self, database_manager: DatabaseManagerMongo):
        """
        Constructor of `CmdbLogManager`

        Args:
            database_manager: Connection to the database class.
        """
        self.dbm = database_manager
        super(CmdbLogManager, self).__init__(CmdbMetaLog.COLLECTION, database_manager=database_manager)

    # CRUD functions
    def get_log(self, public_id: int):
        cursor_result = self._get(self.collection, filter={'public_id': public_id}, limit=1)
        for resource_result in cursor_result.limit(-1):
            return CmdbMetaLog.from_data(resource_result)
        raise ManagerGetError(f'Type with ID: {public_id} not found!')

    def get_logs(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs):
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
            query: Query = self.builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order)
            aggregation_result = next(self._aggregate(self.collection, query))
        except ManagerGetError as err:
            raise ManagerIterationError(err=err)

        try:
            iteration_result: IterationResult[CmdbMetaLog] = IterationResult.from_aggregation(aggregation_result)
            iteration_result.convert_to(CmdbMetaLog)
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ManagerGetError(err)
        return iteration_result

    def insert_log(self, action: LogAction, log_type: str, **kwargs) -> int:
        # Get possible public id
        log_init = {}
        available_id = self.dbm.get_next_public_id(collection=CmdbMetaLog.COLLECTION)
        log_init['public_id'] = available_id

        # set static values
        log_init['action'] = action.value
        log_init['action_name'] = action.name
        log_init['log_type'] = log_type
        log_init['log_time'] = datetime.utcnow()

        log_data = {**log_init, **kwargs}

        try:
            new_log = CmdbLog(**log_data)
            ack = self._insert(CmdbMetaLog.COLLECTION, new_log.to_database())
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise LogManagerInsertError(err)
        return ack

    def update_log(self, data) -> int:
        raise NotImplementedError

    def delete_log(self, public_id):
        try:
            ack = self._delete(CmdbMetaLog.COLLECTION, public_id)
        except CMDBError as err:
            LOGGER.error(err)
            raise ManagerDeleteError(err)
        return ack


class LogManagerGetError(ManagerGetError):

    def __init__(self, err):
        super(LogManagerGetError, self).__init__(err)


class LogManagerInsertError(ManagerInsertError):

    def __init__(self, err):
        super(LogManagerInsertError, self).__init__(err)


class LogManagerUpdateError(ManagerUpdateError):

    def __init__(self, err):
        super(LogManagerUpdateError, self).__init__(err)


class LogManagerDeleteError(ManagerDeleteError):

    def __init__(self, err):
        super(LogManagerDeleteError, self).__init__(err)
