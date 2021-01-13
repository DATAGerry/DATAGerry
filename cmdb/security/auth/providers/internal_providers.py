# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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

from cmdb.manager import ManagerGetError
from cmdb.search import Query
from cmdb.security.auth.auth_providers import AuthenticationProvider
from cmdb.security.auth.auth_errors import AuthenticationError
from cmdb.security.auth.provider_config import AuthProviderConfig
from cmdb.user_management import UserModel
from cmdb.user_management.managers.group_manager import GroupManager
from cmdb.user_management.managers.user_manager import UserManager
from cmdb.security.security import SecurityManager

LOGGER = logging.getLogger(__name__)


class LocalAuthenticationProviderConfig(AuthProviderConfig):

    def __init__(self, active: bool = None, **kwargs):
        super(LocalAuthenticationProviderConfig, self).__init__(active, **kwargs)


class LocalAuthenticationProvider(AuthenticationProvider):
    PROVIDER_CONFIG_CLASS = LocalAuthenticationProviderConfig

    def __init__(self, config: LocalAuthenticationProviderConfig = None, user_manager: UserManager = None,
                 group_manager: GroupManager = None, security_manager: SecurityManager = None):
        super(LocalAuthenticationProvider, self).__init__(config=config, user_manager=user_manager,
                                                          group_manager=group_manager,
                                                          security_manager=security_manager)

    def authenticate(self, user_name: str, password: str, *args, **kwargs) -> UserModel:
        try:
            user: UserModel = self.user_manager.get_by(Query({'user_name': user_name}))
        except ManagerGetError as err:
            raise AuthenticationError(LocalAuthenticationProvider.get_name(), err.message)
        login_pass = self.security_manager.generate_hmac(password)
        if login_pass == user.password:
            return user
        raise AuthenticationError(LocalAuthenticationProvider.get_name(), 'Password did not matched with hmac!')

    def is_active(self) -> bool:
        """Local auth is always activated"""
        return True
