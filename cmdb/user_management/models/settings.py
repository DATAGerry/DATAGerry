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
from typing import Any

from cmdb.data_storage.database_utils import default
from cmdb.framework import CmdbDAO
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


class UserSettingEntry:
    """
    Represents a single entry in the user settings.
    """
    __slots__ = 'name', 'setting'

    def __init__(self, name: str, setting: Any):
        """
        Constructor of `UserSettingEntry`.

        Args:
            name (str): Name/Identifier of the setting.
            setting (Any): Settings option/body/payload.
        """
        self.name: str = name
        self.setting: Any = setting

    @classmethod
    def from_data(cls, data: dict) -> "UserSettingEntry":
        """
        Create a `UserSettingEntry` instance from database.

        Args:
            data (dict): Database user settings entry values.

        Returns:
            UserSettingEntry: Instance of `UserSettingEntry`.
        """
        return cls(
            name=data.get('name'),
            setting=data.get('setting', None)
        )

    @classmethod
    def to_data(cls, instance: "UserSettingEntry") -> str:
        """
        Get the setting to database format.

        Args:
            instance (UserSettingEntry): Instance of `UserSettingEntry`.

        Returns:
            str: JSON dump data of `UserSettingEntry`.
        """
        return dumps(UserSettingEntry.to_dict(instance), default=default)

    @classmethod
    def to_dict(cls, instance: "UserSettingEntry") -> dict:
        """
        Get the dictionary values of `UserSettingEntry`

        Args:
            instance (UserSettingEntry): Instance of `UserSettingEntry`.

        Returns:
            dict: Return the `UserSettingEntry` as dict.
        """
        return {
            'name': instance.name,
            'setting': instance.setting
        }


class UserSettingModel(CmdbDAO):
    """
    User settings model. Holds all stored user-settings for a specific user.
    Every user has exact one model document in the database collection.
    """

    COLLECTION: Collection = 'management.users.settings'
    MODEL: Model = 'UserSetting'

    SCHEMA: dict = {
        'public_id': {
            'type': 'integer',
            'required': False
        },
        'user_id': {
            'type': 'integer',
            'required': True
        },
        'setting': {
            'type': 'dict',
            'required': False
        },
        'active': {
            'type': 'boolean',
            'required': True
        },
        'setting_type': {
            'type': 'datetime',
            'required': True
        }
    }

    __slots__ = 'public_id', 'user_id', 'setting', 'active', 'setting_type', 'setting_time'

    def __init__(self, public_id: int, user_id: int, setting: UserSettingEntry, active: bool,
                 setting_type: UserSettingType, setting_time: datetime):
        """
        Constructor of `UserSettingModel`.

        Args:
            public_id: (int): PublicID of the setting
            user_id (int): PublicID of the user
            setting (UserSettingEntry): User setting
            active (bool): Activate/Deactivate flag.
            setting_type (UserSettingType): Type of the setting scope.
            setting_time: Datetime of the setting creation.
        """
        self.user_id: int = user_id
        self.setting: UserSettingEntry = setting
        self.active: bool = active
        self.setting_type: UserSettingType = setting_type
        self.setting_time: datetime = setting_time
        super().__init__(public_id=public_id)

    @classmethod
    def from_data(cls, data: dict, *args, **kwargs) -> "UserSettingModel":
        """
        Create a `UserSettingsModel` instance from database.

        Args:
            data (dict): Database user settings.

        Returns:
            UserSettingModel: Instance of `UserSettingsModel`.
        """
        return cls(
            public_id=int(data.get('public_id')),
            user_id=int(data.get('user_id')),
            setting=UserSettingEntry.from_data(data=data.get('settings', None)),
            active=data.get('active'),
            setting_type=UserSettingType(data.get('setting_type')),
            setting_time=data.get('setting_time')
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
            'public_id': instance.public_id,
            'user_id': instance.user_id,
            'settings': UserSettingEntry.to_data(instance.setting),
            'active': instance.active,
            'setting_type': instance.setting_type,
            'setting_time': instance.setting_time
        }
