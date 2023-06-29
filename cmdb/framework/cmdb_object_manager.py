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

from typing import List
from queue import Queue
from bson import json_util

from cmdb.database.utils import object_hook
from cmdb.database.errors.database_errors import PublicIDAlreadyExists
from cmdb.event_management.event import Event
from cmdb.framework.cmdb_base import CmdbManagerBase
from cmdb.framework.managers.type_manager import TypeManager
from cmdb.framework.models.category import CategoryModel
from cmdb.framework.cmdb_dao import RequiredInitKeyNotFoundError
from cmdb.framework.cmdb_errors import ObjectInsertError, ObjectDeleteError, ObjectManagerGetError, \
    ObjectManagerInsertError, ObjectManagerInitError, FieldNotFoundError, FieldInitError
from cmdb.framework.cmdb_object import CmdbObject
from cmdb.framework.models.type import TypeModel
from cmdb.search.query import Pipeline
from cmdb.security.acl.control import AccessControlList
from cmdb.security.acl.errors import AccessDeniedError
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.utils.error import CMDBError
from cmdb.user_management import UserModel
from cmdb.utils.wraps import deprecated

LOGGER = logging.getLogger(__name__)


def has_access_control(model: TypeModel, user: UserModel, permission: AccessControlPermission) -> bool:
    """Check if a user has access to object/objects for a given permission"""
    acl: AccessControlList = model.acl
    if acl and acl.activated:
        return acl.verify_access(user.group_id, permission)
    return True


def verify_access(model: TypeModel, user: UserModel = None, permission: AccessControlPermission = None):
    """Validate if a user has access to objects of this type."""
    if not user or not permission:
        return

    verify = has_access_control(model, user, permission)
    if not verify:
        raise AccessDeniedError('Protected by ACL permission!')


