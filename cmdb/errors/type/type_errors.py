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
This module contains all error classes for CmdbTypes
"""
from ..cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class CmdbTypeError(CMDBError):
    """
    Base CmdbType Error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# -------------------------------------------------- CmdbType ERRORS ------------------------------------------------- #

class TypeNotFoundError(CmdbTypeError):
    """
    Raised when a type was not found
    """
    def __init__(self, type_id: int):
        self.message = f"Type with ID: {type_id} not found!"
        super().__init__(self.message)


#TODO: ERROR-FIX (never used)
class ExternalFillError(CmdbTypeError):
    """
    Raised if href of TypeExternalLink could not filled with input data
    """
    def __init__(self, href: str):
        self.message = f"Href link do not fit with inputs: {href}!"
        super().__init__(self.message)


class TypeReferenceLineFillError(CmdbTypeError):
    """
    Raised if summary line of TypeReferences could not filled with input data
    """
    def __init__(self, line: str):
        self.message = f"Type reference summary line do not fit with inputs: {line}!"
        super().__init__(self.message)


class FieldNotFoundError(CmdbTypeError):
    """
    Raised if field do not exists
    """
    def __init__(self, field_name: str = None):
        self.message = f"Field '{field_name}' was not found!"
        super().__init__(self.message)


class FieldInitError(CmdbTypeError):
    """
    Error if field could not be initialized
    """
    def __init__(self, field_name:str):
        self.message = f"Field '{field_name}' could not be initialized"
        super().__init__(self.message)
