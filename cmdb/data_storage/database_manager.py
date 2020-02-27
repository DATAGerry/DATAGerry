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
Database Management instance for database actions

"""
import logging
from typing import Generic

from pymongo.errors import DuplicateKeyError
from pymongo.results import DeleteResult, UpdateResult

from cmdb.data_storage import CONNECTOR
from cmdb.data_storage.database_connection import MongoConnector
from cmdb.data_storage.database_framework_counter import IDCounter
from cmdb.utils.error import CMDBError
from cmdb.utils.wraps import deprecated

LOGGER = logging.getLogger(__name__)


class DatabaseManager(Generic[CONNECTOR]):
    """
    Default database manager with no implementation

    """

    DB_MANAGER_TYPE = 'base'
    DEFAULT_DATABASE_NAME = 'cmdb'
    ASCENDING = 1
    DESCENDING = -1

    def __init__(self, connector: CONNECTOR):
        """instance of super class

        Args:
            connector (CONNECTOR): Database Connector for subclass implementation

        """

        self.connector: CONNECTOR = connector

    def get_connector(self) -> CONNECTOR:
        return self.connector

    def status(self):
        """check if connector has connection

        Returns: connection status

        """
        return self.connector.is_connected()

    def setup(self):
        """
        setup script for database init
        """
        raise NotImplementedError

    def search(self, *args, **kwargs):
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
        """find only one document by requirement

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


