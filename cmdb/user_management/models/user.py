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
from json import dumps
from datetime import datetime

from cmdb.data_storage.database_utils import default
from cmdb.framework import CmdbDAO
from cmdb.framework.utils import Collection, Model


class UserModel(CmdbDAO):
    COLLECTION: Collection = 'management.users'
    MODEL: Model = 'User'
    INDEX_KEYS = [
        {'keys': [('user_name', CmdbDAO.DAO_ASCENDING)], 'name': 'user_name', 'unique': True}
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
            'required': False
        },
        'first_name': {
            'type': 'string',
            'nullable': True,
            'required': False
        },
        'last_name': {
            'type': 'string',
            'nullable': True,
            'required': False
        },
        'email': {
            'type': 'string',
            'nullable': True,
            'required': False
        },
        'image': {
            'type': 'string',
            'nullable': True,
            'required': False
        }
    }

    __slots__ = 'public_id', 'user_name', 'active', 'group_id', 'registration_time', 'password', \
                'image', 'first_name', 'last_name', 'email', 'authenticator'

    def __init__(self, public_id: int, user_name: str, active: bool, group_id: int = None,
                 registration_time: datetime = None, password: str = None, image: str = None, first_name: str = None,
                 last_name: str = None, email: str = None, authenticator: str = None):

        self.user_name: str = user_name
        self.active: bool = active

        self.group_id: int = group_id or UserModel.DEFAULT_GROUP
        self.authenticator: str = authenticator or UserModel.DEFAULT_AUTHENTICATOR
        self.registration_time: datetime = registration_time or datetime.utcnow()

        self.email: str = email
        self.password: str = password
        self.image: str = image
        self.first_name: str = first_name or None
        self.last_name: str = last_name or None

        super(UserModel, self).__init__(public_id=public_id)

    def get_display_name(self) -> str:
        """
        Get the display name of the user.
        The display is first_name + last_name

        Returns:
            str: first_name + last_name or user_name if not first- and lastname is set
        """
        if self.first_name is None or self.last_name is None:
            return self.user_name
        else:
            return f'{self.first_name} {self.last_name}'

    @classmethod
    def from_data(cls, data: dict) -> "UserModel":
        return cls(
            public_id=data.get('public_id'),
            user_name=data.get('user_name'),
            active=data.get('active'),
            group_id=data.get('group_id', None),
            registration_time=data.get('registration_time', None),
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
            'email': instance.email,
            'password': instance.password,
            'image': instance.image,
            'first_name': instance.first_name,
            'last_name': instance.last_name
        }
