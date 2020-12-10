# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2020 NETHINKS GmbH
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
Database-Connection
Real connection to database over a given connector
"""
from datetime import datetime
from typing import Generic
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

from cmdb.database import CLIENT
from cmdb.database.errors.connection_errors import DatabaseConnectionError


class ConnectionStatus:

    def __init__(self, connected: bool, message: str = None, time_alive: datetime = None):
        self.connected: bool = connected  # Connected = True, Disconnected = False
        self.message: str = message or 'No message given'
        self.time_alive = time_alive


class Connector(Generic[CLIENT]):
    """
    Base class of the database connector.
    This class is called by the managers, which allows an indirect forwarding to the respective database client.
    """
    DEFAULT_CONNECTION_TIMEOUT = 3000

    def __init__(self, client: CLIENT, host: str, port: int = None, *args, **kwargs):
        """
        Constructor of Connector class
        Args:
            client: Generic connection client instance (e.g. PyMongoClient)
            host: ip address or hostname of the database
            port: port of the database
        """
        self.client: CLIENT = client
        self.host: str = host
        self.port: int = port

    def connect(self, *args, **kwargs) -> ConnectionStatus:
        """
        Connect to database
        Returns: connections status
        """
        raise NotImplementedError

    def disconnect(self, *args, **kwargs) -> ConnectionStatus:
        """
        Disconnect from database
        Returns: connection status
        """
        raise NotImplementedError

    def is_connected(self) -> bool:
        """
        Check if client is connected successfully
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

    def __init__(self, host: str, port: int, database_name: str, client_options: dict):
        client = MongoClient(host=host, port=int(port), connect=False, **client_options)
        self.database: Database = client.get_database(database_name)
        super(MongoConnector, self).__init__(client, host, port)

    def connect(self) -> ConnectionStatus:
        """
        Connect to database
        Returns: connections status
        """
        try:
            status = self.client.admin.command('ismaster')
            return ConnectionStatus(connected=True, message=str(status))
        except ConnectionFailure as mcf:
            raise DatabaseConnectionError(message=str(mcf))

    def disconnect(self) -> ConnectionStatus:
        """
        Disconnect from database
        Returns: connection status
        """
        self.client.close()
        return ConnectionStatus(connected=False)

    def is_connected(self) -> bool:
        """
        check if client is connected successfully
        Returns: True if connected / False if disconnected
        """
        return self.connect().connected

    def create_collection(self, collection_name) -> Collection:
        """
        Creation collection in database
        Args:
            collection_name
        """
        return self.database.create_collection(collection_name)

    def delete_collection(self, collection_name):
        """
        delete collection/table in database

        Args:
            collection_name: name of collection

        Returns:
            creation ack
        """
        self.database.drop_collection(collection_name)

    def get_collection(self, name) -> Collection:
        """
        Get a collection inside database

        Args:
            name: Collection name
        """
        return self.database[name]

    def __exit__(self, *err):
        """auto close mongo client on exit"""
        self.disconnect()
