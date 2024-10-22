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
Contains CmdbDAO object error classes
"""
from ..cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class CmdbDAOError(CMDBError):
    """
    Base CmdbDAO Error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# -------------------------------------------------- CmdbDAO ERRORS -------------------------------------------------- #

class NoPublicIDError(CmdbDAOError):
    """
    Error if object has no public_id
    """
    def __init__(self):
        self.message = "The object has no public_id!"
        super().__init__(self.message)


#ERROR-FIX (not used)
class VersionTypeError(CmdbDAOError):
    """
    Error if update step of object version was wrong
    """
    def __init__(self, err: str):
        self.message = f"Error: {err}"
        super().__init__(self.message)


#ERROR-FIX (not used)
class NoVersionError(CmdbDAOError):
    """
    Error if object from models child class has no version number
    """
    def __init__(self, err: str):
        self.message = f"No version control. Error: {err}"
        super().__init__(self.message)


class RequiredInitKeyNotFoundError(CmdbDAOError):
    """
    Error if on of the given parameters is missing inside required init keys
    """
    def __init__(self, err: str):
        self.message = f"Initialization key was not found: {err}"
        super().__init__(self.message)
