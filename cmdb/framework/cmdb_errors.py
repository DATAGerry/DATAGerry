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

class TypeNotFoundError(CMDBError):
    """TODO: document"""
    def __init__(self, type_id):
        self.message = f"Type with ID: {type_id} not found!"


class ObjectInsertError(CMDBError):
    """TODO: document"""
    def __init__(self, error):
        self.message = f'Object could not be inserted | Error {error.message} \n show into logs for details'


class ObjectDeleteError(CMDBError):
    """TODO: document"""
    def __init__(self, msg):
        self.message = f'Something went wrong during delete: {msg}'


class ExternalFillError(CMDBError):
    """Error if href of TypeExternalLink could not filled with input data"""
    def __init__(self, inputs, error):
        super().__init__()
        self.message = f'Href link do not fit with inputs: {inputs}, error: {error}'


class TypeReferenceLineFillError(CMDBError):
    """Error if summary line of TypeReferences could not filled with input data"""
    def __init__(self, inputs, error):
        super().__init__()
        self.message = f'Type reference summary line do not fit with inputs: {inputs}, error: {error}'


class FieldInitError(CMDBError):
    """Error if field could not be initialized"""
    def __init__(self, field_name):
        super().__init__()
        self.message = f'Field {field_name} could not be initialized'


class FieldNotFoundError(CMDBError):
    """Error if field do not exists"""

    def __init__(self, field_name, type_name):
        super().__init__()
        self.message = f'Field {field_name} was not found inside input_type: {type_name}'

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
