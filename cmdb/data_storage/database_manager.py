"""
Database Management instance for database actions

"""


class DatabaseManager:
    """
    Default database manager with no implementation

    """

    DEFAULT_DATABASE_NAME = 'cmdb'
    ASCENDING = 1
    DESCENDING = -1

    def __init__(self, connector):
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


class DatabaseManagerMongo(DatabaseManager):
    """PyMongo (mongodb) implementation of Database Manager
    """

    def __init__(self, connector):
        """init mongo implementation

        Args:
            connector: mongodb connector

        """
        super().__init__(connector)

    def setup(self):
        """setup script

        Returns:
            acknowledged

        """
        raise NotImplementedError

    def __find(self, collection: str, *args, **kwargs):
        """general find function for database search

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            founded document

        """

        return self.database_connector.get_collection(collection).find(*args, **kwargs)

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
        for result in cursor_result.limit(-1):
            return result
        raise NoDocumentFound(collection, public_id)

    def find_one_by(self, collection: str, *args, **kwargs):
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

    def insert(self, collection, data) -> int:
        """adds document to database

        Args:
            collection (str): name of database collection
            data (str): insert data

        Returns:
            int: new public id of the document
            None: if anything goes wrong while inserting
        """
        result = self.database_connector.get_collection(collection).insert_one(data)
        if result.acknowledged:
            formatted_id = {'_id': result.inserted_id}
            projection = {'public_id': 1}
            cursor_result = self.__find(collection, formatted_id, projection, limit=1)
            for result in cursor_result.limit(-1):
                return int(result['public_id'])
        return None

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
        return self.database_connector.get_collection(collection).update(formatted_public_id, formatted_data)

    def delete(self, collection: str, public_id: int):
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
        from pymongo.errors import CollectionInvalid

        try:
            self.database_connector.create_collection(collection_name)
        except CollectionInvalid:
            raise CollectionAlreadyExists(collection_name)
        return collection_name

    def delete_collection(self, collection_name):
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
        return int(self.get_document_with_highest_id(collection)['public_id'])


class CollectionAlreadyExists(Exception):
    def __init__(self, collection_name):
        super().__init__()
        self.message = "Collection {} already exists".format(collection_name)


class NoDocumentFound(Exception):
    """
    Error if no document was found
    """

    def __init__(self, collection, public_id):
        super().__init__()
        self.message = "No document with the id {} was found inside {}".format(public_id, collection)


class DocumentCouldNotBeDeleted(Exception):
    """
    Error if document could not be deleted from database
    """

    def __init__(self, collection, public_id):
        super().__init__()
        self.message = "The document with the id {} could not be deleted inside {}".format(public_id, collection)
