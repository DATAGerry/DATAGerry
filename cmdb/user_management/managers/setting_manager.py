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
from typing import Union, List

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.framework.results import IterationResult
from cmdb.framework.utils import PublicID
from cmdb.manager import ManagerGetError, ManagerIterationError
from cmdb.search import Query
from cmdb.user_management.models.settings import UserSettingModel, UserSettingType
from cmdb.user_management.managers.account_manager import AccountManager


class UserSettingsManager(AccountManager):
    """
    Manager for user settings CRUD functions.
    """

    def __init__(self, database_manager: DatabaseManagerMongo = None):
        """
        Constructor of `UserSettingsManager`
        Args:
            database_manager: Active database connection manager
        """
        super(UserSettingsManager, self).__init__(collection=UserSettingModel.COLLECTION,
                                                  database_manager=database_manager)

    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) \
            -> IterationResult[UserSettingModel]:
        """
        Iterate over a collection of settings resources.

        Args:
            filter: match requirements of field values
            limit: max number of elements to return
            skip: number of elements to skip first
            sort: sort field
            order: sort order

        Returns:
            IterationResult: Instance of IterationResult with generic UserSettingModel.
        """

        try:
            query: Query = self.builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order)
            aggregation_result = next(self._aggregate(self.collection, query))
        except ManagerGetError as err:
            raise ManagerIterationError(err=err)
        iteration_result: IterationResult[UserSettingModel] = IterationResult.from_aggregation(aggregation_result)
        iteration_result.convert_to(UserSettingModel)
        return iteration_result

    def get(self, public_id: PublicID) -> UserSettingModel:
        """
        Get a single setting by its id.

        Args:
            public_id (int): ID of the setting.

        Returns:
            UserSettingModel: Instance of UserSettingModel with data.
        """

        result = self._get(self.collection, filter={'public_id': public_id}, limit=1)
        for resource_result in result.limit(-1):
            return UserSettingModel.from_data(resource_result)
        raise ManagerGetError(f'No setting with the id: {public_id} was found!')

    def get_user_settings(self, user_id: PublicID, setting_type: UserSettingType = None) -> List[UserSettingModel]:
        """
        Get all settings from a user by the user_id.
        Args:
            user_id (int): PublicID of the user.
            setting_type(UserSettingType): Optional the type of user settings for filtering.

        Returns:
            - List of UserSettingModel.
        """
        query = {'user_id': user_id}
        if setting_type:
            query.update({'setting_type': setting_type.value})

        user_settings = self._get(self.collection, filter=query)
        return [UserSettingModel.from_data(setting) for setting in user_settings]

    def insert(self, setting: Union[dict, UserSettingModel]):
        """
        Insert a single setting into the database.

        Args:
            setting (Union[dict, UserSettingModel]): Raw data of the setting.

        Notes:
            - If no public id was given, the database manager will auto insert the next available ID.
            - If a UserSettingModel instance was passed as type argument, \
              it will be auto converted via the model `to_data` method.

        Returns:
            int: The Public ID of the new inserted UserSettingModel
        """

        if isinstance(setting, UserSettingModel):
            setting = UserSettingModel.to_data(setting)
        return self._insert(self.collection, resource=setting)

    def update(self, public_id: PublicID, setting: Union[dict, UserSettingModel]):
        """
        Update a existing setting in the database.

        Args:
            public_id (int): PublicID of the setting in the database.
            setting (Union[dict, UserSettingModel]): Instance of UserSettingModel or dict

        Notes:
            If a UserSettingModel instance was passed as type argument, \
            it will be auto converted via the model `to_data` method.
        """

        if isinstance(setting, UserSettingModel):
            setting = UserSettingModel.to_data(setting)
        return self._update(collection=self.collection, filter={'public_id': public_id}, resource=setting)

    def delete(self, public_id: PublicID):
        """
        Delete a existing setting by its PublicID.

        Args:
            public_id (int): PublicID of the setting.

        Returns:
            UserSettingModel: The deleted setting as its model.
        """
        setting: UserSettingModel = self.get(public_id=public_id)
        self._delete(self.collection, public_id=public_id)
        return setting
