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
"""The module implements the base for database managers"""
import logging
from typing import Union, Any, List

from pymongo.database import Database
from pymongo.errors import CollectionInvalid
from pymongo import IndexModel
from pymongo.collection import Collection

from cmdb.database.mongo_connector import MongoConnector
from cmdb.errors.database import DatabaseAlreadyExists, DatabaseNotExists, CollectionAlreadyExists
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class DatabaseManager:
    """
    Base class for database managers
    """

    def __init__(self, connector: MongoConnector):
        """Constructor of `DatabaseManager`
        Args:
            connector (MongoConnector): Database Connector for subclass implementation
        """
        self.connector: MongoConnector = connector

# -------------------------------------------- GENERAL DATABASE OPERATIONS ------------------------------------------- #

    def check_database_exists(self, name:str) -> bool:
        """Checks if a database with the given name exists

        Args:
            name (str): Name of the database which should be checked

        Returns:
            bool: True if database with given name exists, else false
        """
        database_names = self.connector.client.list_database_names()

        return name in database_names


    def create_database(self, name: str) -> Database:
        """Create a new empty database

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


    def drop_database(self, database: Union[str, Database]):
        """Delete a existing database.

        Args:
            database: name or instance of the database

        Raises:
            DatabaseNotExists: If the database does not exist
        """
        if isinstance(database, Database):
            database = database.name

        if database not in self.connector.client.list_database_names():
            raise DatabaseNotExists(database)

        self.connector.client.drop_database(database)


    def create_collection(self, collection_name: str) -> str:
        """
        Creation empty MongoDB collection
        Args:
            collection_name: name of collection

        Returns:
            collection name
        """
        try:
            all_collections = self.connector.database.list_collection_names()

            if collection_name not in all_collections:
                self.connector.database.create_collection(collection_name)
        except CollectionInvalid as err:
            raise CollectionAlreadyExists(collection_name) from err

        return collection_name


    def get_collection(self, name) -> Collection:
        """
        Get a collection inside database

        Args:
            name: Collection name
        """
        return self.connector.database[name]


    def delete_collection(self, collection: str) -> dict[str, Any]:
        """
        Delete MongoDB collection
        Args:
            collection (str): collection name

        Returns:
            delete ack
        """
        return self.connector.database.drop_collection(collection)


    def create_indexes(self, collection: str, indexes: List[IndexModel]) -> List[str]:
        """Creates indexes for collection"""
        return self.get_collection(collection).create_indexes(indexes)


    def get_index_info(self, collection: str):
        """get the max index value"""
        return self.get_collection(collection).index_information()


    def status(self):
        """Check if connector has connection."""
        return self.connector.is_connected()
