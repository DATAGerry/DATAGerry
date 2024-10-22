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
import logging
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

from cmdb.database.connection_status import ConnectionStatus

from cmdb.errors.database import DatabaseConnectionError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
class MongoConnector:
    """
    PyMongo (MongoDB) implementation from connector
    """

    def __init__(self, host: str, port: int, database_name: str, client_options: dict = None):
        if client_options:
            self.client: MongoClient = MongoClient(host=host, port=int(port), connect=False, **client_options)
        else:
            self.client: MongoClient = MongoClient(host=host, port=int(port), connect=False)

        self.database: Database = self.client.get_database(database_name)
        self.host: str = host
        self.port: int = port


    def set_database(self, db_name: str):
        """Sets the database of the connector"""
        try:
            self.database = self.client.get_database(db_name)
        except Exception as err:
            #ERROR-FIX
            LOGGER.error("Can't set connector database with name: %s. Error: %s", db_name, err)


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
        return self.connect().get_status()


    def __exit__(self, *err):
        """auto close mongo client on exit"""
        self.disconnect()
