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

# --------------------------------------------- SPECIFIC DATABASE ERRORS --------------------------------------------- #

class NoPublicIDError(CmdbDAOError):
    """
    Error if object has no public_id
    """
    def __init__(self):
        self.message = 'The object has no public_id!'
        super().__init__(self.message)


#TODO: ERROR-FIX (not used)
class VersionTypeError(CmdbDAOError):
    """
    Error if update step input was wrong
    """
    def __init__(self, level: str, update_input: str):
        self.message = f'The version type {update_input} update for {level} is wrong'
        super().__init__(self.message)


#TODO: ERROR-FIX (not used)
class NoVersionError(CmdbDAOError):
    """
    Error if object from models child class has no version number
    """
    def __init__(self, public_id: int):
        self.message = f'The object (ID: {public_id}) has no version control'
        super().__init__(self.message)


class RequiredInitKeyNotFoundError(CmdbDAOError):
    """
    Error if on of the given parameters is missing inside required init keys
    """
    def __init__(self, key_name: str):
        self.message = f'Following initialization key was not found inside the document: {key_name}'
        super().__init__(self.message)
