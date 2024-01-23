# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
This module contains the implementation of LocationQueryBuilder and
LocationManager which are responsible to interact with the Database 
regarding locations.
"""
import json
import logging

from queue import Queue
from typing import Union, List
from bson import json_util

from cmdb.database.utils import object_hook
from cmdb.event_management.event import Event
from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.framework import CmdbLocation
from cmdb.framework.cmdb_object_manager import verify_access
from cmdb.security.acl.errors import AccessDeniedError
from cmdb.manager.managers import ManagerQueryBuilder, ManagerBase
from cmdb.framework.managers.type_manager import TypeManager
from cmdb.framework.results import IterationResult
from cmdb.framework.utils import PublicID
from cmdb.manager import ManagerGetError, ManagerIterationError, ManagerUpdateError
from cmdb.search import Query, Pipeline
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.security.acl.builder import AccessControlQueryBuilder
from cmdb.user_management import UserModel
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

class LocationQueryBuilder(ManagerQueryBuilder):
    """
    The LocationQueryBuilder builds queries for locations
    """

    def build(self, filter: Union[List[dict], dict], limit: int, skip: int, sort: str, order: int,
              user: UserModel, permission: AccessControlPermission, *args, **kwargs) -> Union[Query, Pipeline]:
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

        Returns:
            The LocationQueryBuilder query pipeline with the parameter contents.
        """
        self.clear()
        self.query = Pipeline([])

        if isinstance(filter, dict):
            self.query.append(self.match_(filter))
        elif isinstance(filter, list):
            for pipe in filter:
                self.query.append(pipe)

        self.query.append(self.sort_(sort=sort, order=order))

        #if user and permission:
        #    self.query += (AccessControlQueryBuilder().build(group_id=PublicID(user.group_id), permission=permission))

        if limit == 0:
            results_query = [self.skip_(limit)]
        else:
            results_query = [self.skip_(skip), self.limit_(limit)]
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

        #if user and permission:
        #    self.query += (AccessControlQueryBuilder().build(group_id=PublicID(user.group_id), permission=permission))

        self.query.append(self.count_('total'))
        return self.query

# -------------------------------------------------------------------------------------------------------------------- #
#                                                LocationManager - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #

class LocationManager(ManagerBase):
    """
    The Locationmanager interacts between API functions and database
    """

    def __init__(self, database_manager: DatabaseManagerMongo, event_queue: Union[Queue, Event] = None):
        """
        Set the database connection and the queue for sending events.

        Args:
            database_manager (DatabaseManagerMongo): Active database managers instance.
            event_queue (Queue, Event): The queue for sending events or the created event to send
        """
        self.event_queue = event_queue
        self.location_builder = LocationQueryBuilder()
        self.type_manager = TypeManager(database_manager)
        super().__init__(CmdbLocation.COLLECTION, database_manager=database_manager)


    def get(self, public_id: Union[PublicID, int], user: UserModel = None,
            permission: AccessControlPermission = None) -> CmdbLocation:
        """
        Get a single location by its id.

        Args:
            public_id (int): ID of the object.

        Returns:
            CmdbObject: Instance of CmdbObject with data.
        """
        cursor_result = self._get(self.collection, filter={'public_id': public_id}, limit=1)
        for resource_result in cursor_result.limit(-1):
            resource = CmdbLocation.from_data(resource_result)
            ## consider that the type of root location is -1
            type_ = TypeManager(database_manager=self._database_manager).get(resource.type_id)
            verify_access(type_, user, permission)
            return resource


    def iterate(self, filter: Union[List[dict], dict], limit: int, skip: int, sort: str, order: int,
                user: UserModel = None, permission: AccessControlPermission = None, *args, **kwargs) \
            -> IterationResult[CmdbLocation]:
        """
        TODO: description for iterate
        """

        try:
            query: Pipeline = self.location_builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order,
                                                        user=user, permission=permission)
            count_query: Pipeline = self.location_builder.count(filter=filter)
            aggregation_result = list(self._aggregate(self.collection, query))
            total_cursor = self._aggregate(self.collection, count_query)
            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']
        except ManagerGetError as err:
            raise ManagerIterationError(err=err) from err

        iteration_result: IterationResult[CmdbLocation] = IterationResult(aggregation_result, total)
        iteration_result.convert_to(CmdbLocation)
        return iteration_result


    def update(self, public_id: Union[PublicID, int], data: Union[CmdbLocation, dict], user: UserModel = None,
               permission: AccessControlPermission = None):
        """
        Update an existing location in the system

        Args:
            public_id (int): PublicID of the location in the system.
            data: New object data
        Notes:
            If a CmdbLocation instance was passed as data argument, \
            it will be auto converted via the model `to_json` method.
        """
        if isinstance(data, CmdbLocation):
            instance = CmdbLocation.to_json(data)
        else:
            instance = json.loads(json.dumps(data, default=json_util.default), object_hook=object_hook)

        type_ = self.type_manager.get(instance.get('type_id'))

        if not type_.active:
            raise AccessDeniedError(f'Objects cannot be updated because type `{type_.name}` is deactivated.')
        verify_access(type_, user, permission)

        update_result = self._update(self.collection, filter={'public_id': public_id}, resource=instance)

        if update_result.matched_count != 1:
            raise ManagerUpdateError('Matched count is higher than 1')

        if self.event_queue and user:
            event = Event("cmdb.core.location.updated",
                            {"id": public_id,
                            "user_id": user.get_public_id(), 
                            "event": 'update'})
            self.event_queue.put(event)

        return update_result


    def update_many(self, query: dict, update: dict):
        """
        update all documents that match the filter from a collection.
        Args:
            query (dict): A query that matches the documents to update.
            update (dict): The modifications to apply.

        Returns:
            acknowledgment of database
        """
        try:
            update_result = self._update_many(self.collection, query=query, update=update)
        except (ManagerUpdateError, AccessDeniedError) as err:
            raise err
        return update_result
