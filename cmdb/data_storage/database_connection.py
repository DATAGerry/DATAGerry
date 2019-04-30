# Net|CMDB - OpenSource Enterprise CMDB
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
Database-Connection
Real connection to database over a given connector
"""
import logging
from pymongo.errors import ServerSelectionTimeoutError

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


class Connector:
    """
    Superclass connector
    """

    DEFAULT_CONNECTION_TIMEOUT = 100

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
        Returns: connections status
        """
        raise NotImplementedError

    def disconnect(self):
        """
        disconnect from database
        Returns: connection status
        """
        raise NotImplementedError

    def is_connected(self):
        """
        check if connection to database exists
        Returns: True/False
        """
        raise NotImplementedError


class MongoConnector(Connector):
    """
    PyMongo (MongoDB) implementation from connector
    """

    DEFAULT_CONNECTION_TIMEOUT = 1000

    def __init__(self, host: str, port: int, database_name: str, timeout: int = DEFAULT_CONNECTION_TIMEOUT,
                 auth: str = ''):
        """

        init mongodb connector
        Args:
            host: database server address
            port: database server port
            database_name: database name
            timeout: connection timeout
            auth: (optional) authentication methods
            @see http://api.mongodb.com/python/current/examples/authentication.html for more informations -
            same paramenters in cmdb.conf
        """

        super().__init__(host, port, database_name, timeout)
        from pymongo import MongoClient
        self.auth_method = auth  # TODO: Implement authentication
        self.client = MongoClient(
            self.host,
            self.port,
            connect=False,
            socketTimeoutMS=self.timeout,
            serverSelectionTimeoutMS=self.timeout,
            # socketKeepAlive=True, # Deactivated on DeprecationWarning: The socketKeepAlive option is deprecated.
            # see https://docs.mongodb.com/manual/faq/diagnostics/#does-tcp-keepalive-time-affect-mongodb-deployments
            maxPoolSize=None
        )
        self.database = self.client[database_name]

    def connect(self) -> str:
        """
        try's to connect to database
        Returns:
            server status
        """
        try:
            self.client.admin.command('ping')
            return self.client.server_info()
        except ServerSelectionTimeoutError:
            raise ServerTimeoutError(self.host)

    def disconnect(self) -> bool:
        """
        try's to disconnect from database
        Returns:
            server status
        """
        return self.client.close()

    def is_connected(self) -> bool:
        """
        check if connection to database exists
        Returns:
            connection status
        """
        try:
            self.connect()
            return True
        except ServerTimeoutError as e:
            LOGGER.error(f'Not connected to database: {e.message}')
            return False

    def create_collection(self, collection_name) -> str:
        """
        creation collection/table in database
        Args:
            collection_name: name of collection

        Returns:
            creation ack
        """
        return self.database.create_collection(collection_name)

    def delete_collection(self, collection_name) -> str:
        """
        delete collection/table in database
        Args:
            collection_name: name of collection

        Returns:
            creation ack
        """
        return self.database.drop_collection(collection_name)

    def get_database_name(self) -> str:
        """
        get database name
        Returns:
            name of selected database
        """
        return self.database.name

    def get_database(self):
        """
        get database
        Returns:
            database object
        """
        return self.database

    def get_collection(self, name):
        """
        get a collection inside database
        (same as Tables in SQL)
        Args:
            name:  collection name

        Returns: collection object
        """
        return self.database[name]

    def get_collections(self) -> list:
        """
        list all collections inside mongo database
        Returns:
            list of collections
        """
        return self.database.collection_names()

    def __exit__(self, *err):
        """auto close client on exit"""
        self.client.close()


class DatabaseConnectionError(CMDBError):
    """
    Error if connection to database broke up
    """

    def __init__(self):
        super().__init__()
        self.message = "Connection error - No connection could be established with the database"


class ServerTimeoutError(CMDBError):
    """
    Server timeout error if connection is lost
    """

    def __init__(self, host):
        super().__init__()
        self.message = "Server Timeout - No connection to database at {}".format(host)
