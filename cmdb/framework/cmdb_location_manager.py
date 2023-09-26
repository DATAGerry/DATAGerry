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
This managers represents the core functionalities for the use of CMDB objects.
All communication with the objects is controlled by this managers.
The implementation of the managers used is always realized using the respective superclass.

"""
import logging
import json

from typing import Union
from queue import Queue
from bson import json_util

from flask import current_app

from cmdb.database.utils import object_hook
from cmdb.database.errors.database_errors import PublicIDAlreadyExists
from cmdb.event_management.event import Event
from cmdb.framework.cmdb_base import CmdbManagerBase
from cmdb.framework.managers.type_manager import TypeManager
from cmdb.framework.cmdb_errors import ObjectInsertError, LocationManagerDeleteError, LocationManagerError, \
    LocationManagerInsertError
from cmdb.framework.cmdb_location import CmdbLocation
from cmdb.framework.models.type import TypeModel
from cmdb.search.query import Pipeline
from cmdb.security.acl.control import AccessControlList
from cmdb.security.acl.errors import AccessDeniedError
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.utils.error import CMDBError
from cmdb.user_management import UserModel
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.managers.object_manager import ObjectManager

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                    MANAGERS SETUP                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

with current_app.app_context():
    object_manager = CmdbObjectManager(current_app.database_manager, current_app.event_queue)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                    ACCESS CONTROL                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

def has_access_control(model: TypeModel, user: UserModel, permission: AccessControlPermission) -> bool:
    """Check if a user has access to location/locations for a given permission"""
    acl: AccessControlList = model.acl
    if acl and acl.activated:
        return acl.verify_access(user.group_id, permission)
    return True


def verify_access(model: TypeModel, user: UserModel = None, permission: AccessControlPermission = None):
    """Validate if a user has access to locations of this type."""
    if not user or not permission:
        return

    verify = has_access_control(model, user, permission)
    if not verify:
        raise AccessDeniedError('Protected by ACL permission!')


# -------------------------------------------------------------------------------------------------------------------- #


class CmdbLocationManager(CmdbManagerBase):
    """
    class CmdbLocationManager
    """
    def __init__(self, database_manager=None, event_queue: Queue = None):
        self._event_queue = event_queue
        self._type_manager = TypeManager(database_manager)
        super().__init__(database_manager)


    def get_location_for_object(self, object_id: int, user: UserModel = None,
                   permission: AccessControlPermission = None) -> CmdbLocation:
        try:
            resource = self.get_location_by_object(collection=CmdbLocation.COLLECTION, object_id=object_id)
            if resource:
                resource = CmdbLocation(**resource)

        except Exception as error:
            raise LocationManagerError(str(error)) from error

        # if resource.type_id > 0:
        #     type_ = self._type_manager.get(resource.type_id)
        #     verify_access(type_, user, permission)
        return resource


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


    def get_location(self, public_id: int, user: UserModel = None,
                   permission: AccessControlPermission = None) -> CmdbLocation:
        try:
            resource = []
            location = self._get(collection=CmdbLocation.COLLECTION, public_id=public_id)
            if location:
                resource = CmdbLocation(**location)
        except Exception as error:
            raise LocationManagerError(str(error)) from error

        if resource and resource.type_id and resource.type_id > 0:
            type_ = self._type_manager.get(resource.type_id)
            verify_access(type_, user, permission)
        return resource

    def get_locations_by(self, sort='public_id', direction=-1, user: UserModel = None,
                       permission: AccessControlPermission = None, **requirements):
        ack = []
        locations = self._get_many(collection=CmdbLocation.COLLECTION, sort=sort, direction=direction, **requirements)

        for location in locations:
            location_ = CmdbLocation(**location)
            try:
                type_ = self._type_manager.get(location_.type_id)
                verify_access(type_, user, permission)
            except CMDBError:
                LOGGER.debug("Error in get_locations_by")
                continue
            ack.append(CmdbLocation(**location))
        return ack

    def get_locations_by_type(self, type_id: int):
        """
        function 'get_objects_by_type' gets all objects with the given type_id

        Args: 
            type_id (int): ID of the type

        Returns:
            list: All objects with the given ID (empty list if none found) 
        """
        return self.get_locations_by(type_id=type_id)

    def count_locations_by_type(self, public_id: int):
        """This method does not actually
               performs the find() operation
               but instead returns
               a numerical count of the documents that meet the selection criteria.

               Args:
                   public_id (int): public id of document
               Returns:
                   returns the count of the documents
               """

        formatted_type_id = {'type_id': public_id}
        return self.dbm.count(CmdbLocation.COLLECTION, formatted_type_id)

    def count_locations(self):
        return self.dbm.count(collection=CmdbLocation.COLLECTION)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                    UPDATE SECTION                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

    def insert_location(self, data: Union[CmdbLocation, dict], user: UserModel = None,
                      permission: AccessControlPermission = None) -> int:
        """
        Insert new CMDB Object
        Args:
            data: init data
            user: current user, to detect who triggered event
            permission: extended user acl rights
        Returns:
            Public ID of the new object in database
        """
        new_location = None
        if isinstance(data, dict):
            try:
                new_location = CmdbLocation(**data)
            except CMDBError as error:
                LOGGER.debug('Error while inserting object - error: %s', error)
                raise LocationManagerInsertError(error) from error
        elif isinstance(data, CmdbLocation):
            new_location = data

        type_ = self._type_manager.get(new_location.type_id)
        if not type_.active:
            raise AccessDeniedError(f'Objects cannot be created because type `{type_.name}` is deactivated.')

        verify_access(type_, user, permission)

        try:
            ack = self.dbm.insert(
                collection=CmdbLocation.COLLECTION,
                data=new_location.__dict__
            )
            # if self._event_queue:
            #     event = Event("cmdb.core.location.added", {"id": new_location.public_id,
            #                                              "type_id": new_location.type_id,
            #                                              "object_id": new_location.object_id,
            #                                              "name": new_location.name,
            #                                              "parent": new_location.parent,
            #                                              "event": 'insert'})
            #     self._event_queue.put(event)
        except (CMDBError, PublicIDAlreadyExists) as error:
            raise ObjectInsertError(error) from error
        return ack


# -------------------------------------------------------------------------------------------------------------------- #
#                                                    DELETE SECTION                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

    def delete_location(self, public_id: int, user: UserModel, permission: AccessControlPermission = None):
        current_location_instance: CmdbLocation = self.get_location(public_id=public_id)
        type_ = self._type_manager.get(current_location_instance.type_id)

        if not type_.active:
            raise AccessDeniedError(f'Objects cannot be removed because type `{type_.name}` is deactivated.')
        verify_access(type_, user, permission)
        try:
            # if self._event_queue:
            #     event = Event("cmdb.core.location.deleted",
            #                   {"id": public_id,
            #                    "user_id": user.get_public_id(),
            #                    "event": 'delete'})
            #     self._event_queue.put(event)

            # first delete the reference on the corresponding object
            current_object_instance = object_manager.get_object(current_location_instance.object_id)

            if current_object_instance:
                for current_object_field in current_object_instance.fields:
                    if current_object_field['name'] == 'dg_location':
                        current_object_field['value'] = None

            manager = ObjectManager(database_manager=current_app.database_manager, event_queue=current_app.event_queue)
            manager.update(current_object_instance.public_id,current_object_instance)

            # then delete the location itself
            ack = self._delete(CmdbLocation.COLLECTION, public_id)
            return ack
        except (CMDBError, Exception) as error:
            raise LocationManagerDeleteError(error) from error


# -------------------------------------------------------------------------------------------------------------------- #
#                                                    HELPERS SECTION                                                   #
# -------------------------------------------------------------------------------------------------------------------- #

    def is_ready(self) -> bool:
        """
        function 'is_ready' returns the current database connector status

        Returns:
            bool: Connector is connected to database
        """
        return self.dbm.status()

    def get_new_id(self, collection: str) -> int:
        """
        Retrieves next publicID
        Args:
            collection (str): used collection

        Returns:
            int: new publicID
        """
        return self.dbm.get_next_public_id(collection)


    def has_children(self, public_id: int):
        try:
            has_child = False
            a_child = self._get_child(CmdbLocation.COLLECTION,public_id)

            if a_child:
                has_child = True
        except Exception as error:
            raise LocationManagerError(str(error)) from error

        return has_child


    def aggregate(self, collection, pipeline: Pipeline, **kwargs):
        try:
            return self._aggregate(collection=collection, pipeline=pipeline, **kwargs)
        except Exception as error:
            raise LocationManagerError(error) from error
