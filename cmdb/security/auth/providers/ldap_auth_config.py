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
import logging

from cmdb.security.auth.base_provider_config import BaseAuthProviderConfig

from cmdb.errors.provider import GroupMappingError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                       LdapAuthenticationProviderConfig - CLASS                                       #
# -------------------------------------------------------------------------------------------------------------------- #
class LdapAuthenticationProviderConfig(BaseAuthProviderConfig):
    """TODO: document"""

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
        },
        'groups': {
            'active': False,
            'searchfiltergroup': '(memberUid=%username%)',
            'mapping': []
        }
    }

    def __init__(self, active: bool = None, default_group: int = None, server_config: dict = None,
                 connection_config: dict = None, search: dict = None, groups: dict = None, *args, **kwargs):
        active = active or False
        self.default_group = int(default_group or LdapAuthenticationProviderConfig. \
                                 DEFAULT_CONFIG_VALUES.get('default_group'))
        self.server_config: dict = server_config or LdapAuthenticationProviderConfig. \
            DEFAULT_CONFIG_VALUES.get('server_config')
        self.connection_config: dict = connection_config or LdapAuthenticationProviderConfig. \
            DEFAULT_CONFIG_VALUES.get('connection_config')
        self.search: dict = search or LdapAuthenticationProviderConfig. \
            DEFAULT_CONFIG_VALUES.get('search')
        self.groups: dict = groups or LdapAuthenticationProviderConfig. \
            DEFAULT_CONFIG_VALUES.get('groups')
        super().__init__(active)


    def mapping(self, group_dn: str) -> int:
        """Get a group mapping by the group_dn"""
        try:
            return next(int(group['group_id']) for group in self.groups['mapping'] if
                        group['group_dn'].lower() == group_dn.lower())
        except StopIteration as err:
            raise GroupMappingError(str(err)) from err
