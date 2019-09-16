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

from datetime import datetime

from cmdb.user_management.user_base import UserManagementBase


class User(UserManagementBase):
    """
    User class
    """
    COLLECTION = 'management.users'
    REQUIRED_INIT_KEYS = ['user_name', 'registration_time', 'group_id']
    INDEX_KEYS = [
        {'keys': [('user_name', UserManagementBase.ASCENDING)], 'name': 'user_name', 'unique': True}
    ]

    def __init__(self, user_name, group_id, registration_time, active=True, password=None, last_login_time=None,
                 image=None, first_name=None, last_name=None, email=None, authenticator='LocalAuthenticationProvider',
                 **kwargs):
        """

        Args:
            user_name: display/login name of this user
            group_id: ID of the user group
            registration_time: time the user was inserted into database
            password: hmac hashed user password - if auth requires a password
            first_name: Display firstname
            last_name: Display lastname
            email: Email-address
            authenticator: String presentation of the selected Authenticator
            **kwargs: optional params
        """
        self.user_name = user_name
        self.password = password
        self.last_login_time = last_login_time or datetime.utcnow()
        self.image = image
        self.active = active
        self.group_id = group_id
        self.authenticator = authenticator
        self.email = email
        self.registration_time = registration_time
        self.first_name = first_name
        self.last_name = last_name
        super(User, self).__init__(**kwargs)

    def get_name(self) -> str:
        """
        Get the name of the user
        Display by first_name + last_name
        If not set the user_name will be returned
        Returns:
            str: display name
        """
        if self.first_name is None or self.last_name is None:
            return self.user_name
        else:
            return f'{self.first_name} {self.last_name}'

    def get_first_name(self) -> str:
        """
        Get firstname
        Returns:
            str: firstname
        """
        return self.first_name

    def get_last_name(self) -> str:
        """
        Get lastname
        Returns:
            str: lastname
        """
        return self.last_name

    def get_username(self) -> str:
        """
        Get username
        Returns:
            str: username/loginname
        """
        return self.user_name

    def get_email(self) -> (str, None):
        """
        Get email
        Returns:
            str: Returns none if string is empty
        """
        if self.email is None or self.email == "":
            return None
        return self.email

    def get_password(self) -> (str, bytes):
        """
        Get user password
        Returns:
            str: returns the hast
        """
        return self.password

    def get_group(self):
        """
        Get the public if of the user group
        Returns:
            int: group public id
        """
        return self.group_id

    def get_authenticator(self) -> str:
        """
        Get the Authenticator
        Returns:
            str: returns string representation of the authenticator class
        """
        return self.authenticator
