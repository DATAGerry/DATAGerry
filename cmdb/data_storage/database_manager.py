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
        """
        instance of super class
        :param connector: Database Connector for subclass implementation
        """
        self.database_connector = connector

    def status(self):
        """
        check if connector has connection
        :return: connection status
        """
        return self.database_connector.is_connected()

    def setup(self):
        """
        setup script for database init
        :return:
        """
        raise NotImplementedError

    def __find(self, *args, **kwargs):
        """
        general find function for database search
        :param args: arguments for search operation
        :param kwargs: key arguments
        :return: founded document
        """
        raise NotImplementedError

    def find_one_by(self, *args, **kwargs):
        raise NotImplementedError

    def find_one(self, *args, **kwargs):
        """
        calls __find with single return
        :param args: arguments for search operation
        :param kwargs: key arguments
        :return: founded document
        """
        raise NotImplementedError

    def find_all(self, *args, **kwargs):
        """
        calls __find with all returns
        :param args: arguments for search operation
        :param kwargs: key arguments
        :return: list of founded documents
        """
        raise NotImplementedError

    def insert(self, *args, **kwargs):
        """
        adds document to database
        :param args: object data
        :param kwargs: dict of data
        :return: public id of inserted document
        """
        raise NotImplementedError

    def update(self, *args, **kwargs):
        """
        update document inside database
        :param args: object data
        :param kwargs: dict of data
        :return: acknowledged
        """
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        """
        delete document inside database
        :param args: public id
        :param kwargs: dict of public id
        :return: acknowledged
        """
        raise NotImplementedError

    def create(self, db_name):
        """
        create new database
        :param db_name: name of database
        :return: acknowledged
        """
        raise NotImplementedError

    def drop(self, db_name):
        """
        delete database
        :param db_name: name of database
        :return: acknowledged
        """
        raise NotImplementedError


class DatabaseManagerMongo(DatabaseManager):
    """
    PyMongo (mongodb) implementation of Database Manager
    """

    def __init__(self, connector):
        """
        init mongo implementation
        :param connector: mongodb connector
        """
        super().__init__(connector)
        self.database_name = self.database_connector.get_database_name()

    def setup(self):
        """
        setup script
        :return: acknowledged
        """
        pass

    def __find(self, collection, *args, **kwargs):
        """
        general find function for database search
        :param args: arguments for search operation
        :param kwargs: key arguments
        :return: founded document
        """
        return self.database_connector.get_collection(collection).find(*args, **kwargs)

    def find_one(self, collection, public_id, *args, **kwargs):
        """
        calls __find with single return
        :param collection: name of collection
        :param public_id: public id of document
        :param args: arguments for search operation
        :param kwargs: key arguments
        :return: founded document
        """
        formatted_public_id = {'public_id': public_id}
        formatted_sort = [('public_id', DatabaseManager.DESCENDING)]
        cursor_result = self.__find(collection, formatted_public_id, limit=1, sort=formatted_sort, *args, **kwargs)
        for result in cursor_result.limit(-1):
            return result
        raise NoDocumentFound(collection, public_id)

    def find_one_by(self, collection, *args, **kwargs):
        cursor_result = self.__find(collection, limit=1, *args, **kwargs)
        for result in cursor_result.limit(-1):
            return result
        raise NoDocumentFound(collection, args)

    def find_all(self, collection, *args, **kwargs):
        """
        calls __find with all returns
        :param collection: name of collection
        :param args: arguments for search operation
        :param kwargs: key arguments
        :return: list of founded documents
        """
        return list(self.__find(collection=collection, *args, **kwargs))

    def insert(self, collection, data):
        """
        adds document to database
        :param collection: name of collection
        :param data: dict of data
        :return: public id of inserted document
        """
        result = self.database_connector.get_collection(collection).insert_one(data)
        if result.acknowledged:
            formatted_id = {'_id': result.inserted_id}
            projection = {'public_id': 1}
            cursor_result = self.__find(collection, formatted_id, projection, limit=1)
            for result in cursor_result.limit(-1):
                return int(result['public_id'])
        return None

    def update(self, collection, public_id: int, data):
        """
        update document inside database
        :param collection: name of collection
        :param public_id: public id of document
        :param data: data to update
        :return: acknowledged
        """
        formatted_public_id = {'public_id': public_id}
        formatted_data = {'$set': data}
        return self.database_connector.get_collection(collection).update(formatted_public_id, formatted_data)

    def delete(self, collection, public_id: int):
        """
        delete document inside database
        :param collection: name of collection
        :param public_id: public id of document
        :return: acknowledged
        """
        formatted_public_id = {'public_id': public_id}
        result = self.database_connector.get_collection(collection).delete_one(formatted_public_id)
        if result.deleted_count != 1:
            raise DocumentCouldNotBeDeleted(collection, public_id)
        return result

    def create(self, db_name):
        """
        create database
        :param db_name: name of database
        :return: acknowledge of operation
        """
        return self.database_connector.client[db_name]

    def drop(self, db_name):
        """
        delete database
        :param db_name: name of database
        :return: acknowledge of operation
        """
        return self.database_connector.client.drop_database(db_name)


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
