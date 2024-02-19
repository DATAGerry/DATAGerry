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
"""Contains Database Error Classes"""
from pymongo.errors import DuplicateKeyError

from ..cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class DataBaseError(CMDBError):
    """Base Database Error"""
    def __init__(self, message: str):
        super().__init__(message)

# --------------------------------------------- SPECIFIC DATABASE ERRORS --------------------------------------------- #

class DatabaseConnectionError(DataBaseError):
    """Error if connection to database broke up or unable to connect"""
    def __init__(self, db_name: str):
        super().__init__(f'Could not connect to database {db_name}')


class ServerTimeoutError(DataBaseError):
    """Server timeout error if connection is lost"""
    def __init__(self, host:str):
        super().__init__(f'Server Timeout - No connection to database at {host}')


class DatabaseAlreadyExists(DataBaseError):
    """Error when database already exists"""
    def __init__(self, db_name: str):
        super().__init__(f'Database with the name {db_name} already exists')


class DatabaseNotExists(DataBaseError):
    """Error when database does not exist"""
    def __init__(self, db_name: str):
        super().__init__(f'Database with the name {db_name} doesn`t exists')


class CollectionAlreadyExists(DataBaseError):
    """Error if you try to create a collection that alrady exists"""
    def __init__(self, collection_name: str):
        super().__init__(f"Collection {collection_name} already exists")

#TODO: Use the PyMongo error
class PublicIDAlreadyExists(DuplicateKeyError):
    """Error if public_id inside database already exists"""
    def __init__(self, public_id: int):
        super().__init__(f"Object with this public id already exists: {public_id}")


#TODO: Use the Pymongo error
class NoDocumentFound(DataBaseError):
    """Error if no document was found"""
    def __init__(self, collection:str, public_id: int):
        super().__init__(f"No document with the id {public_id} was found inside {collection}")


class DocumentCouldNotBeDeleted(DataBaseError):
    """Error if document could not be deleted from database"""
    def __init__(self, collection: str, public_id: int):
        super().__init__(f"The document with the id {public_id} could not be deleted inside {collection}")
