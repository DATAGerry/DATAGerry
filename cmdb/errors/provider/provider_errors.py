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
Contains Provider Error Classes
"""
# -------------------------------------------------------------------------------------------------------------------- #

class ProviderError(Exception):
    """
    Base Provider Error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# -------------------------------------------------- PROVIDER ERRORS ------------------------------------------------- #

class GroupMappingError(ProviderError):
    """
    Raised if a LDAP mapping was not found or failed
    """
    def __init__(self, err: str):
        self.message = f"LDAP mapping failed or was not found. Error: {err}"
        super().__init__(self.message)


class AuthenticationProviderNotActivated(ProviderError):
    """
    Raised if auth provider is not activated
    """
    def __init__(self, err: str):
        self.message = f"Auth provider not activated. Error: {err}"
        super().__init__(self.message)


class AuthenticationProviderNotFoundError(ProviderError):
    """
    Raised if auth provider does not exist
    """
    def __init__(self, err: str):
        self.message = f"Provider does not exist or is not installed. Error: {err}"
        super().__init__(self.message)


class AuthenticationError(ProviderError):
    """
    Raised when user could not be authenticated via provider
    """
    def __init__(self, err: str):
        self.message = f"Could not authenticate via provider. Error: {err}"
        super().__init__(self.message)
