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
Contains DocAPI Error Classes
"""
# -------------------------------------------------------------------------------------------------------------------- #

class DocapiError(Exception):
    """Base DocAPI Error"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# --------------------------------------------------- DOCAPI ERRORS -------------------------------------------------- #

class DocapiGetError(DocapiError):
    """
    Error raised when a GET-operation fails
    """
    def __init__(self, err: str):
        self.message = f"DocAPI-Error while GET: {err}"
        super().__init__(self.message)


class DocapiInsertError(DocapiError):
    """
    Error raised when an INSERT-operation fails
    """
    def __init__(self, err: str):
        self.message = f"DocAPI-Error while INSERT: {err}"
        super().__init__(self.message)


class DocapiUpdateError(DocapiError):
    """
    Error raised when an UPDATE-operation fails
    """
    def __init__(self, err: str):
        self.message = f"DocAPI-Error while UPDATE: {err}"
        super().__init__(self.message)


class DocapiDeleteError(DocapiError):
    """
    Error raised when a DELETE-operation fails
    """
    def __init__(self, err: str):
        self.message = f"DocAPI-Error while DELETE: {err}"
        super().__init__(self.message)
