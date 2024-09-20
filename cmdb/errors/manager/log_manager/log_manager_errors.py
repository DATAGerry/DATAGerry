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
"""This module contains the classes of all LogManager errors"""
from cmdb.errors.cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class LogManagerError(CMDBError):
    """Base ConfigFile Error"""
    def __init__(self, message: str):
        super().__init__(message)

# -------------------------------------------------- CmdbDAOErrors --------------------------------------------------- #

class LogManagerGetError(LogManagerError):
    """Raised when Exportd log could not be retrieved"""
    def __init__(self, err):
        super().__init__(f'Exportd log could not be retrieved! Error: {err}')


class LogManagerInsertError(LogManagerError):
    """Raised when Exportd log could not be inserted"""
    def __init__(self, err):
        super().__init__(f'Exportd log could not be inserted! Error: {err}')


class LogManagerDeleteError(LogManagerError):
    """Raised when Exportd log could not be deleted"""
    def __init__(self, err):
        super().__init__(f'Exportd log could not be deleted! Error: {err}')
