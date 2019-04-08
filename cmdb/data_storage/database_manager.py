"""
Database Management instance for database actions

"""
import logging
from pymongo.errors import DuplicateKeyError
from pymongo.results import DeleteResult
from cmdb.data_storage.database_connection import Connector
from cmdb.utils.error import CMDBError
from cmdb.data_storage.database_connection import MongoConnector

LOGGER = logging.getLogger(__name__)


class DatabaseManager:
    """
    Default database manager with no implementation

    """

    DB_MANAGER_TYPE = 'base'
    DEFAULT_DATABASE_NAME = 'cmdb'
    ASCENDING = 1
    DESCENDING = -1

    def __init__(self, connector: Connector):
        """instance of super class

        Args:
            connector (Connector): Database Connector for subclass implementation

        """

        self.database_connector = connector

    def status(self):
        """check if connector has connection

        Returns: connection status

        """
        return self.database_connector.is_connected()

    def setup(self):
        """
        setup script for database init
        """
        raise NotImplementedError

    def _import(self, *args, **kwargs):
        raise NotImplementedError

    def __find(self, *args, **kwargs):
        """general find function for database search

        Args:
            *args: arguments for search operation
            **kwargs:

        Returns:
            str: founded document

        """

        raise NotImplementedError

    def find_one_by(self, *args, **kwargs):
        """
        find only one document by requirement
        Args:
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            str: founded document

        """

        raise NotImplementedError

    def find_one(self, *args, **kwargs):
        """calls __find with single return

        Args:
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            founded document

        """

        raise NotImplementedError

    def find_all(self, *args, **kwargs):
        """calls __find with all returns

        Args:
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            list: list of founded documents

        """

        raise NotImplementedError

    def insert(self, *args, **kwargs):
        """adds document to database

        Args:
            *args: object data
            **kwargs: dict of data

        Returns:
            int: public id of inserted document

        """

        raise NotImplementedError

    def update(self, *args, **kwargs):
        """update document inside database

        Args:
            *args: object data
            **kwargs: dict of data

        Returns:
            acknowledged

        """

        raise NotImplementedError

    def delete(self, *args, **kwargs):
        """delete document inside database

        Args:
            *args: public id
            **kwargs: dict of public id

        Returns:
            acknowledged

        """

        raise NotImplementedError

    def create(self, db_name):
        """create new database

        Args:
            db_name (str): name of database

        Returns:
            acknowledged

        """

        raise NotImplementedError

    def drop(self, db_name: str):
        """delete database

        Args:
            db_name (str): name of database

        Returns:
            acknowledged

        """
        raise NotImplementedError

    def get_database_name(self):
        """get name of selected database

        Returns:
            db_name (str): name of database
        """
        raise NotImplementedError


