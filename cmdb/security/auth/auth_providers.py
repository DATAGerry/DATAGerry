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
from typing import ClassVar

from cmdb.security.auth.provider_config import AuthProviderConfig
from cmdb.security.security import SecurityManager
from cmdb.user_management import UserModel
from cmdb.user_management.managers.group_manager import GroupManager
from cmdb.user_management.managers.user_manager import UserManager

LOGGER = logging.getLogger(__name__)


class AuthenticationProvider:
    """Provider super class"""
    PASSWORD_ABLE: bool = True
    EXTERNAL_PROVIDER: bool = False
    PROVIDER_CONFIG_CLASS: ClassVar[AuthProviderConfig] = AuthProviderConfig

    def __init__(self, config: AuthProviderConfig = None, user_manager: UserManager = None,
                 group_manager: GroupManager = None, security_manager: SecurityManager = None):
        """
        Init constructor for provider classes
        Args:
            config: Configuration object
            user_manager: Instance of UserManager
            group_manager: Instance of GroupManager
        """
        self.user_manager = user_manager
        self.group_manager = group_manager
        self.security_manager = security_manager
        self.config = config or self.PROVIDER_CONFIG_CLASS(**self.PROVIDER_CONFIG_CLASS.DEFAULT_CONFIG_VALUES)

    def authenticate(self, user_name: str, password: str, **kwargs) -> UserModel:
        raise NotImplementedError

    def get_config(self) -> AuthProviderConfig:
        return self.config

    @classmethod
    def is_password_able(cls):
        """check if auth needs an password"""
        return cls.PASSWORD_ABLE

    @classmethod
    def get_name(cls):
        return cls.__qualname__


class NoValidAuthenticationProviderError(Exception):
    """Exception if auth provider do not exist"""

    def __init__(self, authenticator):
        self.message = "The Provider {} is not a valid authentication-provider".format(authenticator)


class NotPasswordAbleError(Exception):
    """Exception if application tries to generate a password for an not password_able class"""

    def __init__(self, provider):
        self.message = "The AuthenticationProvider {} is not password able".format(provider)
