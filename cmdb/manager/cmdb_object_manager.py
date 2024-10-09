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
This managers represents the core functionalities for the use of CMDB objects.
All communication with the objects is controlled by this managers.
The implementation of the managers used is always realized using the respective superclass.
"""
import logging
import json
from queue import Queue
from bson import json_util

from cmdb.cmdb_objects.cmdb_base import CmdbManagerBase
from cmdb.manager.objects_manager import ObjectsManager

from cmdb.database.utils import object_hook
from cmdb.event_management.event import Event
from cmdb.framework.models.category import CategoryModel
from cmdb.cmdb_objects.cmdb_object import CmdbObject
from cmdb.framework.models.type import TypeModel
from cmdb.search.query import Pipeline
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management.models.user import UserModel
from cmdb.security.acl.helpers import verify_access

from cmdb.errors.manager.object_manager import ObjectManagerGetError,\
                                               ObjectManagerInitError,\
                                               ObjectManagerDeleteError
from cmdb.errors.cmdb_object import RequiredInitKeyNotFoundError
from cmdb.errors.security import AccessDeniedError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   CmdbObjectManager                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
class CmdbObjectManager(CmdbManagerBase):
    """
    Extends: CmdbManagerBase
    """
    def __init__(self, database_manager=None, event_queue: Queue = None, database: str = None):
        self._event_queue = event_queue

        if database:
            database_manager.connector.set_database(database)

        self.objects_manager = ObjectsManager(database_manager)
        super().__init__(database_manager)


    def aggregate(self, collection, pipeline: Pipeline, **kwargs):
        """TODO: document"""
        try:
            return self._aggregate(collection=collection, pipeline=pipeline, **kwargs)
        except Exception as error:
            raise ObjectManagerGetError(error) from error


    def get_objects_by(self, sort='public_id', direction=-1, user: UserModel = None,
                       permission: AccessControlPermission = None, **requirements):
        """TODO: document"""
        ack = []
        objects = self._get_many(collection=CmdbObject.COLLECTION, sort=sort, direction=direction, **requirements)
        for obj in objects:
            object_ = CmdbObject(**obj)
            try:
                type_ = self.objects_manager.get_object_type(object_.type_id)
                verify_access(type_, user, permission)
            except Exception:
                #TODO: ERROR-FIX
                continue
            ack.append(CmdbObject(**obj))
        return ack


    def get_objects_by_type(self, type_id: int):
        """
        function 'get_objects_by_type' gets all objects with the given type_id

        Args: 
            type_id (int): ID of the type

        Returns:
            list: All objects with the given ID (empty list if none found) 
        """
        return self.get_objects_by(type_id=type_id)


    def group_objects_by_value(self, value: str, match=None, user: UserModel = None,
                               permission: AccessControlPermission = None):
        """This method does not actually
           performs the find() operation
           but instead returns
           a objects grouped by type of the documents that meet the selection criteria.

           Args:
               value (str): grouped by value
               match (dict): stage filters the documents to only pass documents.
               user (UserModel): request user
               permission (AccessControlPermission):  ACL operations
           Returns:
               returns the objects grouped by value of the documents
           """
        ack = []
        agr = []

        if match:
            agr.append({'$match': match})

        agr.append({
            '$group': {
                '_id': '$' + value,
                'result': {'$first': '$$ROOT'},
                'count': {'$sum': 1},
            }
        })

        agr.append({'$sort': {'count': -1}})

        objects = self.dbm.aggregate(CmdbObject.COLLECTION, agr)

        for obj in objects:
            object_ = CmdbObject(**obj['result'])
            try:
                type_ = self.objects_manager.get_object_type(object_.type_id)
                verify_access(type_, user, permission)
            except Exception:
                #TODO: ERROR-FIX
                continue
            ack.append(obj)

        return ack


    def delete_object(self, public_id: int, user: UserModel, permission: AccessControlPermission = None):
        """TODO: document"""
        type_id = self.objects_manager.get_object(public_id).type_id
        type_ = self.objects_manager.get_object_type(type_id)
        if not type_.active:
            #TODO: ERROR-FIX
            raise AccessDeniedError(f'Objects cannot be removed because type `{type_.name}` is deactivated.')
        verify_access(type_, user, permission)
        try:
            if self._event_queue:
                event = Event("cmdb.core.object.deleted",
                              {"id": public_id,
                               "type_id": type_id,
                               "user_id": user.get_public_id(),
                               "event": 'delete'})
                self._event_queue.put(event)
            ack = self._delete(CmdbObject.COLLECTION, public_id)
            return ack
        except Exception as err:
            #TODO: ERROR-FIX
            raise ObjectManagerDeleteError(str(err)) from err


    def delete_many_objects(self, filter_query: dict, public_ids, user: UserModel):
        """TODO: document"""
        ack = self.delete_many(CmdbObject.COLLECTION, filter_query)
        # TODO: RABBIT_MQ
        # if self._event_queue:
        #     event = Event("cmdb.core.objects.deleted", {"ids": public_ids,
        #                                                 "user_id": user.get_public_id(),
        #                                                 "event": 'delete'})
        #     self._event_queue.put(event)
        return ack


    #@deprecated
    def get_all_types(self) -> list[TypeModel]:
        """TODO: document"""
        try:
            raw_types: list[dict] = self._get_many(collection=TypeModel.COLLECTION)
        except Exception as error:
            raise ObjectManagerGetError(err=error) from error
        try:
            return [TypeModel.from_data(type) for type in raw_types]
        except Exception as error:
            raise ObjectManagerInitError(error) from error


    #@deprecated
    def get_type(self, public_id: int):
        """TODO: document"""
        try:
            return TypeModel.from_data(self.dbm.find_one(
                collection=TypeModel.COLLECTION,
                public_id=public_id)
            )
        except RequiredInitKeyNotFoundError as err:
            raise ObjectManagerInitError(err)  from err
        except Exception as err:
            raise ObjectManagerGetError(err=err) from err


    #@deprecated
    def get_types_by(self, sort='public_id', **requirements):
        """TODO: document"""
        try:
            return [TypeModel.from_data(data) for data in
                    self._get_many(collection=TypeModel.COLLECTION, sort=sort, **requirements)]
        except Exception as error:
            raise ObjectManagerGetError(error) from error


    #@deprecated
    def get_type_aggregate(self, arguments):
        """This method does not actually
           performs the find() operation
           but instead returns
           a objects sorted by value of the documents that meet the selection criteria.

           Args:
               arguments: query search for
           Returns:
               returns the list of CMDB Types sorted by value of the documents
           """
        type_list = []
        cursor = self.dbm.aggregate(TypeModel.COLLECTION, arguments)
        for document in cursor:
            put_data = json.loads(json_util.dumps(document), object_hook=object_hook)
            type_list.append(TypeModel.from_data(put_data))
        return type_list


    #@deprecated
    def get_categories_by(self, sort='public_id', **requirements: dict) -> list[CategoryModel]:
        """Get a list of categories by special requirements"""
        try:
            raw_categories = self._get_many(collection=CategoryModel.COLLECTION, sort=sort, **requirements)
        except Exception as error:
            raise ObjectManagerGetError(error) from error
        try:
            return [CategoryModel.from_data(category) for category in raw_categories]
        except Exception as error:
            raise ObjectManagerInitError(error) from error
