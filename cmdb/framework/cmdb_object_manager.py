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

"""
This managers represents the core functionalities for the use of CMDB objects.
All communication with the objects is controlled by this managers.
The implementation of the managers used is always realized using the respective superclass.

"""
import logging
import json

from cmdb.database.utils import object_hook
from bson import json_util
from datetime import datetime
from typing import List

from cmdb.database.errors.database_errors import PublicIDAlreadyExists
from cmdb.event_management.event import Event
from cmdb.framework.cmdb_base import CmdbManagerBase
from cmdb.framework.managers.type_manager import TypeManager
from cmdb.framework.models.category import CategoryModel
from cmdb.framework.cmdb_dao import RequiredInitKeyNotFoundError
from cmdb.framework.cmdb_errors import WrongInputFormatError, \
    ObjectInsertError, ObjectDeleteError, ObjectManagerGetError, \
    ObjectManagerInsertError, ObjectManagerUpdateError, ObjectManagerDeleteError, ObjectManagerInitError
from cmdb.framework.cmdb_link import CmdbLink
from cmdb.framework.cmdb_object import CmdbObject
from cmdb.framework.models.type import TypeModel
from cmdb.search.query import Query, Pipeline
from cmdb.security.acl.control import AccessControlList
from cmdb.security.acl.errors import AccessDeniedError
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.utils.error import CMDBError
from cmdb.user_management import UserModel
from cmdb.utils.wraps import deprecated

LOGGER = logging.getLogger(__name__)


def has_access_control(type: TypeModel, user: UserModel, permission: AccessControlPermission) -> bool:
    """Check if a user has access to object/objects for a given permission"""
    acl: AccessControlList = type.acl
    if acl and acl.activated:
        return acl.verify_access(user.group_id, permission)
    return True


def verify_access(type: TypeModel, user: UserModel = None, permission: AccessControlPermission = None):
    """Validate if a user has access to objects of this type."""
    if not user or not permission:
        return

    verify = has_access_control(type, user, permission)
    if not verify:
        raise AccessDeniedError('Protected by ACL permission!')


