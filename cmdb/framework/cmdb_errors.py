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
"""TODO: document"""
from cmdb.utils.error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class ObjectInsertError(CMDBError):
    """TODO: document"""
    def __init__(self, error):
        self.message = f'Object could not be inserted | Error {error.message} \n show into logs for details'


class ObjectDeleteError(CMDBError):
    """TODO: document"""
    def __init__(self, msg):
        self.message = f'Something went wrong during delete: {msg}'

# -------------------------------------------------- CMDB BASE ERROS ------------------------------------------------- #

class ManagerInitError(CMDBError):
    "TODO: document"
    def __init__(self, err):
        self.message = f'Error while INIT operation - E: ${err}'


class ManagerGetError(CMDBError):
    "TODO: document"
    def __init__(self, err):
        self.message = f'Error while GET operation - E: ${err}'


class ManagerInsertError(CMDBError):
    "TODO: document"
    def __init__(self, err):
        self.message = f'Error while INSERT operation - E: ${err}'


class ManagerUpdateError(CMDBError):
    "TODO: document"
    def __init__(self, err):
        self.message = f'Error while UPDATE operation - E: ${err}'


class ManagerDeleteError(CMDBError):
    "TODO: document"
    def __init__(self, err):
        self.message = f'Error while DELETE operation - E: ${err}'


# ------------------------------------------------- OBJECT EXCEPTIONS ------------------------------------------------ #

class ObjectManagerInitError(ManagerInitError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


class ObjectManagerGetError(ManagerGetError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)

class ObjectManagerInsertError(ManagerInsertError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


class ObjectManagerUpdateError(ManagerUpdateError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


class ObjectManagerDeleteError(ManagerDeleteError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)