class DatabaseManagerMongo(DatabaseManager[MongoConnector]):
    """PyMongo (mongodb) implementation of Database Manager"""

    DB_MANAGER_TYPE = 'MONGO_DB'

    def __init__(self, host: str, port: int, database_name: str, **kwargs):
        connector = MongoConnector(host, port, database_name, **kwargs)
        super(DatabaseManagerMongo, self).__init__(connector)

    def setup(self) -> bool:
        """setup script

        Returns:
            acknowledged

        """
        from cmdb.framework import __COLLECTIONS__ as cmdb_collection
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
        self.connector.get_collection(collection).create_index(
            name=name,
            unique=unique,
            background=background
        )

    def create_indexes(self, collection: str, indexes: list):
        self.connector.get_collection(collection).create_indexes(indexes)

    def get_index_info(self, collection: str):
        """get the max index value"""
        return self.connector.get_collection(collection).index_information()

    def get_database_name(self):
        return self.connector.get_database_name()

    def __find(self, collection: str, *args, **kwargs):
        """general find function for database search

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            founded document
        """
        if 'projection' not in kwargs:
            kwargs.update({'projection': {'_id': 0}})
        result = self.connector.get_collection(collection).find(*args, **kwargs)
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
        founded_documents = self.__find(collection=collection, *args, **kwargs)
        return list(founded_documents)

    def count(self, collection: str, *args, **kwargs):
        """This method does not actually
        performs the find() operation
        but instead returns
        a numerical count of the documents that meet the selection criteria.

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs:

        Returns:
            returns the count of the documents
        """
        result = self._count(collection, *args, **kwargs)
        return result

    def _count(self, collection: str, *args, **kwargs):
        """general find function for database search

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            count document

        """
        result = self.connector.get_collection(collection).count(*args, **kwargs)
        return result

    def aggregate(self, collection: str, *args, **kwargs):
        """This method does not actually
           performs the find() operation
           but instead Aggregation operations process data records and return computed results.

           Args:
               collection (str): name of database collection
               *args: arguments for search operation
               **kwargs: key arguments
           Returns:
               returns computed results
           """
        result = self.connector.get_collection(collection).aggregate(*args, **kwargs)
        return result

    def insert(self, collection: str, data: dict) -> int:
        """adds document to database

        Args:
            collection (str): name of database collection
            data (str): insert data

        Returns:
            int: new public id of the document
        """
        if 'public_id' not in data:
            data['public_id'] = self.get_highest_id(collection=collection) + 1
        self.connector.get_collection(collection).insert_one(data)
        return data['public_id']

    def update(self, collection: str, filter: dict, data: dict, *args, **kwargs):
        """update document inside database

        Args:
            collection (str): name of database collection
            filter (dict): filter of document
            data: data to update

        Returns:
            acknowledged
        """
        formatted_data = {'$set': data}
        return self.connector.get_collection(collection).update_one(filter, formatted_data, *args, **kwargs)

    def unset_update_many(self, collection: str, filter: dict, data: str, *args, **kwargs):
        """update document inside database

        Args:
            collection (str): name of database collection
            filter (dict): filter of document
            data: data to delete

        Returns:
            acknowledged
        """
        formatted_data = {'$unset': {data: 1}}
        return self.connector.get_collection(collection).update_many(filter, formatted_data, *args, **kwargs)

    def update_many(self, collection: str, query: dict, update: dict) -> UpdateResult:
        """update all documents that match the filter from a collection.

        Args:
            collection (str): name of database collection
            query (dict): A query that matches the documents to update.
            update (dict): The modifications to apply.

        Returns:
            A boolean acknowledged as true if the operation ran with write concern or false if write concern was disabled

        """
        result = self.connector.get_collection(collection).update_many(filter=query, update=update)
        if not result.acknowledged:
            raise DocumentCouldNotBeDeleted(collection)
        return result

    def insert_with_internal(self, collection: str, _id: int or str, data: dict):
        formatted_id = {'_id': _id}
        formatted_data = {'$set': data}
        return self.connector.get_collection(collection).insert_one(formatted_id, formatted_data)

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
        return self.connector.get_collection(collection).update_one(formatted_id, formatted_data)

    def delete(self, collection: str, public_id: int) -> DeleteResult:
        """delete document inside database

        Args:
            collection (str): name of database collection
            public_id (int): public id of document

        Returns:
            acknowledged

        """

        formatted_public_id = {'public_id': public_id}
        result = self.connector.get_collection(collection).delete_one(formatted_public_id)
        if result.deleted_count != 1:
            raise DocumentCouldNotBeDeleted(collection, public_id)
        return result

    def delete_many(self, collection: str, **requirements: dict) -> DeleteResult:
        """removes all documents that match the filter from a collection.

        Args:
            collection (str): name of database collection
            filter (dict): Specifies deletion criteria using query operators.

        Returns:
            A boolean acknowledged as true if the operation ran with write concern or false if write concern was disabled

        """
        requirements_filter = {}
        for k, req in requirements.items():
            requirements_filter.update({k: req})

        result = self.connector.get_collection(collection).delete_many(requirements_filter)
        if not result.acknowledged:
            raise DocumentCouldNotBeDeleted(collection)
        return result

    def create(self, db_name: str):
        """create database

        Args:
            db_name (str): name of database

        Returns:
            acknowledge of operation

        """

        return self.connector.client[db_name]

    def drop(self, db_name: str):
        """delete database

        Args:
            db_name (str): name of database

        Returns:
            acknowledge

        """

        return self.connector.client.drop_database(db_name)

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
            self.connector.create_collection(collection_name)
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
        return self.connector.delete_collection(collection_name)

    @deprecated
    def get_document_with_highest_id(self, collection: str) -> str:
        """get the document with the highest public id inside a collection

        Args:
            collection (str): name of database collection

        Returns:
            str: document from database
        """
        formatted_sort = [('public_id', self.DESCENDING)]
        return self.find_one_by(collection=collection, sort=formatted_sort)

    @deprecated
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

    def get_next_public_id(self, collection: str) -> int:
        try:
            founded_counter = self.connector.get_collection(IDCounter.COLLECTION).find_one(filter={
                '_id': collection
            })
            new_id = founded_counter['counter'] + 1
        except (NoDocumentFound, Exception) as err:
            LOGGER.error(err)

            LOGGER.warning(f'Counter for collection {collection} wasn´t found - setup new with data from {collection}')
            docs_count = self.get_highest_id(collection)
            self.connector.get_collection(IDCounter.COLLECTION).insert({
                '_id': collection,
                'counter': docs_count
            })
            new_id = docs_count + 1
        finally:
            self._update_public_id_counter(collection)
        return new_id

    def _update_public_id_counter(self, collection: str):
        working_collection = self.connector.get_collection(IDCounter.COLLECTION)
        query = {
            '_id': collection
        }
        counter_doc = working_collection.find_one(query)
        counter_doc['counter'] = counter_doc['counter'] + 1
        self.connector.get_collection(IDCounter.COLLECTION).update(query, counter_doc)


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
