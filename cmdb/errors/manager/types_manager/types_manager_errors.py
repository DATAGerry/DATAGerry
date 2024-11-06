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
This module contains the classes of all TypesManager errors
"""
# -------------------------------------------------------------------------------------------------------------------- #

class TypesManagerError(Exception):
    """
    Base UsersManager error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               TypesManagerError Errors                                               #
# -------------------------------------------------------------------------------------------------------------------- #

class TypesManagerGetError(TypesManagerError):
    """
    Raised when TypesManager could not retrieve a type
    """
    def __init__(self, err: str):
        self.message = f"Type could not be retrieved. Error: {err}"
        super().__init__(self.message)


class TypesManagerInsertError(TypesManagerError):
    """
    Raised when TypesManager could not create a type
    """
    def __init__(self, err: str):
        self.message = f"Type could not be created. Error: {err}"
        super().__init__(self.message)


class TypesManagerUpdateError(TypesManagerError):
    """
    Raised when TypesManager could not update a type
    """
    def __init__(self, err: str):
        self.message = f"Type could not be updated. Error: {err}"
        super().__init__(self.message)


class TypesManagerDeleteError(TypesManagerError):
    """
    Raised when TypesManager could not delete a type
    """
    def __init__(self, err: str):
        self.message = f"Type could not be deleted. Error: {err}"
        super().__init__(self.message)


class TypesManagerInitError(TypesManagerError):
    """
    Raised when TypesManager could not initialise a type
    """
    def __init__(self, err: str):
        self.message = f"Type could not be initialised. Error: {err}"
        super().__init__(self.message)
