# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

from cmdb.database.errors.connection_errors import DatabaseConnectionError
# -------------------------------------------------------------------------------------------------------------------- #

class ConnectionStatus:
    """Class representing the status of connection to database"""

    def __init__(self, connected: bool, message: str = 'No message given', time_alive: datetime = None):
        self.connected: bool = connected
        self.message: str = message
        self.time_alive = time_alive

# -------------------------------------------------------------------------------------------------------------------- #
#                                                MongoConnector - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #

class MongoConnector:
    """
    PyMongo (MongoDB) implementation from connector
    """
    DEFAULT_CONNECTION_TIMEOUT = 3000

    def __init__(self, host: str, port: int, database_name: str, client_options: dict = None):
        if client_options:
            self.client: MongoClient = MongoClient(host=host, port=int(port), connect=False, **client_options)
        else:
            self.client: MongoClient = MongoClient(host=host, port=int(port), connect=False)

        self.database: Database = self.client.get_database(database_name)
        self.host: str = host
        self.port: int = port


    def connect(self) -> ConnectionStatus:
        """
        Connect to database
        Returns: connections status
        """
        try:
            status = self.client.admin.command('ismaster')
            return ConnectionStatus(connected=True, message=str(status))
        except ConnectionFailure as err:
            raise DatabaseConnectionError(err) from err


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


    def __exit__(self, *err):
        """auto close mongo client on exit"""
        self.disconnect()
