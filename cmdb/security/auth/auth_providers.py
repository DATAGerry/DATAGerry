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
from cmdb.security.auth.auth_errors import WrongUserPasswordError
from cmdb.security.auth.provider_base import AuthenticationProvider
from cmdb.utils import get_security_manager
from cmdb.utils.system_reader import SystemConfigReader

LOGGER = logging.getLogger(__name__)


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


