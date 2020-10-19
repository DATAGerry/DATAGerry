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

from datetime import datetime

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.security.auth.auth_errors import AuthenticationError
from cmdb.security.auth.auth_providers import AuthenticationProvider
from cmdb.security.auth.provider_config import AuthProviderConfig
from cmdb.security.auth.provider_config_form import AuthProviderConfigForm, AuthProviderConfigFormEntry, \
    AuthProviderConfigFormSection
from cmdb.user_management import User, UserManager
from cmdb.user_management.user_manager import UserManagerGetError, UserManagerInsertError
from cmdb.utils.system_config import SystemConfigReader

LOGGER = logging.getLogger(__name__)


class LdapAuthenticationProviderConfig(AuthProviderConfig):
    DEFAULT_CONFIG_VALUES = {
        'active': False,
        'default_group': 2,
        'server_config': {
            'host': 'localhost',
            'port': 389,
            'use_ssl': False
        },
        'connection_config': {
            'user': 'cn=reader,dc=example,dc=com',
            'password': 'secret1234',
            'version': 3
        },
        'search': {
            'basedn': 'dc=example,dc=com',
            'searchfilter': '(uid=%username%)'
        }
    }

    PROVIDER_CONFIG_FORM = AuthProviderConfigForm(
        entries=[
            AuthProviderConfigFormEntry(name='active', type='checkbox',
                                        default=DEFAULT_CONFIG_VALUES.get('active')),
            AuthProviderConfigFormEntry(name='default_group', type='number',
                                        default=DEFAULT_CONFIG_VALUES.get('default_group'))
        ],
        sections=[
            AuthProviderConfigFormSection(name='server_config', entries=[
                AuthProviderConfigFormEntry(name='host', type='text',
                                            default=DEFAULT_CONFIG_VALUES.get('server_config').get('host')),
                AuthProviderConfigFormEntry(name='port', type='number',
                                            default=DEFAULT_CONFIG_VALUES.get('server_config').get('port')),
                AuthProviderConfigFormEntry(name='use_ssl', type='checkbox',
                                            default=DEFAULT_CONFIG_VALUES.get('server_config').get('use_ssl'))
            ]),
            AuthProviderConfigFormSection(name='connection_config', entries=[
                AuthProviderConfigFormEntry(name='user', type='text',
                                            default=DEFAULT_CONFIG_VALUES.get('connection_config').get('user')),
                AuthProviderConfigFormEntry(name='password', type='password', force_hidden=True,
                                            default=DEFAULT_CONFIG_VALUES.get('connection_config').get('password')),
                AuthProviderConfigFormEntry(name='version', type='number',
                                            default=DEFAULT_CONFIG_VALUES.get('connection_config').get('version'))
            ]),
            AuthProviderConfigFormSection(name='search', entries=[
                AuthProviderConfigFormEntry(name='basedn', type='text',
                                            default=DEFAULT_CONFIG_VALUES.get('search').get('basedn')),
                AuthProviderConfigFormEntry(name='searchfilter', type='text',
                                            description='%username% will be inserted from the login data',
                                            default=DEFAULT_CONFIG_VALUES.get('search').get('searchfilter'))
            ])
        ]
    )

    def __init__(self, active: bool, default_group: int, server_config: dict, connection_config: dict, search: dict,
                 **kwargs):
        self.default_group = default_group
        self.server_config: dict = server_config
        self.connection_config: dict = connection_config
        self.search: dict = search
        super(LdapAuthenticationProviderConfig, self).__init__(active, **kwargs)


class LdapAuthenticationProvider(AuthenticationProvider):
    from ldap3 import Server, Connection
    PASSWORD_ABLE: bool = False
    EXTERNAL_PROVIDER: bool = True
    PROVIDER_CONFIG_CLASS = LdapAuthenticationProviderConfig

    def __init__(self, config: LdapAuthenticationProviderConfig = None):

        super(LdapAuthenticationProvider, self).__init__(config)

        self.__ldap_server = LdapAuthenticationProvider.Server(**self.config.server_config)
        self.__ldap_connection = LdapAuthenticationProvider.Connection(self.__ldap_server,
                                                                       **self.config.connection_config)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__ldap_connection:
            self.__ldap_connection.unbind()

    def connect(self) -> bool:
        return self.__ldap_connection.bind()

    def authenticate(self, user_name: str, password: str, **kwargs) -> User:
        __dbm = DatabaseManagerMongo(
            **SystemConfigReader().get_all_values_from_section('Database')
        )
        __user_manager = UserManager(__dbm)
        try:
            ldap_connection_status = self.connect()
            LOGGER.debug(f'[LdapAuthenticationProvider] Connection status: {ldap_connection_status}')
        except Exception as e:
            LOGGER.error(f'[LdapAuthenticationProvider] Failed to connect to LDAP server - error: {e}')
            raise AuthenticationError(LdapAuthenticationProvider.get_name(), e)
        ldap_search_filter = self.config.search['searchfilter'].replace("%username%", user_name)
        LOGGER.debug(f'[LdapAuthenticationProvider] Search Filter: {ldap_search_filter}')
        search_result = self.__ldap_connection.search(self.config.search['basedn'], ldap_search_filter)
        LOGGER.debug(f'[LdapAuthenticationProvider] Search result: {search_result}')

        if not search_result:
            raise AuthenticationError(LdapAuthenticationProvider.get_name(), 'No matching entry')

        for entry in self.__ldap_connection.entries:
            LOGGER.debug(f'[LdapAuthenticationProvider] Entry: {entry}')
            entry_dn = entry.entry_dn
            try:
                entry_connection_result = LdapAuthenticationProvider.Connection(self.__ldap_server, entry_dn, password,
                                                                                auto_bind=True)
                LOGGER.debug(f'[LdapAuthenticationProvider] User connection result: {entry_connection_result}')
            except Exception as e:
                LOGGER.error(f'[LdapAuthenticationProvider] User auth result: {e}')
                raise AuthenticationError(LdapAuthenticationProvider.get_name(), e)

        # Check if user exists
        try:
            user_instance: User = __user_manager.get_user_by_name(user_name=user_name)
        except UserManagerGetError as umge:
            LOGGER.warning(f'[LdapAuthenticationProvider] User exists on LDAP but not in database: {umge}')
            LOGGER.info(f'[LdapAuthenticationProvider] Try creating user: {user_name}')
            try:
                new_user_data = dict()
                new_user_data['public_id'] = __user_manager.get_new_id(User.COLLECTION)
                new_user_data['user_name'] = user_name
                new_user_data['group_id'] = self.config.default_group
                new_user_data['registration_time'] = datetime.utcnow()
                new_user_data['authenticator'] = LdapAuthenticationProvider.get_name()
                new_user = User(**new_user_data)
            except Exception as e:
                LOGGER.debug(f'[LdapAuthenticationProvider] {e}')
                raise AuthenticationError(LdapAuthenticationProvider.get_name(), e)
            LOGGER.debug(f'[LdapAuthenticationProvider] New user was init')
            try:
                user_id = __user_manager.insert_user(new_user)
            except UserManagerInsertError as umie:
                LOGGER.debug(f'[LdapAuthenticationProvider] {umie}')
                raise AuthenticationError(LdapAuthenticationProvider.get_name(), umie)
            try:
                user_instance: User = __user_manager.get_user(public_id=user_id)
            except UserManagerGetError as umge:
                LOGGER.debug(f'[LdapAuthenticationProvider] {umge}')
                raise AuthenticationError(LdapAuthenticationProvider.get_name(), umge)
        return user_instance

    def is_active(self) -> bool:
        return self.config.active
