"""
Database-Connection
Real connection to database over a given connector
"""
from pymongo.errors import ServerSelectionTimeoutError


class Connector:
    """
    Superclass connector
    """

    DEFAULT_CONNECTION_TIMEOUT = 10

    def __init__(self, host, port, database_name, timeout=DEFAULT_CONNECTION_TIMEOUT):
        """
        Connector init
        Args:
            host: database server address
            port: database server port
            database_name: database name
            timeout: connection timeout in sec
        """
        self.host = host
        self.port = port
        self.database_name = database_name
        self.timeout = timeout

    def connect(self):
        """
        connect to database
        :return: connections status
        """
        raise NotImplementedError

    def disconnect(self):
        """
        disconnect from database
        :return: connection status
        """
        raise NotImplementedError

    def is_connected(self):
        """
        check if connection to database exists
        :return: True/False
        """
        raise NotImplementedError


class MongoConnector(Connector):
    """
    PyMongo (MongoDB) implementation from connector
    """

    DEFAULT_CONNECTION_TIMEOUT = 100

    def __init__(self, host, port, database_name, timeout):
        """
        init mongodb connector
        :param host: database server address
        :param port: database server port
        :param database_name: database name
        :param auth: (optional) authentication methods
               @see http://api.mongodb.com/python/current/examples/authentication.html
               for more informations - same paramenters in cmdb.conf
        """
        super().__init__(host, port, database_name, timeout)
        from pymongo import MongoClient
        self.client = MongoClient(
            self.host,
            self.port,
            connect=False,
            socketTimeoutMS=self.timeout,
            serverSelectionTimeoutMS=self.timeout,
            socketKeepAlive=True,
            maxPoolSize=None
        )
        self.database = self.client[database_name]

    def connect(self):
        """
        try's to connect to database
        :return: server status
        """
        try:
            self.client.admin.command('ping')
            return self.client.server_info()
        except ServerSelectionTimeoutError:
            raise ServerTimeoutError(self.host)

    def disconnect(self):
        """
        try's to disconnect from database
        :return: server status
        """
        return self.client.close()

    def is_connected(self):
        """
        check if connection to database exists
        :return: True/False
        """
        try:
            self.connect()
            return True
        except ServerSelectionTimeoutError:
            return False

    def create_collection(self, collection_name):
        return self.database.create_collection(collection_name)

    def delete_collection(self, collection_name):
        return self.database.drop_collection(collection_name)

    def get_database_name(self):
        """
        get database name
        :return: database name
        """
        return self.database.name

    def get_database(self):
        """
        get database
        :return: database object
        """
        return self.database

    def get_collection(self, name):
        """
        get a collection inside database
        (same as Tables in SQL)
        :param name: collection name
        :return: collection object
        """
        return self.database[name]

    def get_collections(self):
        """
        list all collections inside mongo database
        :return:
        """
        return self.database.collection_names()


class ServerTimeoutError(Exception):
    """
    Server timeout error if connection is lost
    """

    def __init__(self, host):
        super().__init__()
        self.message = "Server Timeout - No connection to database at {}".format(host)
