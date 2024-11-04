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
Contains Security Error Classes
"""
from ..cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class SecurityError(CMDBError):
    """
    Base Security Error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# -------------------------------------------------- SECURITY ERRORS ------------------------------------------------- #

class TokenValidationError(SecurityError):
    """
    Raised when a jwt token could not be decoded
    """
    def __init__(self, err: str):
        self.message = f"Error while decode the token operation - Error: {err}"
        super().__init__(self.message)


class AccessDeniedError(SecurityError):
    """
    Raised when access was denied
    """
    def __init__(self, err: str):
        self.message = f"Access was denied. Error: {err}"
        super().__init__(self.message)


class RightNotFoundError(SecurityError):
    """
    Raised when a right was not found
    """
    def __init__(self, err: str):
        self.message = f"Right was not found inside the group. {err}"
        super().__init__(self.message)


class InvalidLevelRightError(SecurityError):
    """
    Raised when a right level is not valid
    """
    def __init__(self, err: str):
        self.message = f"Invalid right level. Level does not exist: {err}"
        super().__init__(self.message)


class MinLevelRightError(SecurityError):
    """
    Raised when min level for a right was violated
    """
    def __init__(self, err: str):
        self.message = f"Min level for the right has been violated. Error: {err}"
        super().__init__(self.message)


class MaxLevelRightError(SecurityError):
    """
    Raised when max level for a right was violated
    """
    def __init__(self, err: str):
        self.message = f"Max level for the right has been violated. Error: {err}"
        super().__init__(self.message)


class AuthSettingsInitError(SecurityError):
    """
    Raised when AuthSettingsDAO could not be initialised
    """
    def __init__(self, err: str):
        self.message = f"Could not initialise AuthSettingsDAO. Error: {err}"
        super().__init__(self.message)