class CmdbObjectManager(CmdbManagerBase):
    """
    class CmdbObjectManager
    """
    def __init__(self, database_manager=None, event_queue: Queue = None):
        self._event_queue = event_queue
        self._type_manager = TypeManager(database_manager)
        super(CmdbObjectManager, self).__init__(database_manager)

    def is_ready(self) -> bool:
        """
        function 'is_ready' returns the current database connector status

        Returns:
            bool: Connector is connected to database
        """
        return self.dbm.status()

    def get_new_id(self, collection: str) -> int:
        return self.dbm.get_next_public_id(collection)

    def aggregate(self, collection, pipeline: Pipeline, **kwargs):
        try:
            return self._aggregate(collection=collection, pipeline=pipeline, **kwargs)
        except Exception as err:
            raise ObjectManagerGetError(err)

    def get_object(self, public_id: int, user: UserModel = None,
                   permission: AccessControlPermission = None) -> CmdbObject:
        try:
            resource = CmdbObject(**self._get(
                collection=CmdbObject.COLLECTION,
                public_id=public_id))
        except Exception as err:
            raise ObjectManagerGetError(str(err))

        type_ = self._type_manager.get(resource.type_id)
        verify_access(type_, user, permission)
        return resource

    def get_objects_by(self, sort='public_id', direction=-1, user: UserModel = None,
                       permission: AccessControlPermission = None, **requirements):
        ack = []
        objects = self._get_many(collection=CmdbObject.COLLECTION, sort=sort, direction=direction, **requirements)
        for obj in objects:
            object_ = CmdbObject(**obj)
            try:
                type_ = self._type_manager.get(object_.type_id)
                verify_access(type_, user, permission)
            except CMDBError:
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

    def count_objects_by_type(self, public_id: int):
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
        return self.dbm.count(CmdbObject.COLLECTION, formatted_type_id)

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
                type_ = self._type_manager.get(object_.type_id)
                verify_access(type_, user, permission)
            except CMDBError:
                continue
            ack.append(obj)
        return ack

    def sort_objects_by_field_value(self, value: str, order=-1, match=None):
        """This method does not actually
           performs the find() operation
           but instead returns
           a objects sorted by value of the documents that meet the selection criteria.

           Args:
               value (str): sorted by value
               order : Ascending/Descending Sort e.g. -1
               match (dict): stage filters the documents to only pass documents.
           Returns:
               returns the list of CMDB Objects sorted by value of the documents
           """
        agr = []
        if match:
            agr.append({'$match': match})
        agr.append({"$addFields": {
            "order": {
                "$filter": {
                    "input": "$fields",
                    "as": "fields",
                    "cond": {"$eq": ["$$fields.name", value]}
                }
            }
        }})
        agr.append({'$sort': {'order': order}})

        object_list = []
        cursor = self.dbm.aggregate(CmdbObject.COLLECTION, agr)
        for document in cursor:
            put_data = json.loads(json_util.dumps(document), object_hook=object_hook)
            object_list.append(CmdbObject(**put_data))

        return object_list

    def count_objects(self):
        return self.dbm.count(collection=CmdbObject.COLLECTION)

    def _find_query_fields(self, query, match_fields=None):

        match_fields = match_fields or list()
        for key, items in query.items():
            if isinstance(items, dict):
                if 'fields.value' == key:
                    match_fields.append(items['$regex'])
                else:
                    for item in items:
                        self._find_query_fields(item, match_fields=match_fields)
        return match_fields

    def insert_object(self, data: (CmdbObject, dict), user: UserModel = None,
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
        new_object = None
        if isinstance(data, dict):
            try:
                new_object = CmdbObject(**data)
            except CMDBError as e:
                LOGGER.debug(f'Error while inserting object - error: {e.message}')
                raise ObjectManagerInsertError(e)
        elif isinstance(data, CmdbObject):
            new_object = data

        type_ = self._type_manager.get(new_object.type_id)
        if not type_.active:
            raise AccessDeniedError(f'Objects cannot be created because type `{type_.name}` is deactivated.')

        verify_access(type_, user, permission)

        try:
            ack = self.dbm.insert(
                collection=CmdbObject.COLLECTION,
                data=new_object.__dict__
            )
            if self._event_queue:
                event = Event("cmdb.core.object.added", {"id": new_object.get_public_id(),
                                                         "type_id": new_object.get_type_id(),
                                                         "user_id": new_object.author_id,
                                                         "event": 'insert'})
                self._event_queue.put(event)
        except (CMDBError, PublicIDAlreadyExists) as e:
            raise ObjectInsertError(e)
        return ack

    def get_object_references(self, public_id: int, active_flag=None, user: UserModel = None,
                              permission: AccessControlPermission = None) -> list:
        # Type of given object id
        type_id = self.get_object(public_id=public_id, user=user, permission=permission).type_id

        # query for all types with ref input type with value of type id
        req_type_query = {
            "$and": [
                {'fields': {'$elemMatch': {'type': 'ref'}}},
                {'$or':
                    [
                        {'fields': {'$elemMatch': {'ref_types': type_id}}},
                        {'fields': {'$elemMatch': {'ref_types': {'$in': [type_id]}}}}
                    ]
                }
            ]
        }

        # get type list with given query
        req_type_list = self.get_types_by(**req_type_query)
        type_init_list = []
        for new_type_init in req_type_list:
            try:
                current_loop_type = new_type_init
                ref_fields = current_loop_type.get_fields_of_type_with_value(input_type='ref', _filter='ref_types',
                                                                             value=type_id)
                for ref_field in ref_fields:
                    type_init_list.append(
                        {"type_id": current_loop_type.get_public_id(), "field_name": ref_field['name']})
            except (CMDBError, FieldNotFoundError, FieldInitError):
                continue

        referenced_by_objects = []
        for possible_object_types in type_init_list:
            referenced_query = {"type_id": possible_object_types['type_id'], "fields": {
                "$elemMatch": {"$and": [{"name": possible_object_types['field_name']}],
                               "$or": [{"value": int(public_id)}, {"value": str(public_id)}]}}}
            if active_flag:
                referenced_query.update({'active': {"$eq": True}})

            referenced_by_objects = referenced_by_objects + self.get_objects_by(**referenced_query,
                                                                                user=user, permission=permission)

        return referenced_by_objects

    def delete_object(self, public_id: int, user: UserModel, permission: AccessControlPermission = None):
        type_id = self.get_object(public_id=public_id).type_id
        type_ = self._type_manager.get(type_id)
        if not type_.active:
            raise AccessDeniedError(f'Objects cannot be removed because type `{type_.name}` is deactivated.')
        verify_access(type_, user, permission)
        try:
            if self._event_queue:
                event = Event("cmdb.core.object.deleted",
                              {"id": public_id,
                               "type_id": self.get_object(public_id).get_type_id(),
                               "user_id": user.get_public_id(),
                               "event": 'delete'})
                self._event_queue.put(event)
            ack = self._delete(CmdbObject.COLLECTION, public_id)
            return ack
        except (CMDBError, Exception):
            raise ObjectDeleteError(msg=public_id)

    def delete_many_objects(self, filter_query: dict, public_ids, user: UserModel):
        ack = self._delete_many(CmdbObject.COLLECTION, filter_query)
        if self._event_queue:
            event = Event("cmdb.core.objects.deleted", {"ids": public_ids,
                                                        "user_id": user.get_public_id(),
                                                        "event": 'delete'})
            self._event_queue.put(event)
        return ack

    #@deprecated
    def get_all_types(self) -> List[TypeModel]:
        try:
            raw_types: List[dict] = self._get_many(collection=TypeModel.COLLECTION)
        except Exception as err:
            raise ObjectManagerGetError(err=err)
        try:
            return [TypeModel.from_data(type) for type in raw_types]
        except Exception as err:
            raise ObjectManagerInitError(err=err)

    #@deprecated
    def get_type(self, public_id: int):
        try:
            return TypeModel.from_data(self.dbm.find_one(
                collection=TypeModel.COLLECTION,
                public_id=public_id)
            )
        except RequiredInitKeyNotFoundError as err:
            raise ObjectManagerInitError(err=err.message)
        except Exception as err:
            raise ObjectManagerGetError(err=err)

    #@deprecated
    def get_types_by(self, sort='public_id', **requirements):
        try:
            return [TypeModel.from_data(data) for data in
                    self._get_many(collection=TypeModel.COLLECTION, sort=sort, **requirements)]
        except Exception as err:
            raise ObjectManagerGetError(err=err)

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
    def count_types(self):
        return self.dbm.count(collection=TypeModel.COLLECTION)

    #@deprecated
    def get_categories(self) -> List[CategoryModel]:
        """Get all categories as nested list"""
        try:
            raw_categories = self._get_many(collection=CategoryModel.COLLECTION, sort='public_id')
        except Exception as err:
            raise ObjectManagerGetError(err)
        try:
            return [CategoryModel.from_data(category) for category in raw_categories]
        except Exception as err:
            raise ObjectManagerInitError(err)

    #@deprecated
    def get_category_by(self, **requirements) -> CategoryModel:
        """Get a single category by requirements
        Notes:
            Even if multiple categories match the requirements only the first matched will be returned
        """
        try:
            raw_category = self._get_by(collection=CategoryModel.COLLECTION, **requirements)
        except Exception as err:
            raise ObjectManagerGetError(err)

        try:
            return CategoryModel.from_data(raw_category)
        except Exception as err:
            raise ObjectManagerInitError(err)

    #@deprecated
    def get_categories_by(self, sort='public_id', **requirements: dict) -> List[CategoryModel]:
        """Get a list of categories by special requirements"""
        try:
            raw_categories = self._get_many(collection=CategoryModel.COLLECTION, sort=sort, **requirements)
        except Exception as err:
            raise ObjectManagerGetError(err)
        try:
            return [CategoryModel.from_data(category) for category in raw_categories]
        except Exception as err:
            raise ObjectManagerInitError(err)

    #@deprecated
    def insert_category(self, category: CategoryModel):
        """Add a new category into the database or add the children list an existing category"""
        try:
            return self._insert(collection=CategoryModel.COLLECTION, data=CategoryModel.to_json(category))
        except Exception as err:
            raise ObjectManagerInsertError(err=err)
