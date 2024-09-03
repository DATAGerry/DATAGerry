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
This module contains the implementation of the ObjectLinksManager
"""
import logging
from queue import Queue
from typing import Union
from datetime import datetime, timezone

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.framework.cmdb_object_manager import CmdbObjectManager

from cmdb.event_management.event import Event
from cmdb.framework import ObjectLinkModel
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel
from cmdb.framework.results import IterationResult
from cmdb.errors.manager import ManagerGetError, ManagerInsertError, ManagerDeleteError, ManagerIterationError

from .base_manager import BaseManager
from .query_builder.base_query_builder import BaseQueryBuilder
from .query_builder.builder_parameters import BuilderParameters
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #

class ObjectLinksManager(BaseManager):
    """
    The ObjectLinksManager handles the interaction between the ObjectLinks-API and the Database
    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, event_queue: Union[Queue, Event] = None, database: str = None):
        """
        Set the database connection and the queue for sending events

        Args:
            database_manager (DatabaseManagerMongo): Active database managers instance.
            event_queue (Queue, Event): The queue for sending events or the created event to send
        """
        self.event_queue = event_queue

        if database:
            dbm.connector.set_database(database)

        self.query_builder = BaseQueryBuilder()
        self.object_manager = CmdbObjectManager(dbm)  # TODO: Replace when object api is updated
        super().__init__(ObjectLinkModel.COLLECTION, dbm)


# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_object_link(self,
                           link: Union[dict, ObjectLinkModel],
                           user: UserModel = None,
                           permission: AccessControlPermission = AccessControlPermission.CREATE) -> int:
        """
        Insert a single object link into the database

        Args:
            link (ObjectLinkModel): Raw data of the link
            user: User requesting this operation
            permission: acl permission
        Returns:
            int: The public_id of the new inserted object link
        """
        try:
            if isinstance(link, ObjectLinkModel):
                link = ObjectLinkModel.to_json(link)

            if 'creation_time' not in link:
                link['creation_time'] = datetime.now(timezone.utc)

            if user and permission:
                self.object_manager.get_object(public_id=link['primary'], user=user, permission=permission)
                self.object_manager.get_object(public_id=link['secondary'], user=user, permission=permission)

            new_public_id = self.insert(link)
        except ManagerGetError as err:
            LOGGER.debug("ManagerGetError: %s", err)
            raise ManagerGetError(err) from err
        except ManagerInsertError as err:
            LOGGER.debug("ManagerInsertError: %s", err)
            raise ManagerInsertError(err) from err

        return new_public_id

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def iterate(self,
                builder_params: BuilderParameters,
                user: UserModel = None,
                permission: AccessControlPermission = None) -> IterationResult[ObjectLinkModel]:
        """
        Iterate over a collection where the public id exists
        """
        try:
            query: list[dict] = self.query_builder.build(builder_params, user, permission)
            count_query: list[dict] = self.query_builder.count(builder_params.get_criteria())

            aggregation_result = list(self.aggregate(query))
            total_cursor = self.aggregate(count_query)

            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']
        except ManagerGetError as err:
            raise ManagerIterationError(err) from err

        try:
            iteration_result: IterationResult[ObjectLinkModel] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(ObjectLinkModel)
        except Exception as err:
            raise ManagerIterationError(err) from err

        return iteration_result


    def get_link(self,
                 public_id: int,
                 user: UserModel = None,
                 permission: AccessControlPermission = None) -> ObjectLinkModel:
        """
        Get a single object link by its public_id

        Args:
            public_id (int): public_id of the object link
            user: User requesting this operation
            permission: acl permission
        Returns:
            ObjectLinkModel: Instance of CmdbLink with data
        """
        try:
            link_instance = self.get_one(public_id)
            link = ObjectLinkModel.from_data(link_instance)

            if user and permission:
                self.object_manager.get_object(link.primary, user, permission)
                self.object_manager.get_object(link.secondary, user, permission)

            return link
        except ManagerGetError as err:
            LOGGER.debug("ManagerGetError: %s", err)
            raise ManagerGetError(f'ObjectLinkModel with ID: {public_id} not found!') from err


    def check_link_exists(self, criteria: dict) -> bool:
        """
        Checks if an object link exists with given primary and secondary public_id

        Args:
            criteria (dict): Dict with primary and secondary public_id's
        Returns:
            bool: True if object link exists, else False
        """
        try:
            link_instance = self.get_one_by(criteria)

            return bool(link_instance)
        except ManagerGetError:
            return False

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_object_link(self,
               public_id: int,
               user: UserModel = None,
               permission: AccessControlPermission = AccessControlPermission.DELETE) -> ObjectLinkModel:
        """
        Delete a existing object link with the given public_id

        Args:
            public_id (int): public_id of the object link
            user: User requesting this operation
            permission: acl permission
        Returns:
            ObjectLinkModel: The deleted link as its model
        """
        try:
            link: dict = self.get_one(public_id)

            if user and permission:
                self.object_manager.get_object(link['primary'], user, permission)
                self.object_manager.get_object(link['secondary'], user, permission)

            self.delete({'public_id':public_id})

            return link
        except Exception as err:
            raise ManagerDeleteError(err) from err
