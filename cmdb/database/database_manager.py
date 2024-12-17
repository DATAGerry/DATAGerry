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
"""The module implements the base class for database managers"""
import logging
from typing import Union, Any
from collections.abc import MutableMapping
from pymongo.database import Database
from pymongo.errors import CollectionInvalid
from pymongo import IndexModel
from pymongo.collection import Collection

from cmdb.database.mongo_connector import MongoConnector

from cmdb.errors.database import (
    DatabaseAlreadyExists,
    DatabaseNotExists,
    CollectionAlreadyExists,
    GetCollectionError,
    DeleteCollectionError,
    CreateIndexesError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                    DatabaseManager                                                   #
# -------------------------------------------------------------------------------------------------------------------- #

class DatabaseManager:
    """
    Base class for database managers
    """
    def __init__(self, connector: MongoConnector):
        self.connector: MongoConnector = connector

# -------------------------------------------- GENERAL DATABASE OPERATIONS ------------------------------------------- #

    def check_database_exists(self, name:str) -> bool:
        """Checks if a database with the given name exists

        Args:
            name (str): Name of the database which should be checked

        Returns:
            (bool): True if database with given name exists, else False
        """
        database_names = self.connector.client.list_database_names()

        return name in database_names


    def create_database(self, name: str) -> Database:
        """Create a new empty database

        Args:
            name (str): Name of the new database.

        Raises:
            DatabaseAlreadyExists: If a database with this name already exists

        Returns:
            Database: Instance of the new create database
        """
        if name in self.connector.client.list_database_names():
            raise DatabaseAlreadyExists(name)

        return self.connector.client[name]


    def drop_database(self, database: Union[str, Database]):
        """Delete a existing database

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
            collection_name (str): name of collection

        Returns:
            (str): Collection name
        """
        try:
            all_collections = self.connector.database.list_collection_names()

            if collection_name not in all_collections:
                self.connector.database.create_collection(collection_name)
        except CollectionInvalid as err:
            raise CollectionAlreadyExists(collection_name) from err

        return collection_name


    def get_collection(self, name: str) -> Collection:
        """
        Get a collection from the database

        Args:
            name (str): Collection name

        Raises:
            GetCollectionError: When the collection could not be retrieved
        Returns:
            (Collection): The requested collection
        """
        try:
            return self.connector.database[name]
        except Exception as err:
            LOGGER.debug("[get_collection] Can't retrive collection: %s. Error: %s", name, err)
            raise GetCollectionError(name, str(err)) from err


    def delete_collection(self, collection: str) -> dict[str, Any]:
        """
        Delete MongoDB collection

        Args:
            collection (str): collection name

        Raises:
            DeleteCollectionError: When collection can't be deleted

        Returns:
            delete ack
        """
        try:
            return self.connector.database.drop_collection(collection)
        except Exception as err:
            LOGGER.debug("[delete_collection] Can't delete collection: %s. Error: %s", collection, err)
            raise DeleteCollectionError(collection, str(err)) from err


    def create_indexes(self, collection: str, indexes: list[IndexModel]) -> list[str]:
        """
        Creates indexes for collection

        Args:
            collection (str): name of collection
            indexes (list[IndexModel]): list of IndexModels which should be created

        Raises:
            CreateIndexesError: When indexes can't be created

        Returns:
            list[str]: List of created indexes
        """
        try:
            return self.get_collection(collection).create_indexes(indexes)
        except Exception as err:
            LOGGER.debug("[create_indexes] Can't create indexes in: %s. Error: %s", collection, err)
            raise CreateIndexesError(str(err)) from err


    def get_index_info(self, collection: str) -> MutableMapping[str, Any]:
        """
        Retrives index information for a collection

        Args:
            collection (str): name of collection

        Raises:
            GetCollectionError: When the collection could not be retrieved

        Returns:
            MutableMapping[str, Any]: index information of the collection
        """
        try:
            return self.get_collection(collection).index_information()
        except GetCollectionError as err:
            raise GetCollectionError(collection, err) from err


    def status(self):
        """Check if connector has connection to MongoDB"""
        return self.connector.is_connected()
