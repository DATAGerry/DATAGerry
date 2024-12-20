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
from flask import current_app

from cmdb.manager.users_manager import UsersManager
from cmdb.manager.security_manager import SecurityManager

from cmdb.security.auth.base_authentication_provider import BaseAuthenticationProvider
from cmdb.security.auth.providers.local_auth_config import LocalAuthenticationProviderConfig
from cmdb.models.user_model.user import UserModel

from cmdb.errors.manager import ManagerGetError
from cmdb.errors.provider import AuthenticationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                          LocalAuthenticationProvider - CLASS                                         #
# -------------------------------------------------------------------------------------------------------------------- #
class LocalAuthenticationProvider(BaseAuthenticationProvider):
    """TODO: document"""
    PROVIDER_CONFIG_CLASS = LocalAuthenticationProviderConfig

    def __init__(self,
                 config: LocalAuthenticationProviderConfig = None,
                 security_manager: SecurityManager = None,
                 users_manager: UsersManager = None):
        super().__init__(config=config,
                         security_manager=security_manager,
                         users_manager=users_manager)


    def authenticate(self, user_name: str, password: str) -> UserModel:
        """TODO: document"""
        try:
            if current_app.cloud_mode:
                user: UserModel = self.users_manager.get_user_by({'email': user_name})
            else:
                user: UserModel = self.users_manager.get_user_by({'user_name': user_name})
        except ManagerGetError as err:
            raise AuthenticationError(str(err)) from err
        login_pass = self.security_manager.generate_hmac(password)

        if login_pass == user.password:
            return user

        raise AuthenticationError(f"{LocalAuthenticationProvider.get_name()}: Password did not matched with hmac!")


    def is_active(self) -> bool:
        """Local auth is always activated"""
        return True
