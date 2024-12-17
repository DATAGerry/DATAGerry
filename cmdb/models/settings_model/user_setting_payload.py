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
from typing import Any

from cmdb.database.utils import default
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              UserSettingPayload - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
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