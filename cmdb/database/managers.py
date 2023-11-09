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
Database Management instance for database actions
"""
import logging
from typing import Generic, List

from pymongo import IndexModel
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult
from gridfs import GridFS

from cmdb.database import CONNECTOR
from cmdb.database.connection import MongoConnector
from cmdb.database.counter import PublicIDCounter
from cmdb.database.errors.database_errors import CollectionAlreadyExists, \
                                                 NoDocumentFound, \
                                                 DocumentCouldNotBeDeleted, \
                                                 DatabaseAlreadyExists, \
                                                 DatabaseNotExists
from cmdb.database.utils import DESCENDING


LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                             DatabaseManager - BASE CLASS                                             #
# -------------------------------------------------------------------------------------------------------------------- #

class DatabaseManager(Generic[CONNECTOR]):
    """
    Base database manager
    """

    def __init__(self, connector: CONNECTOR):
        """Constructor of `DatabaseManager`
        Args:
            connector (CONNECTOR): Database Connector for subclass implementation
        """
        self.connector: CONNECTOR = connector


    def create_database(self, *args, **kwargs):
        """Create a new empty database."""
        raise NotImplementedError


    def drop_database(self, *args, **kwargs):
        """Drop a existing database."""
        raise NotImplementedError


    def status(self):
        """Check if connector has connection."""
        return self.connector.is_connected()


    def setup(self):
        """Setup script for database init."""
        raise NotImplementedError


    def count(self, *args, **kwargs):
        """General count method."""
        raise NotImplementedError


    def aggregate(self, *args, **kwargs):
        """General count method."""
        raise NotImplementedError


    def find(self, *args, **kwargs):
        """Find resource by requirements."""
        raise NotImplementedError


    def insert(self, *args, **kwargs):
        """Insert resource to database."""
        raise NotImplementedError


    def update(self, *args, **kwargs):
        """Update resource inside database."""
        raise NotImplementedError


    def delete(self, *args, **kwargs):
        """Delete resource inside database."""
        raise NotImplementedError

# -------------------------------------------------------------------------------------------------------------------- #
#                                             DatabaseManagerMongo - CLASS                                             #
# -------------------------------------------------------------------------------------------------------------------- #

class DatabaseManagerMongo(DatabaseManager[MongoConnector]):
    """PyMongo (mongodb) implementation of Database Manager"""

    def __init__(self, host: str, port: int, database_name: str, **kwargs):
        connector = MongoConnector(host, port, database_name, kwargs)
        super().__init__(connector)


    def setup(self) -> bool:
        """
        Setup script

        Returns:
            acknowledged
        """
        from cmdb.framework import __COLLECTIONS__ as FRAMEWORK_COLLECTIONS
        from cmdb.user_management import __COLLECTIONS__ as USER_MANAGEMENT_COLLECTIONS
        collection = FRAMEWORK_COLLECTIONS + USER_MANAGEMENT_COLLECTIONS

        def _gen_default_tables(collection_class):
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


    def __exit__(self, exc_type, exc_val, exc_tb):
        """Auto disconnect the database connection when the Manager get destroyed"""
        self.connector.disconnect()


    def create_indexes(self, collection: str, indexes: List[IndexModel]) -> List[str]:
        """Creates indexes for collection"""
        return self.connector.get_collection(collection).create_indexes(indexes)


    def get_index_info(self, collection: str):
        """get the max index value"""
        return self.connector.get_collection(collection).index_information()


    def __find(self, collection: str, *args, **kwargs):
        """general find function for database search

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            found document
        """
        if 'projection' not in kwargs:
            kwargs.update({'projection': {'_id': 0}})

        return self.connector.get_collection(collection).find(*args, **kwargs)


    def find(self, collection: str, *args, **kwargs):
        """General find function"""
        return self.connector.get_collection(collection).find(*args, **kwargs)


    def count_documents(self, collection: str, *args, **kwargs):
        """
        Returns the number of documents

        Args:
            collection (str): name of collection

        Returns:
            int: Number of documents
        """
        return  self.connector.get_collection(collection).count_documents(*args, **kwargs)


    def find_one(self, collection: str, public_id: int, *args, **kwargs):
        """
        Retrieves a single document with the given public_id from the given collection 

        Args:
            collection (str): name of database collection
            public_id (int): public_id of document
            *args: arguments for search operation
            **kwargs:

        Returns:
            document with given public_id
        """
        cursor_result = self.__find(collection, {'public_id': public_id}, limit=1, *args, **kwargs)
        for result in cursor_result.limit(-1):
            return result


    def find_one_by_object(self, collection: str, object_id: int, *args, **kwargs):
        """
        Retrieves a single document with the given object_id from the given collection

        Args:
            collection (str): name of database collection
            object_id (int): object_id of document

        Returns:
            document with given object_id
        """
        cursor_result = self.__find(collection, {'object_id': object_id}, limit=1, *args, **kwargs)
        for result in cursor_result.limit(-1):
            return result


    def find_one_child(self, collection: str, parent_id: int, *args, **kwargs):
        """
        Retrieves a single child location of given parent

        Args:
            collection (str): name of database collection
            parent_id (int): public_id of parent

        Returns:
            document with given parent
        """
        cursor_result = self.__find(collection, {'parent': parent_id}, limit=1, *args, **kwargs)
        for result in cursor_result.limit(-1):
            return result


    def find_one_by(self, collection: str, *args, **kwargs) -> dict:
        """find one specific document by special requirements

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            found document
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
        found_documents = self.__find(collection=collection, *args, **kwargs)
        return list(found_documents)


    def count(self, collection: str, filter_: dict = None, *args, **kwargs):
        """Count documents based on filter parameters.

        Args:
            collection (str): name of database collection
            filter (dict): document count requirements
            *args: arguments for search operation
            **kwargs:

        Returns:
            returns the count of the documents
        """
        filter_ = filter_ or {}
        return self.connector.get_collection(collection).count_documents(filter=filter_, *args, **kwargs)


    def aggregate(self, collection: str, *args, **kwargs):
        """
        Aggregation on mongodb.

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            returns computed results
        """
        return self.connector.get_collection(collection).aggregate(*args, **kwargs, allowDiskUse=True)


    def search(self, collection: str, *args, **kwargs):
        """TODO: document"""
        return self.find(collection, *args, **kwargs)


    def insert(self, collection: str, data: dict, skip_public: bool = False) -> int:
        """adds document to database

        Args:
            collection (str): name of database collection
            data (dict): insert data
            skip_public (bool): Skip the public id creation and counter increment

        Returns:
            int: new public id of the document
        """
        if skip_public:
            return self.connector.get_collection(collection).insert_one(data)

        if 'public_id' not in data:
            data['public_id'] = self.get_next_public_id(collection=collection)

        self.connector.get_collection(collection).insert_one(data)
        # update the id counter
        self.update_public_id_counter(collection, data['public_id'])

        return data['public_id']


    def update(self, collection: str, filter_: dict, data: dict, *args, **kwargs):
        """
        Update document inside database

        Args:
            collection (str): name of database collection
            filter (dict): filter of document
            data: data to update

        Returns:
            acknowledged
        """
        formatted_data = {'$set': data}

        return self.connector.get_collection(collection).update_one(filter_, formatted_data, *args, **kwargs)


    def unset_update_many(self, collection: str, filter_: dict, data: str, *args, **kwargs):
        """update document inside database

        Args:
            collection (str): name of database collection
            filter (dict): filter of document
            data: data to delete

        Returns:
            acknowledged
        """
        formatted_data = {'$unset': {data: 1}}

        return self.connector.get_collection(collection).update_many(filter_, formatted_data, *args, **kwargs)


    def update_many(self, collection: str, query: dict, update: dict) -> UpdateResult:
        """update all documents that match the filter from a collection.

        Args:
            collection (str): name of database collection
            query (dict): A query that matches the documents to update.
            update (dict): The modifications to apply.

        Returns:
            A boolean acknowledged as true if the operation ran with write
            concern or false if write concern was disabled
        """
        result = self.connector.get_collection(collection).update_many(filter=query, update=update)

        if not result.acknowledged:
            raise DocumentCouldNotBeDeleted(collection, None)

        return result


    def insert_with_internal(self, collection: str, _id: int or str, data: dict):
        """TODO: document"""
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

    def delete(self, collection: str, filter_: dict, *args, **kwargs) -> DeleteResult:
        """delete document inside database

        Args:
            collection (str): name of database collection
            filter (dict): filter query

        Returns:
            acknowledged
        """
        result = self.connector.get_collection(collection).delete_one(filter_)

        if result.deleted_count != 1:
            raise DocumentCouldNotBeDeleted(collection, filter_)

        return result


    def delete_many(self, collection: str, **requirements: dict) -> DeleteResult:
        """removes all documents that match the filter from a collection.

        Args:
            collection (str): name of database collection
            filter (dict): Specifies deletion criteria using query operators.

        Returns:
            A boolean acknowledged as true if the operation ran
            with write concern or false if write concern was disabled
        """
        requirements_filter = {}
        for k, req in requirements.items():
            requirements_filter.update({k: req})

        result = self.connector.get_collection(collection).delete_many(requirements_filter)

        if not result.acknowledged:
            raise DocumentCouldNotBeDeleted(collection, None)

        return result


    def create_database(self, name: str) -> Database:
        """Create a new empty database.

        Args:
            name (str): Name of the new database.

        Raises:
            DatabaseAlreadyExists: If a database with this name already exists.

        Returns:
            Database: Instance of the new create database.
        """
        if name in self.connector.client.list_database_names():
            raise DatabaseAlreadyExists(name)

        return self.connector.client[name]


    def drop_database(self, database):
        """Delete a existing database.

        Args:
            database: name or instance of the database

        Raises:
            DatabaseNotExists: If the database not exists.
        """
        if isinstance(database, Database):
            database = database.name

        if database not in self.connector.client.list_database_names():
            raise DatabaseNotExists(database)

        self.connector.client.drop_database(database)


    def create_collection(self, collection_name):
        """
        Creation empty MongoDB collection
        Args:
            collection_name: name of collection

        Returns:
            collection name
        """
        from pymongo.errors import CollectionInvalid

        try:
            self.connector.create_collection(collection_name)
        except CollectionInvalid:
            raise CollectionAlreadyExists(collection_name)

        return collection_name


    def delete_collection(self, collection):
        """
        Delete MongoDB collection
        Args:
            collection: collection name

        Returns:
            delete ack
        """
        return self.connector.delete_collection(collection)


    def get_document_with_highest_id(self, collection: str) -> str:
        """get the document with the highest public id inside a collection

        Args:
            collection (str): name of database collection

        Returns:
            str: document from database
        """
        formatted_sort = [('public_id', DESCENDING)]

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

    def get_next_public_id(self, collection: str) -> int:
        try:
            founded_counter = self.connector.get_collection(PublicIDCounter.COLLECTION).find_one(filter={
                '_id': collection
            })
            new_id = founded_counter['counter'] + 1
        except (NoDocumentFound, Exception) as err:
            docs_count = self._init_public_id_counter(collection)
            new_id = docs_count + 1
        finally:
            self.increment_public_id_counter(collection)

        return new_id


    def _init_public_id_counter(self, collection: str):
        """TODO:document"""
        docs_count = self.get_highest_id(collection)
        self.connector.get_collection(PublicIDCounter.COLLECTION).insert_one({
            '_id': collection,
            'counter': docs_count
        })

        return docs_count

    def increment_public_id_counter(self, collection: str):
        """TODO: document"""
        working_collection = self.connector.get_collection(PublicIDCounter.COLLECTION)
        query = {
            '_id': collection
        }
        counter_doc = working_collection.find_one(query)
        counter_doc['counter'] = counter_doc['counter'] + 1

        try:
            self.connector.get_collection(PublicIDCounter.COLLECTION).update_one(query, {"$set":{"counter":counter_doc['counter']}})
        except Exception as error:
            LOGGER.info(f'Public ID Counter not increased: reason => {error}')


    def update_public_id_counter(self, collection: str, value: int):
        """TODO: document"""
        working_collection = self.connector.get_collection(PublicIDCounter.COLLECTION)
        query = {
            '_id': collection
        }
        counter_doc = working_collection.find_one(query)
        # init counter, if it was not found
        if counter_doc is None:
            self._init_public_id_counter(collection)
            counter_doc = working_collection.find_one(query)
        # update counter only, if value is higher than counter
        if value > counter_doc['counter']:
            counter_doc['counter'] = value
            self.connector.get_collection(PublicIDCounter.COLLECTION).update_one(query, counter_doc)


    def get_root_location_data(self) -> dict:
        """
        This class holds the correct root location data
        
        Returns:
            (dict): Returns valid root location data
        """
        return {
            "public_id":1,
            "name":"Root",
            "parent":0,
            "object_id":0,
            "type_id":0,
            "type_label":"Root",
            "type_icon":"fas fa-globe",
            "type_selectable":True
        }


    def validate_root_location(self, tested_location: dict) -> bool:
        """
        Checks if a given location holds valid root location data

        Args:
            tested_location (dict): location data which should be tested

        Returns:
            (bool): Returns boolean if the given dict has valid root location data
        """
        root_location = self.get_root_location_data()

        for root_key, root_value in root_location.items():
            if root_key not in tested_location.keys():
                return False

            # check if value is valid
            if root_value != tested_location[root_key]:
                return False

        return True


    def set_root_location(self, collection: str, create: bool = False):
        """
        Does the setup for root location. If no counter for locations exist, it will be created

        Args:
            collection (str): framework.locations
            create (bool): If true the root location will be created, else it will be updated

        Returns:
            status: status of location creation or update
        """
        status:int = 0

        if create:
            ## check if counter is created in db, else create one
            counter = self.connector.get_collection(PublicIDCounter.COLLECTION).find_one(filter={'_id': collection})

            if not counter:
                self._init_public_id_counter(collection)

            status = self.insert(collection, self.get_root_location_data())
        else:
            status = self.update(collection,{'public_id':1},self.get_root_location_data())

        return status


class DatabaseGridFS(GridFS):
    """
    Creation a GridFSBucket instance to use
    """

    def __init__(self, database: Database, collection_name: str):
        super().__init__(database, collection_name)
        self.message = f"Collection {collection_name} already exists"
