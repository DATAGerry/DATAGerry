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
Database-Connection
Real connection to database over a given connector
"""
import logging
from pymongo.errors import ServerSelectionTimeoutError

from cmdb.data_storage.database_connection_utils import CLIENT, ConnectionStatus, MongoConnectionFailure

from pymongo import MongoClient
from typing import Generic

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


class Connector(Generic[CLIENT]):
    DEFAULT_CONNECTION_TIMEOUT = 3000

    def __init__(self, client: CLIENT, host: str, port: int, database_name: str):
        self.client: CLIENT = client
        self.host: str = host
        self.port: int = port
        self.database_name: str = database_name

    def get_client(self) -> CLIENT:
        """
        get client
        Returns: returns the active client connection
        """
        return self.client

    def get_database_name(self) -> str:
        """get name of selected database"""
        return self.database_name

    def connect(self) -> ConnectionStatus:
        """
        connect to database
        Returns: connections status
        """
        raise NotImplementedError

    def disconnect(self) -> ConnectionStatus:
        """
        disconnect from database
        Returns: connection status
        """
        raise NotImplementedError

    def is_connected(self) -> bool:
        """
        check if client is connected successfully
        Returns: True if connected / False if disconnected
        """
        raise NotImplementedError

    def __exit__(self, *err):
        """auto close client on exit
        Notes: IT IS IMPORTANT TO AUTO DISCONNECT
        """
        raise NotImplementedError


class MongoConnector(Connector[MongoClient]):
    """
    PyMongo (MongoDB) implementation from connector
    """
    DOCUMENT_CLASS = dict
    AUTO_CONNECT: bool = True

    def __init__(self, host: str, port: int, database_name: str, **kwargs):
        self.client_options = kwargs or {}
        client = MongoClient(host=host, port=int(port), document_class=self.DOCUMENT_CLASS,
                             connect=self.AUTO_CONNECT, **self.client_options)
        super(MongoConnector, self).__init__(client, host, port, database_name)
        self.database = self.client.get_database(database_name)

    def connect(self) -> ConnectionStatus:
        """
        connect to database
        Returns: connections status
        """
        try:
            status = self.client.admin.command('ismaster')
            return ConnectionStatus(status=True, message=str(status))
        except MongoConnectionFailure as mcf:
            raise DatabaseConnectionError(message=str(mcf))

    def disconnect(self) -> ConnectionStatus:
        """
        disconnect from database
        Returns: connection status
        """
        self.client.close()
        return ConnectionStatus(status=False)

    def is_connected(self) -> bool:
        """
        check if client is connected successfully
        Returns: True if connected / False if disconnected
        """
        return self.connect().status()

    def __exit__(self, *err):
        """auto close mongo client on exit"""
        self.client.close()

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


class DatabaseConnectionError(CMDBError):
    """
    Error if connection to database broke up
    """

    def __init__(self, message):
        super().__init__()
        self.message = f'Connection error - No connection could be established with the database - error: {message}'


class ServerTimeoutError(CMDBError):
    """
    Server timeout error if connection is lost
    """

    def __init__(self, host):
        super().__init__()
        self.message = "Server Timeout - No connection to database at {}".format(host)
