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
Connection to database over a given connector
"""
import os
import logging
from pymongo import MongoClient
from pymongo.database import Database

from cmdb.database.connection_status import ConnectionStatus

from cmdb.errors.database import DatabaseConnectionError, SetDatabaseError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                MongoConnector - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class MongoConnector:
    """
    PyMongo (MongoDB) implementation with connector
    """
    def __init__(self, host: str, port: int, database_name: str, client_options: dict = None):
        connection_string = os.getenv('CONNECTION_STRING')

        if connection_string:
            self.client = MongoClient(connection_string)
        else:
            if client_options:
                self.client = MongoClient(host=host, port=int(port), connect=False, **client_options)
            else:
                self.client = MongoClient(host=host, port=int(port), connect=False)

        self.database: Database = self.client.get_database(database_name)
        self.host: str = host
        self.port: int = port


    def set_database(self, db_name: str):
        """
        Sets the database of the connector

        Raises:
            SetDatabaseError: Raised when not possible to set connector to database name

        Args:
            db_name (str): name of the database
        """
        try:
            self.database = self.client.get_database(db_name)
        except Exception as err:
            LOGGER.debug("[set_database] Can't set connector to database: %s. Error: %s", db_name, err)
            raise SetDatabaseError(err, db_name) from err


    def connect(self) -> ConnectionStatus:
        """
        Connect to database
        Returns: connections status
        """
        try:
            status = self.client.admin.command('ismaster')

            return ConnectionStatus(connected=True, message=str(status))
        except Exception as err:
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
        Check if client is connected successfully

        Returns (bool): True if connected / False if disconnected
        """
        return self.connect().get_status()


    def __exit__(self, *err):
        """auto close mongo client on exit"""
        self.disconnect()
