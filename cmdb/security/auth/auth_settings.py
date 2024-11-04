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
from cmdb.security.token import DEFAULT_TOKEN_LIFETIME

from cmdb.errors.security.security_errors import AuthSettingsInitError
# -------------------------------------------------------------------------------------------------------------------- #

class AuthSettingsDAO:
    """Authentication data access object"""

    __DOCUMENT_IDENTIFIER = 'auth'
    __DEFAULT_EXTERNAL_ENABLED = False

    def __init__(self,
                 _id : str = None,
                 providers: list[dict] = None,
                 enable_external: bool = None,
                 token_lifetime: int = None):
        """TODO: document"""
        try:
            self._id: str = _id or AuthSettingsDAO.__DOCUMENT_IDENTIFIER
            self.providers: list[dict] = providers or []
            self.token_lifetime: int = token_lifetime or DEFAULT_TOKEN_LIFETIME
            self.enable_external: bool = enable_external or AuthSettingsDAO.__DEFAULT_EXTERNAL_ENABLED
        except Exception as err:
            raise AuthSettingsInitError(str(err)) from err


    def get_id(self) -> str:
        """Get the database document identifier"""
        return self._id


    def get_token_lifetime(self, default: int = DEFAULT_TOKEN_LIFETIME) -> int:
        """Get the lifetime parameter for tokens"""
        if not self.token_lifetime:
            self.token_lifetime = default
        return self.token_lifetime


    def get_provider_list(self) -> list[dict]:
        """Get the list of providers with config"""
        return self.providers


    def get_provider_settings(self, class_name: str) -> dict:
        """Get a specific provider list element by name"""
        return next(config for config in self.get_provider_list() if config['class_name'] == class_name)['config']
