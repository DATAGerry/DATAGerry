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


#ERROR-FIX (never used)
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


#ERROR-FIX (not used)
class CollectionAlreadyExists(DataBaseError):
    """
    Error if you try to create a collection that alrady exists
    """
    def __init__(self, collection_name: str):
        self.message = f"Collection {collection_name} already exists"
        super().__init__(self.message)


#ERROR-FIX (Use the Pymongo error)
class NoDocumentFound(DataBaseError):
    """
    Error if no document was found
    """
    def __init__(self, collection:str):
        self.message = f"No document was found inside {collection}"
        super().__init__(self.message)


class DocumentCouldNotBeDeleted(DataBaseError):
    """
    Error if document could not be deleted from database
    """
    def __init__(self, collection: str):
        self.message = f"A document could not be deleted from Collection: {collection}"
        super().__init__(self.message)
