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

from cmdb.manager.users_manager import UsersManager
from cmdb.manager.security_manager import SecurityManager

from cmdb.security.auth.base_provider_config import BaseAuthProviderConfig
from cmdb.models.user_model.user import UserModel
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                          BaseAuthenticationProvider - CLASS                                          #
# -------------------------------------------------------------------------------------------------------------------- #
class BaseAuthenticationProvider:
    """Provider super class"""
    PASSWORD_ABLE: bool = True
    EXTERNAL_PROVIDER: bool = False
    PROVIDER_CONFIG_CLASS: 'BaseAuthProviderConfig' = BaseAuthProviderConfig

    def __init__(self,
                 config: BaseAuthProviderConfig = None,
                 security_manager: SecurityManager = None,
                 users_manager: UsersManager = None):
        """
        Init constructor for provider classes
        Args:
            config: Configuration object
        """
        self.users_manager = users_manager
        self.security_manager = security_manager
        self.config = config or self.PROVIDER_CONFIG_CLASS(**self.PROVIDER_CONFIG_CLASS.DEFAULT_CONFIG_VALUES)


    def authenticate(self, user_name: str, password: str) -> UserModel:
        """TODO: document"""
        raise NotImplementedError


    def get_config(self) -> BaseAuthProviderConfig:
        """TODO: document"""
        return self.config


    @classmethod
    def is_password_able(cls):
        """check if auth needs an password"""
        return cls.PASSWORD_ABLE


    @classmethod
    def get_name(cls):
        """TODO: document"""
        return cls.__qualname__
