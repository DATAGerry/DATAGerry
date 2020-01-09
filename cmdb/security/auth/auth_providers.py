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

from cmdb.data_storage.database_manager import DatabaseManagerMongo
# from cmdb.security.auth.auth_errors import WrongUserPasswordError
# from cmdb.security.auth.provider_base import AuthenticationProvider
from cmdb.utils import get_security_manager
from cmdb.utils.system_reader import SystemConfigReader

LOGGER = logging.getLogger(__name__)


class AuthenticationProvider:
    PASSWORD_ABLE = True

    def authenticate(self, user, password: str, **kwargs) -> bool:
        raise NotImplementedError

    def generate_password(self, *args, **kwargs) -> (str, bytearray):
        if not self.is_password_able():
            raise NotPasswordAbleError(self.get_name())
        raise NotImplementedError

    @classmethod
    def is_password_able(cls):
        """check if auth needs an password"""
        return cls.PASSWORD_ABLE

    @classmethod
    def get_name(cls):
        return cls.__qualname__


class LocalAuthenticationProvider(AuthenticationProvider):

    def __init__(self):
        self.scr = SystemConfigReader()
        self.__dbm = DatabaseManagerMongo(
            **self.scr.get_all_values_from_section('Database')
        )
        super(AuthenticationProvider, self).__init__()

    def authenticate(self, user, password: str, **kwargs) -> bool:
        security_manager = get_security_manager(self.__dbm)
        login_pass = security_manager.generate_hmac(password)
        if login_pass == user.get_password():
            return True
        raise WrongUserPasswordError(user.get_username())


class NoValidAuthenticationProviderError(Exception):
    """Exception if auth provider do not exist"""

    def __init__(self, authenticator):
        self.message = "The Provider {} is not a valid authentication-provider".format(authenticator)


class WrongUserPasswordError(Exception):
    """Exception if wrong user password"""

    def __init__(self, user):
        self.message = "The password for the user {} was wrong!".format(user)


class NotPasswordAbleError(Exception):
    """Exception if application tries to generate a password for an not password_able class"""

    def __init__(self, provider):
        self.message = "The AuthenticationProvider {} is not password able".format(provider)
