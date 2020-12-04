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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime
from enum import Enum
from json import dumps
from typing import Any, List
from pymongo import IndexModel

from cmdb.database.utils import default
from cmdb.framework.utils import Collection, Model


class UserSettingType(Enum):
    """
    Type of user settings. Applied only on user application level.
    SERVER means only backend settings. APPLICATION only the frontend.
    Global means both.
    """
    GLOBAL = 'GLOBAL'
    APPLICATION = 'APPLICATION'
    SERVER = 'SERVER'


class UserSettingPayload:
    """
    Payload wrapper user settings.
    """
    __slots__ = 'name', 'payload'

    def __init__(self, payload: Any):
        """
        Constructor of `UserSettingPayload`.

        Args:
            payload (Any): Settings option/body/payload.
        """
        self.payload: Any = payload

    @classmethod
    def from_data(cls, data: dict) -> "UserSettingPayload":
        """
        Create a `UserSettingEntry` instance from database.

        Args:
            data (dict): Database user settings values.

        Returns:
            UserSettingPayload: Instance of `UserSettingEntry`.
        """
        return cls(
            payload=data
        )

    @classmethod
    def to_data(cls, instance: "UserSettingPayload") -> str:
        """
        Get the setting to database format.

        Args:
            instance (UserSettingPayload): Instance of `UserSettingPayload`.

        Returns:
            str: JSON dump data of `UserSettingPayload`.
        """
        return dumps(UserSettingPayload.to_dict(instance), default=default)

    @classmethod
    def to_dict(cls, instance: "UserSettingPayload") -> dict:
        """
        Get the dictionary values of `UserSettingEntry`

        Args:
            instance (UserSettingPayload): Instance of `UserSettingEntry`.

        Returns:
            dict: Return the `UserSettingEntry` as dict.
        """
        return instance.payload


class UserSettingModel:
    """
    User settings model. Holds all stored user-settings for a specific user.
    Every user has exact one model document in the database collection.
    """

    COLLECTION: Collection = 'management.users.settings'
    MODEL: Model = 'UserSetting'
    INDEX_KEYS = [
        {'keys': [('resource', 1), ('user_id', 1)],
         'name': 'resource-user',
         'unique': True}
    ]

    SCHEMA: dict = {
        'resource': {
            'type': 'string',
            'required': True
        },
        'user_id': {
            'type': 'integer',
            'required': True
        },
        'payloads': {
            'type': 'list',
            'required': False
        },
        'setting_type': {
            'type': 'string',
            'required': True
        }
    }

    __slots__ = 'resource', 'user_id', 'payloads', 'setting_type'

    def __init__(self, resource: str, user_id: int, payloads: List[UserSettingPayload], setting_type: UserSettingType):
        """
        Constructor of `UserSettingModel`.

        Args:
            resource: (str): Identifier or Name of the setting
            user_id (int): PublicID of the user
            payloads (list): Setting payloads
            setting_type (UserSettingType): Type of the setting scope.
        """
        self.resource: str = resource
        self.user_id: int = user_id
        self.payloads: List[UserSettingPayload] = payloads
        self.setting_type: UserSettingType = setting_type

    @classmethod
    def get_index_keys(cls):
        return [IndexModel(**index) for index in cls.INDEX_KEYS]

    @classmethod
    def from_data(cls, data: dict, *args, **kwargs) -> "UserSettingModel":
        """
        Create a `UserSettingsModel` instance from database.

        Args:
            data (dict): Database user settings.

        Returns:
            UserSettingModel: Instance of `UserSettingsModel`.
        """
        payloads = [UserSettingPayload.from_data(payload) for payload in data.get('payloads', [])]
        return cls(
            resource=data.get('resource'),
            user_id=int(data.get('user_id')),
            payloads=payloads,
            setting_type=UserSettingType(data.get('setting_type'))
        )

    @classmethod
    def to_data(cls, instance: "UserSettingModel") -> str:
        """
        Get the user settings to database format.

        Args:
            instance (UserSettingModel): Instance of `UserSettingsModel`.

        Returns:
            str: JSON dump data of `UserSettingsModel`.
        """

        return dumps(UserSettingModel.to_dict(instance), default=default)

    @classmethod
    def to_dict(cls, instance: "UserSettingModel") -> dict:
        """
        Get the dictionary values of `UserSettingsModel`

        Args:
            instance (UserSettingModel): Instance of `UserSettingsModel`.

        Returns:
            dict: Return the `UserSettingsModel` as dict.
        """
        return {
            'resource': instance.resource,
            'user_id': instance.user_id,
            'payloads': [UserSettingPayload.to_dict(payload) for payload in instance.payloads],
            'setting_type': instance.setting_type.value
        }