class DatabaseManagerMongo(DatabaseManager):
    """PyMongo (mongodb) implementation of Database Manager"""

    DB_MANAGER_TYPE = 'MONGO_DB'

    def __init__(self, connector: MongoConnector):
        """init mongo implementation

        Args:
            connector: mongodb connector

        """
        self.database_connector = connector
        super().__init__(connector)

    def setup(self) -> bool:
        """setup script

        Returns:
            acknowledged

        """
        from cmdb.object_framework import __COLLECTIONS__ as cmdb_collection
        from cmdb.user_management import __COLLECTIONS__ as user_collection
        collection = cmdb_collection + user_collection

        def _gen_default_tables(collection_class: object):
            self.create_collection(collection_class.COLLECTION)
            self.create_indexes(collection_class.COLLECTION, collection_class._SUPER_INDEX_KEYS)
            if len(collection_class.INDEX_KEYS) > 0:
                self.create_indexes(collection_class.COLLECTION, collection_class.INDEX_KEYS)

        for coll in collection:
            # generating the default database "tables"
            try:
                _gen_default_tables(coll)
            except Exception:
                return False
        return True

    def _import(self, collection: str, data_list: list):
        LOGGER.debug(data_list)
        try:
            self.delete_collection(collection)
        except Exception as e:
            LOGGER.debug(e)
        for import_data in data_list:
            try:
                self.insert(collection=collection, data=import_data)
            except (Exception, CMDBError) as e:
                LOGGER.debug(e)
                LOGGER.debug("IMPORT ERROR: {}".format(e))
                return False
        return True

    def create_index(self, collection: str, name: str, unique: bool, background=True):
        self.database_connector.get_collection(collection).create_index(
            name=name,
            unique=unique,
            background=background
        )

    def create_indexes(self, collection: str, indexes: list):
        from pymongo import IndexModel
        import_list = []
        for idx in indexes:
            import_list.append(IndexModel(idx['keys']))
        self.database_connector.get_collection(collection).create_indexes(import_list)

    def get_database_name(self):
        return self.database_connector.get_database_name()

    def __find(self, collection: str, *args, **kwargs):
        """general find function for database search

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            founded document

        """
        result = self.database_connector.get_collection(collection).find(*args, **kwargs)
        return result

    def find_one(self, collection: str, public_id: int, *args, **kwargs):
        """calls __find with single return

        Args:
            collection (str): name of database collection
            public_id (int): public id of document
            *args: arguments for search operation
            **kwargs:

        Returns:
            founded document

        """

        formatted_public_id = {'public_id': public_id}
        formatted_sort = [('public_id', DatabaseManager.DESCENDING)]
        cursor_result = self.__find(collection, formatted_public_id, limit=1, sort=formatted_sort, *args, **kwargs)
        for result in cursor_result:
            return result
        raise NoDocumentFound(collection, public_id)

    def find_one_by(self, collection: str, *args, **kwargs) -> dict:
        """find one specific document by special requirements

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            founded document

        """

        cursor_result = self.__find(collection, limit=1, *args, **kwargs)
        for result in cursor_result.limit(-1):
            return result
        raise NoDocumentFound(collection, args)

    def find_all(self, collection, *args, **kwargs) -> list:
        """calls __find with all returns

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            list: list of founded documents

        """

        return list(self.__find(collection=collection, *args, **kwargs))

    def insert(self, collection: str, data: dict) -> int:
        """adds document to database

        Args:
            collection (str): name of database collection
            data (str): insert data

        Returns:
            int: new public id of the document
            None: if anything goes wrong while inserting
        """
        result = None
        try:
            self.find_one(collection=collection, public_id=data['public_id'])
        except NoDocumentFound:
            try:
                result = self.database_connector.get_collection(collection).insert_one(data)
            except Exception as e:
                raise InsertError(e)
            if result.acknowledged:
                formatted_id = {'_id': result.inserted_id}
                projection = {'public_id': 1}
                cursor_result = self.__find(collection, formatted_id, projection, limit=1)
                for result in cursor_result.limit(-1):
                    return result['public_id']
            return result
        else:
            raise PublicIDAlreadyExists(public_id=data['public_id'])

    def update(self, collection: str, public_id: int, data: dict):
        """update document inside database

        Args:
            collection (str): name of database collection
            public_id (int): public id of document
            data: data to update

        Returns:
            acknowledged

        """

        formatted_public_id = {'public_id': public_id}
        formatted_data = {'$set': data}
        return self.database_connector.get_collection(collection).update_one(formatted_public_id, formatted_data)

    def insert_with_internal(self, collection: str, _id: int or str, data: dict):
        formatted_id = {'_id': _id}
        formatted_data = {'$set': data}
        return self.database_connector.get_collection(collection).insert_one(formatted_id, formatted_data)

    def update_with_internal(self, collection: str, _id: int or str, data: dict):
        """update function for database elements without public id

        Args:
            collection (str): name of database collection
            _id (int): mongodb id of document
            data: data to update

        Returns:
            acknowledged

        """

        formatted_id = {'_id': _id}
        formatted_data = {'$set': data}
        return self.database_connector.get_collection(collection).update_one(formatted_id, formatted_data)

    def delete(self, collection: str, public_id: int) -> DeleteResult:
        """delete document inside database

        Args:
            collection (str): name of database collection
            public_id (int): public id of document

        Returns:
            acknowledged

        """

        formatted_public_id = {'public_id': public_id}
        result = self.database_connector.get_collection(collection).delete_one(formatted_public_id)
        if result.deleted_count != 1:
            raise DocumentCouldNotBeDeleted(collection, public_id)
        return result

    def create(self, db_name: str):
        """create database/collection

        Args:
            db_name (str): name of database

        Returns:
            acknowledge of operation

        """

        return self.database_connector.client[db_name]

    def drop(self, db_name: str):
        """delete database

        Args:
            db_name (str): name of database

        Returns:
            acknowledge

        """

        return self.database_connector.client.drop_database(db_name)

    def create_collection(self, collection_name):
        """
        Creation empty MongoDB collection
        Args:
            collection_name: name of collectio

        Returns:
            collection name
        """
        from pymongo.errors import CollectionInvalid

        try:
            self.database_connector.create_collection(collection_name)
        except CollectionInvalid:
            raise CollectionAlreadyExists(collection_name)
        return collection_name

    def delete_collection(self, collection_name):
        """
        Delete MongoDB collection
        Args:
            collection_name: collection name

        Returns:
            delete ack
        """
        return self.database_connector.delete_collection(collection_name)

    def get_document_with_highest_id(self, collection: str) -> str:
        """get the document with the highest public id inside a collection

        Args:
            collection (str): name of database collection

        Returns:
            str: document from database
        """
        formatted_sort = [('public_id', self.DESCENDING)]
        return self.find_one_by(collection=collection, sort=formatted_sort)

    def get_highest_id(self, collection: str) -> int:
        """wrapper function
        calls get_document_with_highest_id() and returns the public_id

        Args:
            collection (str): name of database collection

        Returns:
            int: highest public id

        """
        try:
            highest = int(self.get_document_with_highest_id(collection)['public_id'])
        except NoDocumentFound:
            return 0
        return highest


class InsertError(CMDBError):

    def __init__(self, error):
        super().__init__()
        self.message = "Insert error {}".format(error)


class CollectionAlreadyExists(CMDBError):
    """
    Creation error if collection already exists
    """

    def __init__(self, collection_name):
        super().__init__()
        self.message = "Collection {} already exists".format(collection_name)


class FileImportError(CMDBError):
    """
    Error if json file import to database failed
    """

    def __init__(self, collection_name):
        super().__init__()
        self.message = "Collection {} could not be imported".format(collection_name)


class PublicIDAlreadyExists(DuplicateKeyError):
    """
    Error if public_id inside database already exists
    """

    def __init__(self, public_id):
        super().__init__("Public ID Exists")
        self.message = "Object with this public id already exists: {}".format(public_id)


class NoDocumentFound(CMDBError):
    """
    Error if no document was found
    """

    def __init__(self, collection, public_id):
        super().__init__()
        self.message = "No document with the id {} was found inside {}".format(public_id, collection)


class DocumentCouldNotBeDeleted(CMDBError):
    """
    Error if document could not be deleted from database
    """

    def __init__(self, collection, public_id):
        super().__init__()
        self.message = "The document with the id {} could not be deleted inside {}".format(public_id, collection)
