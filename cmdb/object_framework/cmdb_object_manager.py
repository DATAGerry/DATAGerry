"""
This manager represents the core functionalities for the use of CMDB objects.
All communication with the objects is controlled by this manager.
The implementation of the manager used is always realized using the respective superclass.

"""
from cmdb.object_framework import *
from cmdb.object_framework import CmdbObjectStatus
from cmdb.data_storage.database_manager import PublicIDAlreadyExists
from cmdb.utils.error import CMDBError
from cmdb.utils import get_logger
from cmdb.utils.helpers import timing

CMDB_LOGGER = get_logger()


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

    def _get(self, collection: str, public_id: int) -> object:
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

    def _get_all(self, collection: str, sort='public_id', **requirements: dict) -> list:
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
        return self.dbm.find_all(collection=collection, filter=requirements_filter, sort=formatted_sort)

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
        )


class CmdbObjectManager(CmdbManagerBase):
    def __init__(self, database_manager=None):
        """

        Args:
            database_manager:
        """
        super(CmdbObjectManager, self).__init__(database_manager)

    def is_ready(self) -> bool:
        return self.dbm.status()

    def search(self, search: str, exclude: str = None):
        return self.dbm.__find(CmdbObject.COLLECTION, {"$text": {"$search": search}})

    def get_highest_id(self, collection: str):
        return self.dbm.get_highest_id(collection)

    def get_object(self, public_id: int):
        """get object by public id
        Args:
            public_id:

        Returns:

        """
        return CmdbObject(
            **self._get(
                collection=CmdbObject.COLLECTION,
                public_id=public_id
            )
        )

    def get_objects(self, public_ids: list):
        object_list = []
        for public_id in public_ids:
            object_list.append(self.get_object(public_id))
        return object_list

    def get_objects_by(self, sort='public_id', **requirements: dict):
        ack = []
        objects = self._get_all(collection=CmdbObject.COLLECTION, sort=sort, **requirements)
        for obj in objects:
            ack.append(CmdbObject(**obj))
        return ack

    def get_all_objects(self):
        ack = []
        objects = self.dbm.find_all(collection=CmdbObject.COLLECTION)
        for obj in objects:
            ack.append(CmdbObject(**obj))
        return ack

    def get_objects_by_type(self, type_id: int):
        return self.get_objects_by(type_id=type_id)

    def insert_object(self, data: (CmdbObject, dict)):
        if type(data) == dict:
            try:
                new_object = CmdbObject(**data)
            except CMDBError as e:
                raise ObjectInsertError(e)
        else:
            new_object = data
            CMDB_LOGGER.debug(new_object)
        try:
            ack = self.dbm.insert(
                collection=CmdbObject.COLLECTION,
                data=new_object.to_database()
            )
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
        if type(data) == dict:
            update_object = CmdbObject(**data)
        elif type(data) == CmdbObject:
            update_object = data
        else:
            raise UpdateError(CmdbObject.__class__, data, 'Wrong CmdbObject init format - expecting CmdbObject or dict')
        ack = self.dbm.update(
            collection=CmdbObject.COLLECTION,
            public_id=update_object.get_public_id(),
            data=update_object.to_database()
        )
        return ack

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
        CMDB_LOGGER.debug("Type ID: {}".format(type_id))
        # query for all types with ref input type with value of type id
        req_type_query = {"fields": {"$elemMatch": {"input_type": "ref", "$and": [{"type_id": int(type_id)}]}}}
        CMDB_LOGGER.debug("Query: {}".format(req_type_query))
        # get type list
        req_type_list = self.dbm.find_all(collection=CmdbType.COLLECTION, filter=req_type_query)
        CMDB_LOGGER.debug("Req type list: {}".format(req_type_list))
        type_init_list = []
        for new_type_init in req_type_list:
            try:
                current_loop_type = self.get_type(new_type_init['public_id'])
                ref_field = current_loop_type.get_field_of_type_with_value(input_type='ref', _filter='type_id',
                                                                           value=type_id)
                CMDB_LOGGER.debug("Current reference field {}".format(ref_field))
                type_init_list.append(
                    {"type_id": current_loop_type.get_public_id(), "field_name": ref_field.get_name()})
            except CMDBError as e:
                CMDB_LOGGER.warning('Unsolvable type reference with type {}'.format(e.message))
                continue
        CMDB_LOGGER.debug("Init type list: {}".format(type_init_list))

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
        CMDB_LOGGER.debug("matched objects count: {}".format(len(matched_objects)))
        CMDB_LOGGER.debug("matched objects: {}".format(matched_objects))
        return matched_objects

    def delete_object(self, public_id: int):
        ack = self._delete(CmdbObject.COLLECTION, public_id)
        return ack

    def delete_many_objects(self, public_ids: list):
        ack = []
        for public_id in public_ids:
            if isinstance(public_id, CmdbObject):
                ack.append(self.delete_object(public_id.get_public_id()))
            else:
                ack.append(self.delete_object(public_id))
        return ack

    def get_all_types(self):
        ack = []
        types = self.dbm.find_all(collection=CmdbType.COLLECTION)
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

    def insert_type(self, data: dict):
        new_type = CmdbType(**data)
        return self._insert(collection=CmdbType.COLLECTION, data=new_type.to_database())

    def update_type(self, data: dict):
        update_type = CmdbType(**data)
        ack = self.dbm.update(
            collection=CmdbType.COLLECTION,
            public_id=CmdbType.get_public_id(),
            data=update_type.to_database()
        )
        return ack

    def delete_type(self, public_id: int):
        ack = self._delete(CmdbType.COLLECTION, public_id)
        return ack

    def get_all_categories(self):
        ack = []
        cats = self.dbm.find_all(collection=CmdbTypeCategory.COLLECTION, sort=[('public_id', 1)])
        for cat_obj in cats:
            try:
                ack.append(CmdbTypeCategory(**cat_obj))
            except CMDBError as e:
                CMDB_LOGGER.debug("Error while parsing Category")
                CMDB_LOGGER.debug(e.message)
        return ack

    def get_categories_by(self, _filter: dict) -> list:
        """
        get all categories by requirements
        """
        ack = []
        query_filter = _filter
        root_categories = self.dbm.find_all(collection=CmdbTypeCategory.COLLECTION, filter=query_filter)
        CMDB_LOGGER.debug("__FIND: categories {}".format(root_categories))
        for cat_obj in root_categories:
            try:
                ack.append(CmdbTypeCategory(**cat_obj))
            except CMDBError as e:
                CMDB_LOGGER.debug("Error while parsing Category")
                CMDB_LOGGER.debug(e.message)
        return ack

    def _get_category_nodes(self, parent_list: list) -> dict:
        edge = {}
        for cat_child in parent_list:
            next_children = self.get_categories_by(_filter={'parent_id': cat_child.get_public_id()})
            if len(next_children) > 0:
                edge.update({
                    'object': cat_child,
                    'children': self._get_category_nodes(next_children)
                })
            else:
                edge.update({
                    'object': cat_child,
                    'children': None
                })
        return edge

    def get_category_tree(self) -> dict:
        tree = {}
        root_categories = self.get_categories_by(_filter={'parent_id': {'$exists': False}})
        if len(root_categories) > 0:
            tree.update({
                'object': "root",
                'children': self._get_category_nodes(root_categories)
            })
        else:
            raise NoRootCategories()
        return tree

    def get_category(self, public_id: int):
        return CmdbTypeCategory(**self.dbm.find_one(
            collection=CmdbTypeCategory.COLLECTION,
            public_id=public_id)
                                )

    def insert_category(self, data: dict):
        new_category = CmdbTypeCategory(**data)
        return self._insert(collection=CmdbTypeCategory.COLLECTION, data=new_category.to_database())

    def update_category(self, data: dict):
        update_type = CmdbTypeCategory(**data)
        ack = self.dbm.update(
            collection=CmdbTypeCategory.COLLECTION,
            public_id=update_type.get_public_id(),
            data=update_type.to_database()
        )
        return ack

    def delete_category(self, public_id: int):
        ack = self._delete(CmdbTypeCategory.COLLECTION, public_id)
        return ack

    def get_status(self, public_id) -> (CmdbObjectStatus, None):
        try:
            return CmdbObjectStatus(**self.dbm.find_one(
                collection=CmdbObjectStatus.COLLECTION,
                public_id=public_id)
                                    )
        except CMDBError:
            return None

    def get_status_by_type(self, type_id: int):
        status_list = []
        for status in self.get_type(type_id).status:
            status_list.append(self.get_status(status))
        return status_list

    def generate_log_state(self, state: (list, dict)) -> str:
        from cmdb.utils.security import SecurityManager
        scm = SecurityManager(self.dbm)
        encrypted_state = scm.encrypt_aes(state)
        CMDB_LOGGER.debug("Encrypt log state: {}".format(encrypted_state))
        return encrypted_state


class UpdateError(CMDBError):
    def __init__(self, class_name, data, error):
        self.message = 'Update error while updating {} - Data: {} - Error: '.format(class_name, data, error)


class TypeNotFoundError(CMDBError):
    def __init__(self, type_id):
        self.message = 'Type with ID: {} not found!'.format(type_id)


class ObjectInsertError(CMDBError):
    def __init__(self, error):
        self.message = 'Object could not be inserted | Error {} \n show into logs for details'.format(error)


class ObjectUpdateError(CMDBError):
    def __init__(self, msg):
        self.message = 'Something went wrong during update: {}'.format(msg)


class NoRootCategories(CMDBError):
    def __init__(self):
        self.message = 'No root categories exists'