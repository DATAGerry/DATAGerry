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
This module contains the classes of all ObjectssManager errors
"""
from cmdb.errors.cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class ObjectManagerError(CMDBError):
    """
    Base ObjectsManager error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# ---------------------------------------------- ObjectsManager Errors ----------------------------------------------- #

class ObjectManagerInsertError(ObjectManagerError):
    """
    Raised when ObjectsManager could not insert an object
    """
    def __init__(self, err: str):
        self.message = f"Object could not be inserted. Error: {err}"
        super().__init__(self.message)


class ObjectManagerDeleteError(ObjectManagerError):
    """
    Raised when ObjectsManager could not delete an object
    """
    def __init__(self, err: str):
        self.message = f"Object could not be deleted. Error: {err}"
        super().__init__(self.message)


class ObjectManagerUpdateError(ObjectManagerError):
    """
    Raised when ObjectsManager could not update an object
    """
    def __init__(self, err: str):
        self.message = f"Object could not be updated. Error: {err}"
        super().__init__(self.message)


class ObjectManagerGetError(ObjectManagerError):
    """
    Raised when ObjectsManager could not retrieve an object
    """
    def __init__(self, err: str):
        self.message = f"Object could not be retrieved. Error: {err}"
        super().__init__(self.message)


class ObjectManagerInitError(ObjectManagerError):
    """
    Raised when ObjectsManager could not initialise an object
    """
    def __init__(self, err: str):
        self.message = f"Object could not be initialised. Error: {err}"
        super().__init__(self.message)


class TypeNotSetError(ObjectManagerError):
    """
    Raised when the type_id was not set for an object
    """
    def __init__(self):
        self.message = "The object has no type_id!"
        super().__init__(self.message)
