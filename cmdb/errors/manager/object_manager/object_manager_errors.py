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
"""This module contains the classes of all ObjectManager errors"""
from cmdb.errors.cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class ObjectManagerError(CMDBError):
    """Base ConfigFile Error"""
    def __init__(self, message: str):
        super().__init__(message)

# -------------------------------------------------- CmdbDAOErrors --------------------------------------------------- #

class ObjectManagerInsertError(ObjectManagerError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(f'Object could not be inserted. Error: {err}')


class ObjectManagerDeleteError(ObjectManagerError):
    """TODO: document"""
    def __init__(self, public_id: int = None, err = None):
        super().__init__(f'Object with public_id: {public_id} could not be deleted. Error: {err}')


#TODO: Provide the public_id of the object
class ObjectManagerUpdateError(ObjectManagerError):
    """Raised when ObjectManager could not update an object"""
    def __init__(self, err):
        super().__init__(f'Object could not be updated. Error: {err}')


#TODO: Provide the public_id of the object
class ObjectManagerGetError(ObjectManagerError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(f'Object could not be retrieved. Error: {err}')


class ObjectManagerInitError(ObjectManagerError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(f'Object could not be initialised. Error: {err}')
