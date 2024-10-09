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
Manages Objects in the backend
"""
import logging
from queue import Queue
from typing import Union

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.base_manager import BaseManager

from cmdb.event_management.event import Event
from cmdb.framework import CmdbObject
from cmdb.manager.query_builder.base_query_builder import BaseQueryBuilder
from cmdb.user_management.models.user import UserModel
from cmdb.security.acl.helpers import verify_access
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.framework.models.type import TypeModel

from cmdb.errors.manager.object_manager import ObjectManagerGetError,\
                                               ObjectManagerInitError,\
                                               ObjectManagerInsertError
from cmdb.errors.manager import ManagerGetError, ManagerInsertError
from cmdb.errors.security import AccessDeniedError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                ObjectsManager - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectsManager(BaseManager):
    """
    Interface for objects between backend and database
    Extends: BaseMaanger
    """
    def __init__(self, dbm: MongoDatabaseManager, event_queue: Union[Queue, Event] = None, database:str = None):
        """
        Set the database connection and the queue for sending events

        Args:
            dbm (DatabaseManagerMongo): Database connection
            event_queue (Queue, Event): The queue for events in RabbitMQ
            database (str): name of database for cloud mode
        """
        self.event_queue = event_queue
        self.query_builder = BaseQueryBuilder()

        if database:
            dbm.connector.set_database(database)

        super().__init__(CmdbObject.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_object(self,
                      data: dict,
                      user: UserModel = None,
                      permission: AccessControlPermission = None) -> int:
        """
        Insert new Object

        Args:
            data: Object data
            user: User requesting the action
            permission: Extended user acl rights

        Raises:
            ObjectManagerInsertError: 
        Returns:
            Public ID of the new object in database
        """
        new_object = None

        try:
            new_object = CmdbObject(**data)
        except Exception as err:
            LOGGER.debug("[insert_object] Error while initialising object. Error: %s", str(err))
            raise ObjectManagerInitError(str(err)) from err

        try:
            object_type = self.get_object_type(new_object.type_id)
        except ObjectManagerGetError as err:
            raise ObjectManagerGetError(err) from err

        if not object_type.active:
            raise AccessDeniedError(f'Objects cannot be created because type `{object_type.name}` is deactivated.')

        verify_access(object_type, user, permission)

        try:
            ack = self.insert(new_object.__dict__)
        except ManagerInsertError as err:
            LOGGER.debug("[insert_object] Error while inserting object. Error: %s", str(err))
            raise ObjectManagerInsertError(err) from err
        except Exception as err:
            #TODO: ERROR-FIX
            LOGGER.debug("[insert_object] Error while inserting object. Exception: %s", str(err))
            raise ObjectManagerInsertError(err) from err

        try:
            if self.event_queue:
                event = Event("cmdb.core.object.added",
                                {
                                    "id": new_object.get_public_id(),
                                    "type_id": new_object.get_type_id(),
                                    "user_id": new_object.author_id,
                                    "event": 'insert'
                                }
                             )

                self.event_queue.put(event)
        except Exception:
            #TODO: ERROR-FIX
            LOGGER.debug("[insert_object] Error while creating object event. Error: %s", str(err))

        return ack

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_object(self, public_id: int,
            user: UserModel = None,
            permission: AccessControlPermission = None) -> CmdbObject:
        """
        Get a single object by its id

        Args:
            public_id (int): ID of the object
            user: Request user
            permission: ACL permission

        Raises:
            ObjectManagerGetError: If object was not found

        Returns:
            (CmdbObject): Requested object
        """
        try:
            requested_object = self.get_one(public_id)
        except Exception as err:
            LOGGER.debug("[get_object] Error: %s, Type: %s", err, type(err))
            raise ObjectManagerGetError(f"Error while retrieving object with ID: {public_id}! Error: {err}") from err

        if requested_object:
            requested_object = CmdbObject.from_data(requested_object)
            object_type = self.get_object_type(requested_object.type_id)
            verify_access(object_type, user, permission)

            return requested_object

        raise ObjectManagerGetError(f'Object with ID: {public_id} not found!')


    def get_object_type(self, type_id: int) -> TypeModel:
        """
        Retrieves the CmdbType for the given public_id of the CmdbType

        Args:
            type_id (int): public_id of the CmdbType

        Returns:
            TypeModel: CmdbType with the given type_id
        """
        try:
            requested_type = self.get_one_from_other_collection(TypeModel.COLLECTION, type_id)
            requested_type = TypeModel.from_data(requested_type)
        except Exception as err:
            LOGGER.debug("[get_object_type] Error: %s, Type: %s", err, type(err))
            raise ObjectManagerGetError(f"Error while retrieving type with ID: {type_id}. Error: {err}") from err

        return requested_type


    def count_objects(self, criteria: dict = None):
        """
        Returns the number of objects with the given criteria

        Args:
            criteria (dict): Filter for counting documents like {'type_id: 1} 

        Raises:
            ObjectManagerGetError: When an error occures during counting objects

        Returns:
            (int): Returns the number of documents with the given criteria
        """
        try:
            if criteria:
                object_count = self.count_documents(self.collection, filter=criteria)
            else:
                object_count = self.count_documents(self.collection)
        except ManagerGetError as err:
            raise ObjectManagerGetError(err) from err

        return object_count


    def get_new_object_public_id(self) -> int:
        """
        Gets the next couter for the public_id from database and increases it

        Returns:
            int: The next public_id for CmdbObject
        """
        return self.get_next_public_id()


    # TODO: REFACTOR-FIX (Move to TypeManager once refactored)
    def count_types(self):
        """TODO: document"""
        return self.count_documents(collection=TypeModel.COLLECTION)

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #
