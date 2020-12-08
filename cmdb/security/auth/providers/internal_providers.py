# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2020 NETHINKS GmbH
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

import logging

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.manager import ManagerGetError
from cmdb.security.auth.auth_providers import AuthenticationProvider
from cmdb.security.auth.auth_errors import AuthenticationError
from cmdb.security.auth.provider_config import AuthProviderConfig
from cmdb.user_management import UserModel
from cmdb.user_management.managers.user_manager import UserManager
from cmdb.security.security import SecurityManager
from cmdb.utils.system_config import SystemConfigReader

LOGGER = logging.getLogger(__name__)


class LocalAuthenticationProviderConfig(AuthProviderConfig):

    def __init__(self, active: bool, **kwargs):
        super(LocalAuthenticationProviderConfig, self).__init__(active, **kwargs)


class LocalAuthenticationProvider(AuthenticationProvider):
    PROVIDER_CONFIG_CLASS = LocalAuthenticationProviderConfig

    def __init__(self, config: LocalAuthenticationProviderConfig = None, *args, **kwargs):
        super(LocalAuthenticationProvider, self).__init__(config)

    def authenticate(self, user_name: str, password: str, **kwargs) -> UserModel:
        __dbm = DatabaseManagerMongo(
            **SystemConfigReader().get_all_values_from_section('Database')
        )
        __scm = SecurityManager(__dbm)
        __user_manager = UserManager(__dbm)
        LOGGER.info(f'[LocalAuthenticationProvider] Try login for user {user_name}')
        try:
            user: UserModel = __user_manager.get_by({'user_name': user_name})
        except ManagerGetError as umge:
            raise AuthenticationError(LocalAuthenticationProvider.get_name(), umge.message)
        login_pass = __scm.generate_hmac(password)
        if login_pass == user.password:
            return user
        raise AuthenticationError(LocalAuthenticationProvider.get_name(), 'UserModel not exists')

    def is_active(self) -> bool:
        """Local auth is always activated"""
        return True
