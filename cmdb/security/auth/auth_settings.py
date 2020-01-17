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
import logging
from typing import List, ClassVar

from cmdb.security.auth.auth_providers import AuthenticationProvider
from cmdb.security.auth.provider_config import AuthProviderConfig

LOGGER = logging.getLogger(__name__)


class AuthSettingsDAO:
    """Authentication data access object"""

    __DOCUMENT_IDENTIFIER = 'auth'
    __DEFAULT_EXTERNAL_ENABLED = False

    def __init__(self, providers: List[dict] = None, enable_external: bool = None, *args, **kwargs):

        self._id: str = AuthSettingsDAO.__DOCUMENT_IDENTIFIER
        self.providers: List[dict] = []
        self.__init_provider_list(providers=providers)
        self.enable_external: bool = enable_external or AuthSettingsDAO.__DEFAULT_EXTERNAL_ENABLED

    def __init_provider_list(self, providers: List[dict]):
        from cmdb.security.auth import AuthModule
        for provider in providers:
            try:
                _provider_class_name: ClassVar[str] = provider.get('class_name')
                if not AuthModule.provider_exists(provider_name=_provider_class_name):
                    continue
                _provider_class: ClassVar[AuthenticationProvider] = AuthModule.get_provider_class(_provider_class_name)
                _provider_config_class: ClassVar[AuthProviderConfig] = _provider_class.PROVIDER_CONFIG_CLASS
                _provider_config_values: dict = provider.get('config', _provider_config_class.DEFAULT_CONFIG_VALUES)

                _provider_config_instance = _provider_config_class(**_provider_config_values)
                _provider_instance: AuthenticationProvider = _provider_class(config=_provider_config_instance)
                LOGGER.debug(f'[AuthSettingsDAO] _provider_instance: {_provider_instance.__dict__}')
                self.providers.append({
                    'class_name': _provider_instance.get_name(),
                    'config': _provider_instance.get_config().__dict__
                })
            except Exception as err:
                LOGGER.error(f'[AuthSettingsDAO] {err}')
                continue

    def get_id(self) -> str:
        """Get the database document identifier"""
        return self._id

    def get_provider_list(self) -> List[dict]:
        """Get the list of providers with config"""
        return self.providers

    def get_provider_settings(self, class_name: str) -> dict:
        """Get a specific provider list element by name"""
        return next(_ for _ in self.get_provider_list() if _['class_name'] == class_name)['config']