class CmdbObjectManager(CmdbManagerBase):

    def __init__(self, database_manager=None, event_queue=None):
        self._event_queue = event_queue
        self._type_manager = TypeManager(database_manager)
        super(CmdbObjectManager, self).__init__(database_manager)

    def is_ready(self) -> bool:
        return self.dbm.status()

    def get_new_id(self, collection: str) -> int:
        return self.dbm.get_next_public_id(collection)

    def aggregate(self, collection, pipeline: Pipeline, **kwargs):
        try:
            return self._aggregate(collection=collection, pipeline=pipeline, **kwargs)
        except Exception as err:
            raise ObjectManagerGetError(err)

    def search(self, collection, query: Query, **kwargs):
        try:
            return self._search(collection=collection, query=query, **kwargs)
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

    def get_objects(self, public_ids: list):
        object_list = []
        for public_id in public_ids:
            try:
                object_list.append(self.get_object(public_id))
            except CMDBError as err:
                LOGGER.error(err)
                continue
        return object_list

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

    def group_objects_by_value(self, value: str, match=None):
        """This method does not actually
           performs the find() operation
           but instead returns
           a objects grouped by type of the documents that meet the selection criteria.

           Args:
               value (str): grouped by value
               match (dict): stage filters the documents to only pass documents.
           Returns:
               returns the objects grouped by value of the documents
           """
        agr = []
        if match:
            agr.append({'$match': match})
        agr.append({'$group': {'_id': '$' + value, 'count': {'$sum': 1}}})
        agr.append({'$sort': {'count': -1}})

        return self.dbm.aggregate(CmdbObject.COLLECTION, agr)

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
        if isinstance(data, dict):
            try:
                new_object = CmdbObject(**data)
            except CMDBError as e:
                LOGGER.debug(f'Error while inserting object - error: {e.message}')
                raise ObjectManagerInsertError(e)
        elif isinstance(data, CmdbObject):
            new_object = data

        type_ = self._type_manager.get(new_object.type_id)
        verify_access(type_, user, permission)

        try:
            ack = self.dbm.insert(
                collection=CmdbObject.COLLECTION,
                data=new_object.__dict__
            )
            if self._event_queue:
                event = Event("cmdb.core.object.added", {"id": new_object.get_public_id(),
                                                         "type_id": new_object.get_type_id(),
                                                         "user_id": new_object.author_id})
                self._event_queue.put(event)
        except (CMDBError, PublicIDAlreadyExists) as e:
            raise ObjectInsertError(e)
        return ack

    def update_object(self, data: (dict, CmdbObject), user: UserModel = None,
                      permission: AccessControlPermission = None) -> str:
        if isinstance(data, dict):
            update_object = CmdbObject(**data)
        elif isinstance(data, CmdbObject):
            update_object = data
        else:
            raise ObjectManagerUpdateError('Wrong CmdbObject init format - expecting CmdbObject or dict')
        update_object.last_edit_time = datetime.utcnow()

        type_ = self._type_manager.get(update_object.type_id)
        verify_access(type_, user, permission)

        ack = self._update(
            collection=CmdbObject.COLLECTION,
            public_id=update_object.get_public_id(),
            data=update_object.__dict__
        )
        # create cmdb.core.object.updated event
        if self._event_queue and user:
            event = Event("cmdb.core.object.updated", {"id": update_object.get_public_id(),
                                                       "type_id": update_object.get_type_id(),
                                                       "user_id": user.get_public_id()})
            self._event_queue.put(event)
        return ack.acknowledged

    def remove_object_fields(self, filter_query: dict, update: dict):
        ack = self._update_many(CmdbObject.COLLECTION, filter_query, update)
        return ack

    def update_object_fields(self, filter: dict, update: dict):
        ack = self._update_many(CmdbObject.COLLECTION, filter, update)
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
            except CMDBError:
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

    def delete_object(self, public_id: int, user: UserModel, permission: AccessControlPermission):
        type_id = self.get_object(public_id=public_id).type_id
        type_ = self._type_manager.get(type_id)
        verify_access(type_, user, permission)
        try:
            if self._event_queue:
                event = Event("cmdb.core.object.deleted",
                              {"id": public_id,
                               "type_id": self.get_object(public_id).get_type_id(),
                               "user_id": user.get_public_id()})
                self._event_queue.put(event)
            ack = self._delete(CmdbObject.COLLECTION, public_id)
            return ack
        except (CMDBError, Exception):
            raise ObjectDeleteError(msg=public_id)

    def delete_many_objects(self, filter_query: dict, public_ids, user: UserModel):
        ack = self._delete_many(CmdbObject.COLLECTION, filter_query)
        if self._event_queue:
            event = Event("cmdb.core.objects.deleted", {"ids": public_ids,
                                                        "user_id": user.get_public_id()})
            self._event_queue.put(event)
        return ack

    @deprecated
    def get_all_types(self) -> List[TypeModel]:
        try:
            raw_types: List[dict] = self._get_many(collection=TypeModel.COLLECTION)
        except Exception as err:
            raise ObjectManagerGetError(err=err)
        try:
            return [TypeModel.from_data(type) for type in raw_types]
        except Exception as err:
            raise ObjectManagerInitError(err=err)

    @deprecated
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

    @deprecated
    def get_types_by(self, sort='public_id', **requirements):
        try:
            return [TypeModel.from_data(data) for data in
                    self._get_many(collection=TypeModel.COLLECTION, sort=sort, **requirements)]
        except Exception as err:
            raise ObjectManagerGetError(err=err)

    @deprecated
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

    @deprecated
    def update_type(self, data: (TypeModel, dict)):
        if isinstance(data, TypeModel):
            update_type = data
        elif isinstance(data, dict):
            update_type = TypeModel.from_data(data)
        else:
            raise WrongInputFormatError(TypeModel, data, "Possible data: dict or TypeModel")

        ack = self._update(
            collection=TypeModel.COLLECTION,
            public_id=update_type.get_public_id(),
            data=TypeModel.to_json(update_type)
        )
        if self._event_queue:
            event = Event("cmdb.core.objecttype.updated", {"id": update_type.get_public_id()})
            self._event_queue.put(event)
        return ack

    @deprecated
    def update_many_types(self, filter: dict, update: dict):
        ack = self._update_many(TypeModel.COLLECTION, filter, update)
        return ack

    @deprecated
    def count_types(self):
        return self.dbm.count(collection=TypeModel.COLLECTION)

    @deprecated
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

    @deprecated
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

    @deprecated
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

    @deprecated
    def insert_category(self, category: CategoryModel):
        """Add a new category into the database or add the children list an existing category"""
        try:
            return self._insert(collection=CategoryModel.COLLECTION, data=CategoryModel.to_json(category))
        except Exception as err:
            raise ObjectManagerInsertError(err=err)

    @deprecated
    def update_category(self, category: CategoryModel):
        """Update a existing category into the database"""
        try:
            return self._update(
                collection=CategoryModel.COLLECTION,
                public_id=category.get_public_id(),
                data=CategoryModel.to_json(category)
            )
        except Exception as err:
            raise ObjectManagerUpdateError(err=err)

    @deprecated
    def unset_update(self, collection: str, field: str):
        try:
            ack = self._unset_update_many(collection, field)
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ObjectManagerUpdateError(err)
        return ack.acknowledged

    # Link CRUD
    def get_link(self, public_id: int, user: UserModel = None, permission: AccessControlPermission = None) -> CmdbLink:
        try:
            link = CmdbLink(**self._get(collection=CmdbLink.COLLECTION, public_id=public_id))
        except (CMDBError, Exception) as err:
            raise ObjectManagerGetError(err)
        # Check permissions
        if user and permission:
            self.get_object(public_id=link.primary, user=user, permission=permission)
            self.get_object(public_id=link.secondary, user=user, permission=permission)
        return link

    def get_links_by_partner(self, public_id: int, user: UserModel) -> List[CmdbLink]:
        query = {
            '$or': [
                {'primary': public_id},
                {'secondary': public_id}
            ]
        }
        link_list: List[CmdbLink] = []
        try:
            find_list: List[dict] = self._get_many(CmdbLink.COLLECTION, **query)
            for link in find_list:
                query = {
                    '$or': [
                        {'public_id': link['primary']},
                        {'public_id': link['secondary']}
                    ]
                }
                verified_object = self.get_objects_by(user=user, permission=AccessControlPermission.READ, **query)
                if len(verified_object) == 2:
                    link_list.append(CmdbLink(**link))
        except CMDBError as err:
            raise ObjectManagerGetError(err)
        return link_list

    def insert_link(self, data: dict, user: UserModel = None, permission: AccessControlPermission = None):
        try:
            link = CmdbLink(public_id=self.get_new_id(collection=CmdbLink.COLLECTION), **data)
        except Exception as err:
            raise ObjectManagerInsertError(err)

        # Check permissions
        if user and permission:
            self.get_object(public_id=link.primary, user=user, permission=permission)
            self.get_object(public_id=link.secondary, user=user, permission=permission)
        try:
            return self._insert(CmdbLink.COLLECTION, link.__dict__)
        except Exception as err:
            raise ObjectManagerInsertError(err)

    def delete_link(self, public_id: int, user: UserModel = None, permission: AccessControlPermission = None):
        # Check permissions and existing
        self.get_link(public_id=public_id, user=user, permission=permission)
        try:
            ack = self._delete(CmdbLink.COLLECTION, public_id)
        except Exception as err:
            raise ObjectManagerDeleteError(err)
        return ack
