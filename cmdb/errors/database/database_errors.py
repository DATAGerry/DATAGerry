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
Contains Database Error Classes
"""
# -------------------------------------------------------------------------------------------------------------------- #

class DataBaseError(Exception):
    """
    Base Database Error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# ------------------------------------------------- DATABASE - ERRORS ------------------------------------------------ #

class DatabaseConnectionError(DataBaseError):
    """
    Error if connection to database broke up or unable to connect
    """
    def __init__(self, db_name: str):
        self.message = f"Could not connect to database {db_name}"
        super().__init__(self.message)


class ServerTimeoutError(DataBaseError):
    """
    Server timeout error if connection is lost
    """
    def __init__(self, host:str):
        self.message = f"Server Timeout - No connection to database at {host}"
        super().__init__(self.message)


#TODO: ERROR-FIX (never used)
class DatabaseAlreadyExists(DataBaseError):
    """
    Error when database already exists
    """
    def __init__(self, db_name: str):
        self.message = f"Database with the name {db_name} already exists"
        super().__init__(self.message)


class DatabaseNotExists(DataBaseError):
    """
    Error when database does not exist
    """
    def __init__(self, db_name: str):
        self.message = f"Database with the name {db_name} doesn`t exists"
        super().__init__(self.message)


class SetDatabaseError(DataBaseError):
    """
    Error if database could not be set for a connector
    """
    def __init__(self, err: str, db_name: str):
        self.message = f"Couldn't set connector to database: {db_name}. Error: {err}"
        super().__init__(self.message)


#TODO: ERROR-FIX (not used)
class CollectionAlreadyExists(DataBaseError):
    """
    Error if you try to create a collection that alrady exists
    """
    def __init__(self, collection_name: str):
        self.message = f"Collection {collection_name} already exists"
        super().__init__(self.message)


class GetCollectionError(DataBaseError):
    """
    Raised when a collection could not be retrieved
    """
    def __init__(self, collection_name:str, err: str):
        self.message = f"Can't retrive collection: {collection_name}. Error: {err}"
        super().__init__(self.message)


class DeleteCollectionError(DataBaseError):
    """
    Raised when a collection could not be deleted
    """
    def __init__(self, collection_name:str, err: str):
        self.message = f"Can't delete collection: {collection_name}. Error: {err}"
        super().__init__(self.message)


class CreateIndexesError(DataBaseError):
    """
    Raised when indexes could not be created
    """
    def __init__(self, err: str):
        self.message = f"CreateIndexesError: {err}"
        super().__init__(self.message)


#TODO: ERROR-FIX (Use the Pymongo error)
class NoDocumentFound(DataBaseError):
    """
    Error if no document was found
    """
    def __init__(self, collection:str):
        self.message = f"No document was found inside {collection}"
        super().__init__(self.message)


class DocumentCreateError(DataBaseError):
    """
    Raised if a document could not be created in a collection
    """
    def __init__(self, collection: str, err: str):
        self.message = f"Document could not be created in collection: {collection}. Error: {err}"
        super().__init__(self.message)


class DocumentUpdateError(DataBaseError):
    """
    Raised if a document could not be updated in a collection
    """
    def __init__(self, collection: str, err: str):
        self.message = f"Document could not be updated in collection: {collection}. Error: {err}"
        super().__init__(self.message)


class DocumentDeleteError(DataBaseError):
    """
    Raised if a document could not be deleted from a collection
    """
    def __init__(self, collection: str, err: str):
        self.message = f"Document could not be deleted from collection: {collection}. Error: {err}"
        super().__init__(self.message)


class DocumentGetError(DataBaseError):
    """
    Raised if a document could not be retrieved from a collection
    """
    def __init__(self, collection: str, err: str):
        self.message = f"Document could not be retrieved from collection: {collection}. Error: {err}"
        super().__init__(self.message)


class DocumentAggregationError(DataBaseError):
    """
    Raised if an aggregation operation fails
    """
    def __init__(self, err: str):
        self.message = f"Aggregation failed. Error: {err}"
        super().__init__(self.message)
