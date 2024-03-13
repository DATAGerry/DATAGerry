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
"""Contains DocAPI Error Classes"""
from ..cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class DocapiError(CMDBError):
    """Base DocAPI Error"""
    def __init__(self, message: str):
        super().__init__(message)

# --------------------------------------------- SPECIFIC DATABASE ERRORS --------------------------------------------- #

class NoPublicIDError(DocapiError):
    """Error if object has no public key and public key was'n removed over IGNORED_INIT_KEYS"""
    def __init__(self):
        super().__init__('The object has no general public id - look at the IGNORED_INIT_KEYS constant or the docs')


class DocapiGetError(DocapiError):
    """Error raised when a GET-operation fails"""
    def __init__(self, err: str):
        super().__init__(f'DocAPI-Error while GET: {err}')


class DocapiInsertError(DocapiError):
    """Error raised when an INSERT-operation fails"""
    def __init__(self, err: str):
        super().__init__(f'DocAPI-Error while INSERT: {err}')


class DocapiUpdateError(DocapiError):
    """Error raised when an UPDATE-operation fails"""
    def __init__(self, err: str):
        super().__init__(f'DocAPI-Error while UPDATE: {err}')


class DocapiDeleteError(DocapiError):
    """Error raised when a DELETE-operation fails"""
    def __init__(self, err: str):
        super().__init__(f'DocAPI-Error while DELETE: {err}')
