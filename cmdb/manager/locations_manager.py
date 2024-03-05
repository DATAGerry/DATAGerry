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
This module contains the implementation of the LocationsManager
"""
import logging

from queue import Queue
from typing import Union

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.framework.managers.type_manager import TypeManager

from cmdb.event_management.event import Event
from cmdb.framework import CmdbLocation
from cmdb.framework.results.iteration import IterationResult
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel

from cmdb.errors.manager import ManagerInsertError, ManagerGetError, ManagerIterationError

from .base_manager import BaseManager
from .query_builder.base_query_builder import BaseQueryBuilder
from .query_builder.builder_parameters import BuilderParameters
# -------------------------------------------------------------------------------------------------------------------- #
LOGGER = logging.getLogger(__name__)


class LocationsManager(BaseManager):
    """
    The LocationsManager handles the interaction between the Location-API and the Database
    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, event_queue: Union[Queue, Event] = None):
        """
        Set the database connection and the queue for sending events

        Args:
            database_manager (DatabaseManagerMongo): Active database managers instance
            event_queue (Queue, Event): The queue for sending events or the created event to send
        """
        self.event_queue = event_queue
        self.query_builder = BaseQueryBuilder()
        self.type_manager = TypeManager(dbm)
        super().__init__(CmdbLocation.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_location(self, data: dict) -> int:
        """
        Insert new location in the database
        Args:
            data (dict): data of the new location
        Returns:
            Public ID of the new object in database
        """
        try:
            ack = self.insert(data)
        except Exception as err:
            raise ManagerInsertError(err) from err

        return ack

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def iterate(self,
                builder_params: BuilderParameters,
                user: UserModel = None,
                permission: AccessControlPermission = None) -> IterationResult[CmdbLocation]:
        """
        Performs an aggregation on the database
        Args:
            builder_params (BuilderParameters): Contains input to identify the target of action
            user (UserModel, optional): User requesting this action
            permission (AccessControlPermission, optional): Permission which should be checked for the user
        Raises:
            ManagerIterationError: Raised when something goes wrong during the aggregate part
            ManagerIterationError: Raised when something goes wrong during the building of the IterationResult
        Returns:
            IterationResult[CmdbLocation]: Result which matches the Builderparameters
        """
        try:
            query: list[dict] = self.query_builder.build(builder_params,user, permission)
            count_query: list[dict] = self.query_builder.count(builder_params.get_criteria())

            aggregation_result = list(self.aggregate(query))
            total_cursor = self.aggregate(count_query)

            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']

        except ManagerGetError as err:
            raise ManagerIterationError(err) from err

        try:
            iteration_result: IterationResult[CmdbLocation] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbLocation)
        except Exception as err:
            raise ManagerIterationError(err) from err

        return iteration_result


    def get_location(self, public_id: int) -> CmdbLocation:
        """
        Retrives a location with the given public_id

        Args:
            public_id (int): public_id of the location which should be retrieved
        Returns:
            CmdbLocation: _description_
        """
        try:
            resource = []
            location = self.get_one(public_id)
            if location:
                resource = CmdbLocation(**location)
        except Exception as err:
            raise ManagerGetError(str(err)) from err

        return resource


    def get_location_for_object(self, object_id: int) -> CmdbLocation:
        """
        Retrieves a single location for the given object

        Args:
            object_id (int): public_id of the object

        Raises:
            ManagerGetError: When location could not be retrieved

        Returns:
            CmdbLocation: The requested location
        """
        try:
            location = self.get_one_by({'object_id':object_id})
            if location:
                location = CmdbLocation(**location)

        except Exception as err:
            raise ManagerGetError(str(err)) from err

        if not location:
            location = []

        return location


    def get_locations_by(self, **requirements):
        """Retrieves all locations matching the key-value pairs

        Returns:
            list: All locations matching the requirements
        """
        locations_list = []
        try:
            locations = self.get_many(**requirements)

            for location in locations:
                locations_list.append(CmdbLocation(**location))

        except Exception as err:
            raise ManagerGetError(str(err)) from err

        return locations_list

# ------------------------------------------------- HELPER FUNCTIONS ------------------------------------------------- #

    def get_all_children(self, public_id: int, all_locations: dict):
        """
        Retrieves all children for a given location with the public_id

        Args:
            public_id (int): public_id of the parent location
            all_locations (dict): all locations from db

        Returns:
            (list[dict]): Returns all child locations
        """
        found_children: list[dict] = []
        recursive_children: list[dict] = []

        # add direct children
        for location in all_locations:
            if location['parent'] == public_id:
                found_children.append(location)

        # search recursive for all children
        if len(found_children) > 0:
            for child in found_children:
                recursive_children = self.get_all_children(child['public_id'], all_locations)

                # add recursive children to found_children
                if len(recursive_children) > 0:
                    found_children += recursive_children

        return found_children
