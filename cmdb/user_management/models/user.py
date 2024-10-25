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
from datetime import datetime, timezone
from dateutil import parser

from cmdb.cmdb_objects.cmdb_dao import CmdbDAO
# -------------------------------------------------------------------------------------------------------------------- #

class UserModel(CmdbDAO):
    """TODO: document"""
    COLLECTION = 'management.users'
    MODEL = 'User'
    INDEX_KEYS = [
        {
            'keys': [('user_name', CmdbDAO.DAO_ASCENDING)],
            'name': 'user_name',
            'unique': True
        }
    ]

    DEFAULT_AUTHENTICATOR: str = 'LocalAuthenticationProvider'
    DEFAULT_GROUP: int = 2

    SCHEMA: dict = {
        'public_id': {
            'type': 'integer'
        },
        'user_name': {
            'type': 'string',
            'required': True,
        },
        'active': {
            'type': 'boolean',
            'default': True,
            'required': False
        },
        'group_id': {
            'type': 'integer',
            'default': DEFAULT_GROUP,
            'required': True
        },
        'registration_time': {
            'type': 'string',
            'nullable': True,
            'empty': True,
            'required': False
        },
        'authenticator': {
            'type': 'string',
            'nullable': True,
            'default': DEFAULT_AUTHENTICATOR,
            'required': False
        },
        'password': {
            'type': 'string',
            'nullable': True,
            'empty': True,
            'required': False
        },
        'first_name': {
            'type': 'string',
            'nullable': True,
            'empty': True,
            'required': False
        },
        'last_name': {
            'type': 'string',
            'nullable': True,
            'empty': True,
            'required': False
        },
        'email': {
            'type': 'string',
            'nullable': True,
            'empty': True,
            'required': False
        },
        'image': {
            'type': 'string',
            'nullable': True,
            'empty': True,
            'required': False
        },
        'database': {
            'type': 'string',
            'nullable': True,
            'empty': True,
            'required': False
        }
    }

    __slots__ = 'public_id', 'user_name', 'active', 'group_id', 'registration_time', 'password', \
                'image', 'first_name', 'last_name', 'database', 'email', 'authenticator'

    def __init__(self,
                 public_id: int,
                 user_name: str,
                 active: bool,
                 group_id: int = None,
                 registration_time: datetime = None,
                 password: str = None,
                 database: str = 'test',
                 image: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 email: str = None,
                 authenticator: str = None):

        self.user_name: str = user_name
        self.active: bool = active

        self.group_id: int = group_id or UserModel.DEFAULT_GROUP
        self.authenticator: str = authenticator or UserModel.DEFAULT_AUTHENTICATOR
        self.registration_time: datetime = registration_time or datetime.now(timezone.utc)

        self.database = database
        self.email: str = email
        self.password: str = password
        self.image: str = image
        self.first_name: str = first_name or None
        self.last_name: str = last_name or None

        super().__init__(public_id=public_id)


    def get_database(self) -> str:
        """Retrives the database name of the user

        Returns:
            str: Name of the database
        """
        return self.database

    def get_display_name(self) -> str:
        """
        Get the display name of the user.
        The display is first_name + last_name

        Returns:
            str: first_name + last_name or user_name if not first- and lastname is set
        """
        if self.first_name is None or self.last_name is None:
            return self.user_name

        return f'{self.first_name} {self.last_name}'


    @classmethod
    def from_data(cls, data: dict) -> "UserModel":
        """TODO: document"""
        reg_date = data.get('registration_time', None)

        if reg_date and isinstance(reg_date, str):
            reg_date = parser.parse(reg_date)

        return cls(
            public_id=data.get('public_id'),
            user_name=data.get('user_name'),
            active=data.get('active'),
            database=data.get('database'),
            group_id=data.get('group_id', None),
            registration_time=reg_date,
            authenticator=data.get('authenticator', None),
            email=data.get('email', None),
            password=data.get('password', None),
            image=data.get('image', None),
            first_name=data.get('first_name', None),
            last_name=data.get('last_name', None)
        )


    @classmethod
    def to_data(cls, instance: "UserModel") -> dict:
        return cls.to_dict(instance)


    @classmethod
    def to_dict(cls, instance: "UserModel") -> dict:
        return {
            'public_id': instance.public_id,
            'user_name': instance.user_name,
            'active': instance.active,
            'group_id': instance.group_id,
            'registration_time': instance.registration_time,
            'authenticator': instance.authenticator,
            'database': instance.database,
            'email': instance.email,
            'password': instance.password,
            'image': instance.image,
            'first_name': instance.first_name,
            'last_name': instance.last_name
        }


    def __str__(self) -> str:
        return (
            f"User(\n"
            f"public_id: {self.public_id},\n"
            f"email: {self.email},\n"
            f"user_name: {self.user_name},\n"
            f"group_id: {self.group_id},\n"
            f"authenticator: {self.authenticator},\n"
            f"database: {self.database}\n"
            f")"
        )
