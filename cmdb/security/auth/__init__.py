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
"""Basic Authentication Module"""
import logging
from typing import Type

from cmdb.errors.manager import ManagerGetError, ManagerInsertError
from cmdb.search import Query
from cmdb.security.auth.auth_errors import AuthenticationProviderNotExistsError, AuthenticationProviderNotActivated, \
    AuthenticationError
from cmdb.security.auth.auth_providers import AuthenticationProvider
from cmdb.security.auth.auth_settings import AuthSettingsDAO
from cmdb.security.auth.providers.external_providers import LdapAuthenticationProvider
from cmdb.security.auth.providers.internal_providers import LocalAuthenticationProvider
from cmdb.security.auth.provider_config import AuthProviderConfig
from cmdb.security.security import SecurityManager
from cmdb.user_management.managers.group_manager import GroupManager
from cmdb.user_management.managers.user_manager import UserManager, UserModel
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                      AuthModule                                                      #
# -------------------------------------------------------------------------------------------------------------------- #
class AuthModule:
    """Authentication module class"""

    __pre_installed_providers: list[AuthenticationProvider] = [
        LocalAuthenticationProvider,
        LdapAuthenticationProvider
    ]

    __installed_providers: list[AuthenticationProvider] = __pre_installed_providers

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

    def __init__(self, settings: dict, user_manager: UserManager = None,
                 group_manager: GroupManager = None, security_manager: SecurityManager = None):
        self.__settings: AuthSettingsDAO = self.__init_settings(settings)
        self.__user_manager = user_manager
        self.__group_manager = group_manager
        self.__security_manager = security_manager


    @staticmethod
    def __init_settings(auth_settings_values: dict) -> AuthSettingsDAO:
        """Merge default values with database entries"""
        provider_config_list: list[dict] = auth_settings_values.get('providers')
        installed_providers = AuthModule.get_installed_providers()
        for provider in installed_providers:
            if not any(p['class_name'] == provider.get_name() for p in provider_config_list):
                auth_settings_values['providers'].append(provider.PROVIDER_CONFIG_CLASS.DEFAULT_CONFIG_VALUES)
            else:
                provider_index = next(
                    (i for i, item in enumerate(provider_config_list) if item['class_name'] == provider.get_name()), -1)
                try:
                    auth_settings_values['providers'][provider_index]['config'] = provider.PROVIDER_CONFIG_CLASS(
                        **auth_settings_values['providers'][provider_index]['config']).__dict__
                except Exception as err:
                    LOGGER.error(
                        'Error while parsing auth provider settings for: %s: %s\n Fallback to default values!',provider.get_name(),err)
                    auth_settings_values['providers'][provider_index]['config'] = provider.PROVIDER_CONFIG_CLASS.DEFAULT_CONFIG_VALUES

        return AuthSettingsDAO(**auth_settings_values)


    @classmethod
    def register_provider(cls, provider: AuthenticationProvider) -> AuthenticationProvider:
        """Install a provider
        Notes:
            This only means that a provider is installed, not that the provider is used or activated!
        """
        cls.__installed_providers.append(provider)
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
    def get_provider_class(provider_name: str) -> 'AuthenticationProvider':
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


    @classmethod
    def get_installed_providers(cls) -> list['AuthenticationProvider']:
        """Get all installed providers as static list"""
        return cls.__installed_providers


    @classmethod
    def get_installed_internals(cls) -> list['AuthenticationProvider']:
        """Get all installed providers as static list"""
        return cls.__installed_providers


    @classmethod
    def get_installed_external(cls) -> list['AuthenticationProvider']:
        """Get all installed providers as static list"""
        return cls.__installed_providers


    @property
    def providers(self) -> list['AuthenticationProvider']:
        """Get all installed providers as property list"""
        return AuthModule.__installed_providers


    @property
    def settings(self) -> AuthSettingsDAO:
        """Get the current auth settings"""
        return self.__settings


    def get_provider(self, provider_name: str) -> AuthenticationProvider:
        """Get a initialized provider instance"""
        try:
            _provider_class_name: Type[str] = provider_name
            if not AuthModule.provider_exists(provider_name=_provider_class_name):
                return None
            _provider_class: Type[AuthenticationProvider] = AuthModule.get_provider_class(_provider_class_name)
            _provider_config_class: Type[AuthProviderConfig] = _provider_class.PROVIDER_CONFIG_CLASS
            _provider_config_values: dict = self.settings.get_provider_settings(_provider_class_name) \
                .get('config', _provider_config_class.DEFAULT_CONFIG_VALUES)
            _provider_config_instance = _provider_config_class(**_provider_config_values)
            _provider_instance = _provider_class(config=_provider_config_instance, user_manager=self.__user_manager,
                                                 group_manager=self.__group_manager,
                                                 security_manager=self.__security_manager)

            return _provider_instance
        except Exception as err:
            LOGGER.error('[AuthModule] %s', err)
            return None


    def login(self, user_name: str, password: str) -> UserModel:
        """
        Performs a login try with given username and password
        If the user is not found, iterate over all installed and activated providers
        Args:
            user_name: Name of the user
            password: Password

        Returns:
            UserModel: instance if user was found and password was correct
        """
        user_name = user_name.lower()

        try:
            user = self.__user_manager.get_by(Query({'user_name': user_name}))
            provider_class_name = user.authenticator

            if not self.provider_exists(provider_class_name):
                raise AuthenticationProviderNotExistsError(provider_class_name)

            provider: Type[AuthenticationProvider] = self.get_provider_class(provider_class_name)
            provider_config_class: Type[str] = provider.PROVIDER_CONFIG_CLASS
            provider_config_settings = self.settings.get_provider_settings(provider.get_name())

            provider_config_instance = provider_config_class(**provider_config_settings)
            provider_instance = provider(config=provider_config_instance, user_manager=self.__user_manager,
                                         group_manager=self.__group_manager, security_manager=self.__security_manager)
            if not provider_instance.is_active():
                raise AuthenticationProviderNotActivated(f'Provider {provider_class_name} is deactivated')
            if provider_instance.EXTERNAL_PROVIDER and not self.settings.enable_external:
                raise AuthenticationProviderNotActivated('External providers are deactivated')

            return provider_instance.authenticate(user_name, password)

        except ManagerGetError as err:
            # get installed providers
            provider_list = self.providers

            for provider in provider_list:

                provider_config_class = provider.PROVIDER_CONFIG_CLASS
                provider_settings = self.settings.get_provider_settings(provider.get_name())
                provider_config_instance = provider_config_class(**provider_settings)

                if not provider_config_instance.is_active():
                    continue
                if provider.EXTERNAL_PROVIDER and not self.settings.enable_external:
                    continue
                provider_instance = provider(config=provider_config_instance, user_manager=self.__user_manager,
                                             group_manager=self.__group_manager,
                                             security_manager=self.__security_manager)
                try:
                    return provider_instance.authenticate(user_name, password)
                except AuthenticationError:
                    continue
                except (ManagerGetError, ManagerInsertError) as error:
                    LOGGER.error('User found by provider but could not be inserted or found %s',error)
                    continue

            raise AuthenticationError('Unknown user could not login.') from err
