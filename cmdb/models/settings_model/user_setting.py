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
from json import dumps
from pymongo import IndexModel

from cmdb.database.utils import default

from cmdb.models.settings_model.user_setting_type_enum import UserSettingType
from cmdb.models.settings_model.user_setting_payload import UserSettingPayload
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               UserSettingModel - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class UserSettingModel:
    """
    User settings model. Holds all stored user-settings for a specific user.
    Every user has exact one model document in the database collection.
    """

    COLLECTION = 'management.users.settings'
    MODEL = 'UserSetting'
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

    def __init__(self, resource: str, user_id: int, payloads: list[UserSettingPayload], setting_type: UserSettingType):
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
        self.payloads: list[UserSettingPayload] = payloads
        self.setting_type: UserSettingType = setting_type

    @classmethod
    def get_index_keys(cls):
        """TODO: document"""
        return [IndexModel(**index) for index in cls.INDEX_KEYS]


    @classmethod
    def from_data(cls, data: dict) -> "UserSettingModel":
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
