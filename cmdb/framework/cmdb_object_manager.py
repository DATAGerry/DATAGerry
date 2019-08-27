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
This manager represents the core functionalities for the use of CMDB objects.
All communication with the objects is controlled by this manager.
The implementation of the manager used is always realized using the respective superclass.

"""
import logging
import re

from cmdb.data_storage import get_pre_init_database
from cmdb.data_storage.database_manager import InsertError, PublicIDAlreadyExists
from cmdb.event_management.event import Event
from cmdb.framework import *
from cmdb.framework import CmdbStatus
from cmdb.framework.cmdb_errors import WrongInputFormatError, UpdateError, TypeInsertError, TypeAlreadyExists, \
    TypeNotFoundError, ObjectInsertError, ObjectNotFoundError, ObjectDeleteError, NoRootCategories
from cmdb.utils.error import CMDBError
from cmdb.utils.helpers import timing

LOGGER = logging.getLogger(__name__)


class CmdbManagerBase:
    """Represents the base class for object managers. A respective implementation is always adapted to the
       respective database manager :class:`cmdb.data_storage.DatabaseManager` or the used functionalities.
       But should always use at least the super functions listed here.

    """

    def __init__(self, database_manager):
        """Example:
            Depending on the condition or whether a fork process is used, the database manager can also be seen
            directly in the declaration of the object manager

        .. code-block:: python
               :linenos:

                system_config_reader = get_system_config_reader()
                object_manager = CmdbObjectManager(
                    database_manager = DatabaseManagerMongo(
                        connector=MongoConnector(
                            host=system_config_reader.get_value('host', 'Database'),
                            port=int(system_config_reader.get_value('port', 'Database')),
                            database_name=system_config_reader.get_value('database_name', 'Database'),
                            timeout=MongoConnector.DEFAULT_CONNECTION_TIMEOUT
                        )
                    )
                )

        Args:
            database_manager (DatabaseManager): initialisation of an database manager

        """
        if database_manager:
            self.dbm = database_manager

    def _get(self, collection: str, public_id: int) -> (object, dict):
        """get document from the database by their public id

        Args:
            collection (str): name of the database collection
            public_id (int): public id of the document/entry

        Returns:
            str: founded document in json format
        """
        return self.dbm.find_one(
            collection=collection,
            public_id=public_id
        )

    def _get_all(self, collection: str, sort='public_id', limit=0, **requirements: dict) -> list:
        """get all documents from the database which have the passing requirements

        Args:
            collection (str): name of the database collection
            sort (str): sort by given key - default public_id
            **requirements (dict): dictionary of key value requirement

        Returns:
            list: list of all documents

        """
        requirements_filter = {}
        formatted_sort = [(sort, self.dbm.DESCENDING)]
        for k, req in requirements.items():
            requirements_filter.update({k: req})
        return self.dbm.find_all(collection=collection, limit=limit, filter=requirements_filter, sort=formatted_sort)

    def _insert(self, collection: str, data: dict) -> (int, None):
        """insert document/object into database

        Args:
            collection (str): name of the database collection
            data (dict): dictionary of object or the data

        Returns:
            int: new public_id of inserted document
            None: if anything goes wrong

        """
        return self.dbm.insert(
            collection=collection,
            data=data
        )

    def _update(self, collection: str, public_id: int, data: dict) -> object:
        """
        update document/object in database
        Args:
            collection (str): name of the database collection
            public_id (int): public id of object
            data: changed data/object

        Returns:
            acknowledgment of database
        """
        return self.dbm.update(
            collection=collection,
            public_id=public_id,
            data=data
        )

    def _delete(self, collection: str, public_id: int):
        """
        delete document/object inside database
        Args:
            collection (str): name of the database collection
            public_id (int): public id of object

        Returns:
            acknowledgment of database
        """
        return self.dbm.delete(
            collection=collection,
            public_id=public_id
        ).acknowledged

    def _delete_many(self, collection: str, filter_query: dict):
        """
        removes all documents that match the filter from a collection.
        Args:
            collection (str): name of the database collection
            filter (dict): Specifies deletion criteria using query operators.

        Returns:
            acknowledgment of database
        """
        return self.dbm.delete_many(
            collection=collection,
            **filter_query
        )

    def _search(self, collection: str, requirements, limit=0):
        return self._get_all(collection, limit=limit, **requirements)


class CmdbObjectManager(CmdbManagerBase):
    def __init__(self, database_manager=None, event_queue=None):
        """

        Args:
            database_manager:
        """
        self._event_queue = event_queue
        super(CmdbObjectManager, self).__init__(database_manager)

    def is_ready(self) -> bool:
        return self.dbm.status()

    def get_highest_id(self, collection: str):
        return self.dbm.get_highest_id(collection)

    def get_object(self, public_id: int):
        """get object by public id
        Args:
            public_id:

        Returns:

        """
        try:
            return CmdbObject(
                **self._get(
                    collection=CmdbObject.COLLECTION,
                    public_id=public_id
                )
            )
        except (CMDBError, Exception):
            raise ObjectNotFoundError(obj_id=public_id)

    def get_objects(self, public_ids: list):
        object_list = []
        for public_id in public_ids:
            object_list.append(self.get_object(public_id))
        return object_list

    def get_objects_by(self, sort='public_id', **requirements):
        ack = []
        objects = self._get_all(collection=CmdbObject.COLLECTION, sort=sort, **requirements)
        for obj in objects:
            ack.append(CmdbObject(**obj))
        return ack

    def get_all_objects(self):
        ack = []
        objects = self._get_all(collection=CmdbObject.COLLECTION, sort='public_id')
        for obj in objects:
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
                   collection (str): name of database collection
                   public_id (int): public id of document
                   *args: arguments for search operation
                   **kwargs:

               Returns:
                   returns the count of the documents
               """

        formatted_type_id = {'type_id': public_id}
        return self.dbm.count(CmdbObject.COLLECTION, formatted_type_id)

    def count_objects(self):
        return self.dbm.count(collection=CmdbObject.COLLECTION)

    def _find_query_fields(self, query, match_fields=list()):
        for key, items in query.items():
            if isinstance(items, dict):
                if 'fields.value' == key:
                    match_fields.append(items['$regex'])
                else:
                    for item in items:
                        self._find_query_fields(item, match_fields=match_fields)
        return match_fields

    def _re_search_fields(self, search_object, regex):
        """returns list of matched fields"""
        match_list = list()
        for index in regex:
            for field in search_object.fields:
                if re.search(index, str(field['value'])):
                    match_list.append(field['name'])
        return match_list

    def search_objects(self, query: dict) -> dict:
        return self.search_objects_with_limit(query, limit=0)

    def search_objects_with_limit(self, query: dict, limit=0) -> dict:
        result_list = dict()
        for result_objects in self._search(CmdbObject.COLLECTION, query, limit=limit):
            try:
                re_query = self._find_query_fields(query)
                result_object_instance = CmdbObject(**result_objects)
                matched_fields = self._re_search_fields(result_object_instance, re_query)

                result_list.update({
                    result_object_instance: matched_fields
                })
            except (CMDBError, re.error):
                continue
        return result_list

    def insert_object(self, data: (CmdbObject, dict)):
        if isinstance(data, dict):
            try:
                new_object = CmdbObject(**data)
            except CMDBError as e:
                raise ObjectInsertError(e)
        elif isinstance(data, CmdbObject):
            new_object = data
        try:
            ack = self.dbm.insert(
                collection=CmdbObject.COLLECTION,
                data=new_object.to_database()
            )
            # create cmdb.core.object.added event
            if self._event_queue:
                event = Event("cmdb.core.object.added", {"id": new_object.get_public_id()})
                self._event_queue.put(event)
        except (CMDBError, PublicIDAlreadyExists) as e:
            raise ObjectInsertError(e)
        return ack

    def insert_many_objects(self, objects: list):
        ack = []
        for obj in objects:
            if isinstance(obj, CmdbObject):
                ack.append(self.insert_object(obj.to_database()))
            elif isinstance(obj, dict):
                ack.append(self.insert_object(obj))
            else:
                raise Exception
        return ack

    def update_object(self, data: (dict, CmdbObject)) -> str:
        if isinstance(data, dict):
            update_object = CmdbObject(**data)
        elif isinstance(data, CmdbObject):
            update_object = data
        else:
            raise UpdateError(CmdbObject.__class__, data, 'Wrong CmdbObject init format - expecting CmdbObject or dict')
        ack = self.dbm.update(
            collection=CmdbObject.COLLECTION,
            public_id=update_object.get_public_id(),
            data=update_object.to_database()
        )
        # create cmdb.core.object.updated event
        if self._event_queue:
            event = Event("cmdb.core.object.updated", {"id": update_object.get_public_id()})
            self._event_queue.put(event)
        return ack.acknowledged

    def update_many_objects(self, objects: list):
        ack = []
        for obj in objects:
            if isinstance(obj, CmdbObject):
                ack.append(self.update_object(obj.to_database()))
            elif isinstance(obj, dict):
                ack.append(self.update_object(obj))
            else:
                raise Exception
        return ack

    @timing("Object references loading time took ")
    def get_object_references(self, public_id: int) -> list:
        # Type of given object id
        type_id = self.get_object(public_id=public_id).get_type_id()
        LOGGER.debug("Type ID: {}".format(type_id))
        # query for all types with ref input type with value of type id
        req_type_query = {"fields": {"$elemMatch": {"input_type": "ref", "$and": [{"type_id": int(type_id)}]}}}
        LOGGER.debug("Query: {}".format(req_type_query))
        # get type list
        req_type_list = self.dbm.find_all(collection=CmdbType.COLLECTION, filter=req_type_query)
        LOGGER.debug("Req type list: {}".format(req_type_list))
        type_init_list = []
        for new_type_init in req_type_list:
            try:
                current_loop_type = self.get_type(new_type_init['public_id'])
                ref_field = current_loop_type.get_field_of_type_with_value(input_type='ref', _filter='type_id',
                                                                           value=type_id)
                LOGGER.debug("Current reference field {}".format(ref_field))
                type_init_list.append(
                    {"type_id": current_loop_type.get_public_id(), "field_name": ref_field.get_name()})
            except CMDBError as e:
                LOGGER.warning('Unsolvable type reference with type {}'.format(e.message))
                continue
        LOGGER.debug("Init type list: {}".format(type_init_list))

        referenced_by_objects = []
        for possible_object_types in type_init_list:
            referenced_query = {"type_id": possible_object_types['type_id'], "fields": {
                "$elemMatch": {"$and": [{"name": possible_object_types['field_name']}],
                               "$or": [{"value": int(public_id)}]}}}
            referenced_by_objects = referenced_by_objects + self.dbm.find_all(collection=CmdbObject.COLLECTION,
                                                                              filter=referenced_query)
        matched_objects = []
        for matched_object in referenced_by_objects:
            matched_objects.append(CmdbObject(
                **matched_object
            ))
        LOGGER.debug("matched objects count: {}".format(len(matched_objects)))
        LOGGER.debug("matched objects: {}".format(matched_objects))
        return matched_objects

    def delete_object(self, public_id: int):
        try:
            ack = self._delete(CmdbObject.COLLECTION, public_id)
            return ack
        except (CMDBError, Exception):
            raise ObjectDeleteError(obj_id=public_id)

    def delete_many_objects(self, public_ids: dict):
        ack = self._delete_many(CmdbObject.COLLECTION, public_ids)
        return ack

    def get_all_types(self):
        ack = []
        types = self._get_all(collection=CmdbType.COLLECTION)
        for type_obj in types:
            ack.append(CmdbType(**type_obj))
        return ack

    def get_type(self, public_id: int):
        try:
            return CmdbType(**self.dbm.find_one(
                collection=CmdbType.COLLECTION,
                public_id=public_id)
                            )
        except (CMDBError, Exception):
            raise TypeNotFoundError(type_id=public_id)

    def get_types_by(self, sort='public_id', **requirements):
        ack = []
        objects = self._get_all(collection=CmdbType.COLLECTION, sort=sort, **requirements)
        for data in objects:
            ack.append(CmdbType(**data))
        return ack

    def insert_type(self, data: (CmdbType, dict)):
        if isinstance(data, CmdbType):
            new_type = data
        elif isinstance(data, dict):
            new_type = CmdbType(**data)
        else:
            raise WrongInputFormatError(CmdbType, data, "Possible data: dict or CmdbType")
        try:
            ack = self._insert(collection=CmdbType.COLLECTION, data=new_type.to_database())
            LOGGER.debug(f"Inserted new type with ack {ack}")
        except PublicIDAlreadyExists:
            raise TypeAlreadyExists(type_id=new_type.get_public_id())
        except (CMDBError, InsertError):
            raise TypeInsertError(new_type.get_public_id())
        return ack

    def update_type(self, data: (CmdbType, dict)):
        if isinstance(data, CmdbType):
            update_type = data
        elif isinstance(data, dict):
            update_type = CmdbType(**data)
        else:
            raise WrongInputFormatError(CmdbType, data, "Possible data: dict or CmdbType")

        ack = self._update(
            collection=CmdbType.COLLECTION,
            public_id=update_type.get_public_id(),
            data=update_type.to_database()
        )
        return ack

    def count_types(self):
        return self.dbm.count(collection=CmdbType.COLLECTION)

    def delete_type(self, public_id: int):
        ack = self._delete(CmdbType.COLLECTION, public_id)
        return ack

    def delete_many_types(self, public_ids: dict):
        ack = self._delete_many(CmdbType.COLLECTION, public_ids)
        return ack

    def get_all_categories(self):
        ack = []
        cats = self.dbm.find_all(collection=CmdbCategory.COLLECTION, sort=[('public_id', 1)])
        for cat_obj in cats:
            try:
                ack.append(CmdbCategory(**cat_obj))
            except CMDBError as e:
                LOGGER.debug("Error while parsing Category")
                LOGGER.debug(e.message)
        return ack

    def get_categories_by(self, _filter: dict) -> list:
        """
        get all categories by requirements
        """
        ack = []
        query_filter = _filter
        root_categories = self.dbm.find_all(collection=CmdbCategory.COLLECTION, filter=query_filter)
        for cat_obj in root_categories:
            try:
                ack.append(CmdbCategory(**cat_obj))
            except CMDBError as e:
                LOGGER.debug("Error while parsing Category")
                LOGGER.debug(e.message)
        return ack

    def _get_category_nodes(self, parent_list: list) -> dict:
        edge = []
        for cat_child in parent_list:
            next_children = self.get_categories_by(_filter={'parent_id': cat_child.get_public_id()})
            if len(next_children) > 0:
                edge.append({
                    'category': cat_child,
                    'children': self._get_category_nodes(next_children)
                })
            else:
                edge.append({
                    'category': cat_child,
                    'children': None
                })
        return edge

    def get_category_tree(self) -> dict:
        tree = list()
        root_categories = self.get_categories_by(_filter={
            '$or': [
                {'parent_id': {'$exists': False}},
                {'parent_id': None}
            ]
        })
        if len(root_categories) > 0:
            tree = self._get_category_nodes(root_categories)
        else:
            raise NoRootCategories()
        return tree

    def get_category(self, public_id: int):
        return CmdbCategory(**self.dbm.find_one(
            collection=CmdbCategory.COLLECTION,
            public_id=public_id)
                            )

    def insert_category(self, data: (CmdbCategory, dict)):
        if isinstance(data, CmdbCategory):
            new_category = data
        elif isinstance(data, dict):
            new_category = CmdbCategory(**data)

        return self._insert(collection=CmdbCategory.COLLECTION, data=new_category.to_database())

    def update_category(self, data: (CmdbCategory, dict)):
        if isinstance(data, CmdbCategory):
            update_category = data
        elif isinstance(data, dict):
            update_category = CmdbCategory(**data)
        ack = self.dbm.update(
            collection=CmdbCategory.COLLECTION,
            public_id=update_category.get_public_id() or update_category.public_id,
            data=update_category.to_database()
        )
        return ack

    def delete_category(self, public_id: int):
        ack = self._delete(CmdbCategory.COLLECTION, public_id)
        return ack

    # STATUS CRUD
    def get_statuses(self) -> list:
        status_list = list()
        try:
            collection_resp = self.dbm.find_all(collection=CmdbStatus.COLLECTION)
        except(CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ObjectManagerGetError(err)

        for collection in collection_resp:
            try:
                status_list.append(CmdbStatus(
                    **collection
                ))
            except(CMDBError, Exception) as err:
                LOGGER.error(err)
                continue
        return status_list

    def get_status(self, public_id) -> CmdbStatus:
        try:
            return CmdbStatus(**self.dbm.find_one(
                collection=CmdbStatus.COLLECTION,
                public_id=public_id
            ))
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ObjectManagerGetError(err)

    def insert_status(self, data) -> int:
        try:
            new_status = CmdbStatus(**data)
            ack = self.dbm.insert(CmdbStatus.COLLECTION, new_status.to_database())
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ObjectManagerInsertError(err)
        return ack

    def update_status(self, data):
        try:
            updated_status = CmdbStatus(**data)
            ack = self.dbm.update(CmdbStatus.COLLECTION, updated_status.get_public_id(), updated_status.to_database())
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ObjectManagerUpdateError(err)
        return ack.acknowledged

    def delete_status(self, public_id: int):
        return NotImplementedError

    # COLLECTIONS/TEMPLATES CRUD

    def get_collections(self) -> list:
        collection_list = list()
        try:
            collection_resp = self.dbm.find_all(collection=CmdbCollection.COLLECTION)
        except(CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ObjectManagerGetError(err)

        for collection in collection_resp:
            try:
                collection_list.append(CmdbCollection(
                    **collection
                ))
            except(CMDBError, Exception) as err:
                LOGGER.error(err)
                continue
        return collection_list

    def get_collection(self, public_id: int) -> CmdbCollection:
        try:
            return CmdbCollection(**self.dbm.find_one(
                collection=CmdbCollection.COLLECTION,
                public_id=public_id
            ))
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ObjectManagerGetError(err)

    def insert_collection(self, data) -> int:
        try:
            new_collection = CmdbCollection(**data)
            ack = self.dbm.insert(CmdbCollection.COLLECTION, new_collection.to_database())
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ObjectManagerInsertError(err)
        return ack

    def update_collection(self, data):
        return NotImplementedError

    def delete_collection(self, public_id: int):
        return NotImplementedError

    def get_collection_templates(self) -> list:
        collection_template_list = list()
        try:
            collection_resp = self.dbm.find_all(collection=CmdbCollectionTemplate.COLLECTION)
        except(CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ObjectManagerGetError(err)

        for collection in collection_resp:
            try:
                collection_template_list.append(CmdbCollectionTemplate(
                    **collection
                ))
            except(CMDBError, Exception) as err:
                LOGGER.error(err)
                continue
        return collection_template_list

    def get_collection_template(self, public_id: int) -> CmdbCollectionTemplate:
        try:
            return CmdbCollectionTemplate(**self.dbm.find_one(
                collection=CmdbCollectionTemplate.COLLECTION,
                public_id=public_id
            ))
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ObjectManagerGetError(err)

    def insert_collection_template(self, data) -> int:
        try:
            new_collection_template = CmdbCollectionTemplate(**data)
            ack = self.dbm.insert(CmdbCollectionTemplate.COLLECTION, new_collection_template.to_database())
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ObjectManagerInsertError(err)
        return ack

    def update_collection_template(self, data):
        return NotImplementedError

    def delete_collection_template(self, public_id: int):
        return NotImplementedError

    # Link CRUDS

    def get_links_by_partner(self, public_id: int):
        return NotImplementedError

    def insert_link(self, data):
        try:
            new_link = CmdbLink(**data)
            ack = self.dbm.insert(CmdbLink.COLLECTION, new_link.to_database())
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise ObjectManagerInsertError(err)
        return ack


class ObjectManagerGetError(CMDBError):

    def __init__(self, err):
        self.message = f'Error while GET operation - E: ${err}'


class ObjectManagerInsertError(CMDBError):

    def __init__(self, err):
        self.message = f'Error while INSERT operation - E: ${err}'


class ObjectManagerUpdateError(CMDBError):

    def __init__(self, err):
        self.message = f'Error while UPDATE operation - E: ${err}'


class ObjectManagerDeleteError(CMDBError):

    def __init__(self, err):
        self.message = f'Error while DELETE operation - E: ${err}'


object_manager = CmdbObjectManager(
    database_manager=get_pre_init_database(),
    event_queue=None
)
