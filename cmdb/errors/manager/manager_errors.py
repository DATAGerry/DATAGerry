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
"""Contains Manager Error Classes"""
from ..cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class ManagerError(CMDBError):
    """Base Manager Error"""
    def __init__(self, message: str):
        super().__init__(message)

# --------------------------------------------- SPECIFIC DATABASE ERRORS --------------------------------------------- #


class ManagerGetError(ManagerError):
    """Manager exception for get operations"""
    def __init__(self, err: str):
        super().__init__(f'Error while GET: {err}')


class ManagerIterationError(ManagerError):
    """Manager exception for iteration operations"""
    def __init__(self, err: str):
        super().__init__(f'Error while ITERATION: {err}')


class ManagerInsertError(ManagerError):
    """Manager exception for insert operations"""
    def __init__(self, err: str):
        super().__init__(f'Error while INSERT: {err}')


#TODO: Replace with specific Manager errors
class ManagerUpdateError(ManagerError):
    """Manager exception for update operations"""
    def __init__(self, err: str):
        super().__init__(f'Error while UPDATE: {err}')


#TODO: Replace with specific Manager errors
class ManagerDeleteError(ManagerError):
    """Manager exception for delete operations"""
    def __init__(self, err: str):
        super().__init__(f'Error while DELETE: {err}')


class DisallowedActionError(ManagerError):
    """Manager exception when an illegal action is initiated"""
    def __init__(self, err: str):
        super().__init__(f'Disallowed Action: {err}')
