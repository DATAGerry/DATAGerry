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
import logging
from typing import List, ClassVar, Union

from cmdb.security.auth.auth_errors import AuthenticationProviderNotExistsError, AuthenticationProviderNotActivated, \
    AuthenticationError
from cmdb.security.auth.auth_providers import AuthenticationProvider
from cmdb.security.auth.auth_settings import AuthSettingsDAO
from cmdb.security.auth.providers.external_providers import LdapAuthenticationProvider
from cmdb.security.auth.providers.internal_providers import LocalAuthenticationProvider
from cmdb.security.auth.provider_config import AuthProviderConfig
from cmdb.user_management import UserManager, User
from cmdb.user_management.user_manager import UserManagerGetError
from cmdb.utils import SystemSettingsReader

LOGGER = logging.getLogger(__name__)


class AuthModule:
    """Authentication module class"""

    __pre_installed_providers: List[AuthenticationProvider] = [
        LocalAuthenticationProvider,
        LdapAuthenticationProvider
    ]

    __installed_providers: List[AuthenticationProvider] = __pre_installed_providers

    __DEFAULT_SETTINGS__ = {
        '_id': 'auth',
        'enable_external': True,
        'token_lifetime': 1400,
        'providers': [
            {
                'class_name': provider.get_name(),
                'config': provider.PROVIDER_CONFIG_CLASS.DEFAULT_CONFIG_VALUES
            } for provider in __installed_providers
        ]
    }

    def __init__(self, system_settings_reader: SystemSettingsReader):
        auth_settings_values = system_settings_reader. \
            get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__)
        self.__settings: AuthSettingsDAO = self.__init_settings(auth_settings_values)

    def __init_settings(self, auth_settings_values: dict) -> AuthSettingsDAO:
        """Merge default values with database entries"""
        for provider in self.get_installed_providers():
            LOGGER.debug(f'[AuthModule][__init_settings] Installed provider: {provider}')
            provider_config_list: List[dict] = auth_settings_values.get('providers')
            LOGGER.debug(f'[AuthModule][__init_settings] Database provider list: {provider_config_list}')
            if not any(p["class_name"] == provider.get_name() for p in provider_config_list):
                LOGGER.warning(f'[AuthModule][__init_settings] No config for: {provider.get_name()}')
                auth_settings_values['providers'].append(provider.PROVIDER_CONFIG_CLASS.DEFAULT_CONFIG_VALUES)
        return AuthSettingsDAO(**auth_settings_values)

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

    @staticmethod
    def get_provider_class(provider_name: str) -> AuthenticationProvider:
        """Get a specific provider class by class name"""
        return next(_ for _ in AuthModule.__installed_providers if _.__qualname__ == provider_name)

    @staticmethod
    def provider_exists(provider_name: str) -> bool:
        """Check if provider exists
        Notes:
            Checks for installation not activation!
        """
        try:
            AuthModule.get_provider_class(provider_name=provider_name)
            return True
        except StopIteration:
            return False

    @staticmethod
    def get_installed_providers() -> List[AuthenticationProvider]:
        """Get all installed providers as static list"""
        return AuthModule.__installed_providers

    @property
    def providers(self) -> List[AuthenticationProvider]:
        """Get all installed providers as property list"""
        return AuthModule.__installed_providers

    @property
    def settings(self) -> AuthSettingsDAO:
        """Get the current auth settings"""
        return self.__settings

    def get_provider(self, provider_name: str) -> AuthenticationProvider:
        """Get a initialized provider instance"""
        try:
            _provider_class_name: ClassVar[str] = provider_name
            if not AuthModule.provider_exists(provider_name=_provider_class_name):
                return None
            _provider_class: ClassVar[AuthenticationProvider] = AuthModule.get_provider_class(_provider_class_name)
            _provider_config_class: ClassVar[AuthProviderConfig] = _provider_class.PROVIDER_CONFIG_CLASS
            _provider_config_values: dict = self.settings.get_provider_settings(_provider_class_name) \
                .get('config', _provider_config_class.DEFAULT_CONFIG_VALUES)
            _provider_config_instance = _provider_config_class(**_provider_config_values)
            _provider_instance = _provider_class(config=_provider_config_instance)

            return _provider_instance
        except Exception as err:
            LOGGER.error(f'[AuthModule] {err}')
            return None

    def login(self, user_manager: UserManager, user_name: str, password: str) -> Union[User, None]:
        """
        Performs a login try with given username and password
        If the user is not found, iterate over all installed and activated providers
        Args:
            user_manager: Usermanager instance
            user_name: Name of the user
            password: Password

        Returns:
            User: instance if user was found and password was correct
            None: if something went wrong
        """
        user_name = user_name.lower()
        user_instance = None
        try:
            founded_user = user_manager.get_user_by_name(user_name=user_name)
            provider_class_name = founded_user.get_authenticator()
            LOGGER.debug(f'[AUTH] Founded user: {founded_user} with provider: {provider_class_name}')
            if not self.provider_exists(provider_class_name):
                raise AuthenticationProviderNotExistsError(provider_class_name)

            provider: ClassVar[AuthenticationProvider] = self.get_provider_class(provider_class_name)
            provider_config_class: ClassVar[str] = provider.PROVIDER_CONFIG_CLASS
            provider_config_settings = self.settings.get_provider_settings(provider.get_name())

            provider_config_instance = provider_config_class(**provider_config_settings)
            provider_instance = provider(config=provider_config_instance)
            if not provider_config_instance.is_active():
                raise AuthenticationProviderNotActivated(f'Provider {provider_class_name} is deactivated')
            if provider_instance.EXTERNAL_PROVIDER and not self.settings.enable_external:
                raise AuthenticationProviderNotActivated(f'External providers are deactivated')
            try:
                user_instance = provider_instance.authenticate(user_name, password)
            except AuthenticationError as ae:
                LOGGER.error(f'[LOGIN] User could not login: {ae}')

        except UserManagerGetError as umge:
            LOGGER.error(f'[AUTH] {user_name} not in database: {umge}')
            LOGGER.info(f'[AUTH] Check for other providers - request_user: {user_name}')
            # get installed providers
            provider_list = self.providers
            LOGGER.debug(f'[AUTH] Provider list: {provider_list}')
            external_enabled = self.settings.enable_external
            for provider in provider_list:
                LOGGER.debug(f'[AUTH] using provider: {provider}')
                provider_config_class = provider.PROVIDER_CONFIG_CLASS
                provider_settings = self.settings.get_provider_settings(provider.get_name())
                provider_config_instance = provider_config_class(**provider_settings)

                if not provider_config_instance.is_active():
                    continue
                if provider.EXTERNAL_PROVIDER and not self.settings.enable_external:
                    continue
                provider_instance = provider(config=provider_config_instance)
                try:
                    user_instance = provider_instance.authenticate(user_name, password)
                    if user_instance:
                        break
                except AuthenticationError as ae:
                    LOGGER.error(
                        f'[AUTH] User {user_name} could not validate with provider {provider}: {ae}')
                LOGGER.info(f'[AUTH] Provider instance: {provider_instance}')
        except Exception as e:
            import traceback
            traceback.print_exc()
            LOGGER.error(f'[AUTH] Error while login: {e}')
            return None
        finally:
            return user_instance
