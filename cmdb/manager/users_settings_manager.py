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
from typing import Union

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.base_manager import BaseManager

from cmdb.models.settings_model.user_setting import UserSettingModel
from cmdb.models.settings_model.user_setting_type_enum import UserSettingType

from cmdb.errors.manager import ManagerDeleteError, ManagerGetError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                             UsersSettingsManager - CLASS                                             #
# -------------------------------------------------------------------------------------------------------------------- #
class UsersSettingsManager(BaseManager):
    """
    Manager for user settings CRUD functions
    """
    def __init__(self, dbm: MongoDatabaseManager = None, database: str = None):
        """
        Constructor of `UsersSettingsManager`
        Args:
            database_manager: Active database connection manager
        """
        if database:
            dbm.connector.set_database(database)

        super().__init__(UserSettingModel.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_setting(self, setting: Union[dict, UserSettingModel]):
        """
        Insert a single setting into the database

        Args:
            setting (Union[dict, UserSettingModel]): Raw data of the setting
        """
        if isinstance(setting, UserSettingModel):
            setting = UserSettingModel.to_data(setting)

        return self.insert(setting, True)

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_user_setting(self, user_id: int, resource: str) -> UserSettingModel:
        """
        Get a single setting from a user by the identifier

        Args:
            user_id (int): PublicID of the user.
            resource (str): Name of the setting.

        Returns:
            UserSettingModel: Instance of UserSettingModel with data.
        """
        result = self.find(criteria={'user_id': user_id, 'resource': resource}, limit=1)

        for resource_result in result.limit(-1):
            return UserSettingModel.from_data(resource_result)

        raise ManagerGetError(f'No setting with the name: {resource} was found!')



    def get_user_settings(self, user_id: int, setting_type: UserSettingType = None) -> list[UserSettingModel]:
        """
        Get all settings from a user by the user_id.
        Args:
            user_id (int): public_id of the user
            setting_type(UserSettingType): Optional the type of user settings for filtering.

        Returns:
            (list[UserSettingModel]): List of UserSettingModel
        """
        query = {'user_id': user_id}

        if setting_type:
            query.update({'setting_type': setting_type.value})

        user_settings = self.find(criteria=query)

        return [UserSettingModel.from_data(setting) for setting in user_settings]

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_setting(self, user_id: int, resource: str, setting: Union[dict, UserSettingModel]):
        """
        Update a existing setting in the database.

        Args:
            setting (Union[dict, UserSettingModel]): Settings data.
            user_id (int): User of this setting.
            resource (str): Identifier of the setting.

        Notes:
            If a `UserSettingModel` was passed as type argument, \
            it will be auto converted via the model `to_data` method.
        """
        if isinstance(setting, UserSettingModel):
            setting = UserSettingModel.to_dict(setting)

        return self.update(criteria={'resource': resource, 'user_id': user_id}, data=setting)

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_setting(self, user_id: int, resource: str):
        """
        Delete a existing setting by the tuple of user_id and identifier.

        Args:
            user_id (int): PublicID of the user in the database.
            resource (str): Name/Identifier of the setting.

        Returns:
            UserSettingModel: The deleted setting as its model.
        """
        setting: UserSettingModel = self.get_user_setting(user_id=user_id, resource=resource)

        delete_result = self.delete(criteria={'user_id': user_id, 'resource': resource})

        if not delete_result:
            raise ManagerDeleteError('No user matched this public id')

        return setting
