# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Basic Authentication Module"""
from typing import List

from cmdb.security.auth.auth_providers import AuthenticationProvider
from cmdb.security.auth.auth_settings import AuthSettingsDAO
from cmdb.security.auth.providers.external_providers import LdapAuthenticationProvider
from cmdb.security.auth.providers.internal_providers import LocalAuthenticationProvider


class AuthModule:
    """Authentication module class"""
    __pre_installed_providers: List[AuthenticationProvider] = [
        LocalAuthenticationProvider,
        LdapAuthenticationProvider
    ]
    __installed_providers: List[AuthenticationProvider] = __pre_installed_providers

    def __init__(self, settings: AuthSettingsDAO = None):
        self.__settings: AuthSettingsDAO = settings

    @classmethod
    def register_provider(cls, provider: AuthenticationProvider) -> AuthenticationProvider:
        """Install a provider
        Notes:
            This only means that a provider is installed, not that the provider is used or activated!
        """
        AuthModule.__installed_providers.append(provider)
        return provider

    @classmethod
    def unregister_provider(cls, provider: AuthenticationProvider) -> bool:
        """Uninstall a provider"""
        try:
            AuthModule.__installed_providers.remove(provider)
            return True
        except ValueError:
            return False

    @property
    def providers(self) -> List[AuthenticationProvider]:
        """Get all installed providers as property list"""
        return AuthModule.__installed_providers

    def get_provider(self, provider_name: str) -> AuthenticationProvider:
        """Get a specific provider by class name"""
        return next(_ for _ in self.providers if _.__qualname__ == provider_name)

    def provider_exists(self, provider_name: str) -> bool:
        """Check if provider exists
        Notes:
            Checks for installation not activation!
        """
        try:
            self.get_provider(provider_name=provider_name)
            return True
        except StopIteration:
            return False

    @property
    def settings(self) -> AuthSettingsDAO:
        """Get the current auth settings"""
        return self.__settings
