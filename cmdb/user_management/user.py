# dataGerry - OpenSource Enterprise CMDB
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

from cmdb.user_management.user_base import UserManagementBase
from cmdb.utils.error import CMDBError


class User(UserManagementBase):
    COLLECTION = 'management.users'
    REQUIRED_INIT_KEYS = ['user_name']
    INDEX_KEYS = [
        {'keys': [('user_name', UserManagementBase.ASCENDING)], 'name': 'user_name', 'unique': True}
    ]

    def __init__(self, user_name, group_id, registration_time, password=None,
                 first_name=None, last_name=None, email=None, authenticator='LocalAuthenticationProvider', **kwargs):
        self.user_name = user_name
        self.password = password
        self.group_id = group_id
        self.authenticator = authenticator
        if email is None or email == "":
            self.email = ""
        else:
            self.email = self.__validate_email(email)
        self.registration_time = registration_time
        self.first_name = first_name
        self.last_name = last_name
        super(User, self).__init__(**kwargs)

    def get_name(self):
        if self.first_name is None or self.last_name is None:
            return self.user_name
        else:
            return f'{self.first_name} {self.last_name}'

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_username(self):
        return self.user_name

    def __validate_email(self, address):
        if not self.is_valid_email(address):
            raise InvalidEmailError(address)
        return address

    def get_email(self):
        if self.email is None or self.email == "":
            return None
        return self.email

    @staticmethod
    def is_valid_email(email):
        import re
        if len(email) > 7:
            return re.match('^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', email)
        else:
            return False

    def get_password(self):
        return self.password

    def get_group(self):
        return self.group_id

    def get_authenticator(self) -> str:
        return self.authenticator


class InvalidEmailError(CMDBError):
    def __init__(self, address):
        self.message = 'Invalid email address: {}'.format(address)
