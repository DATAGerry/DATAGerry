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
"""This module contains all error classes for Types"""
from ..cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class CmdbTypeError(CMDBError):
    """Base ConfigFile Error"""
    def __init__(self, message: str):
        super().__init__(message)

# -------------------------------------------------------------------------------------------------------------------- #

class TypeNotFoundError(CmdbTypeError):
    """TODO: document"""
    def __init__(self, type_id: int):
        super().__init__(f"Type with ID: {type_id} not found!")


class ExternalFillError(CmdbTypeError):
    """Error if href of TypeExternalLink could not filled with input data"""
    def __init__(self, inputs):
        super().__init__(f'Href link do not fit with inputs: {inputs}!')


class TypeReferenceLineFillError(CmdbTypeError):
    """Error if summary line of TypeReferences could not filled with input data"""
    def __init__(self, inputs):
        super().__init__(f'Type reference summary line do not fit with inputs: {inputs}!')


class FieldNotFoundError(CmdbTypeError):
    """Error if field do not exists"""
    def __init__(self, field_name: str = None, type_name: str = None):
        super().__init__(f"Field '{field_name}' was not found inside input_type: '{type_name}'!")


class FieldInitError(CmdbTypeError):
    """Error if field could not be initialized"""
    def __init__(self, field_name:str = None):
        super().__init__(f"Field '{field_name}' could not be initialized")
