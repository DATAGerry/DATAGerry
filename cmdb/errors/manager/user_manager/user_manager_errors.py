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
This module contains the classes of all UserManager errors
"""
from cmdb.errors.cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class UserManagerError(CMDBError):
    """
    Base UserManager error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# ----------------------------------------------- ObjectManager Errors ----------------------------------------------- #

class UserManagerGetError(UserManagerError):
    """
    Raised when UserManager could not retrieve an user
    """
    def __init__(self, err: str):
        self.message = f'User could not be retrieved. Error: {err}'
        super().__init__(self.message)


#TODO: ERROR-FIX (not used)
class UserManagerInsertError(UserManagerError):
    """
    Raised when UserManager could not create an user
    """
    def __init__(self, err):
        self.message = f'User could not be created. Error: {err}'
        super().__init__(self.message)


#TODO: ERROR-FIX (not used)
class UserManagerUpdateError(UserManagerError):
    """
    Raised when UserManager could not update an user
    """
    def __init__(self, err):
        self.message = f'User could not be updated. Error: {err}'
        super().__init__(self.message)


class UserManagerDeleteError(UserManagerError):
    """
    Raised when UserManager could not delete an user
    """
    def __init__(self, err):
        self.message = f'User could not be deleted. Error: {err}'
        super().__init__(self.message)
