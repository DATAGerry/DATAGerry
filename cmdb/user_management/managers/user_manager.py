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
from typing import Union

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.user_management.models.user import UserModel
from .account_manager import AccountManager
from ...framework.results import IterationResult
from ...framework.utils import PublicID


class UserManager(AccountManager):

    def __init__(self, database_manager: DatabaseManagerMongo):
        super(UserManager, self).__init__(UserModel.COLLECTION, database_manager=database_manager)

    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) \
            -> IterationResult[UserModel]:
        """
        Iterate over a collection of user resources.

        Args:
            filter: match requirements of field values
            limit: max number of elements to return
            skip: number of elements to skip first
            sort: sort field
            order: sort order
            *args:
            **kwargs:

        Returns:
            IterationResult: Instance of IterationResult with generic UserModel.
        """
        iteration_result: IterationResult[UserModel] = super(UserManager, self).iterate(
            filter=filter, limit=limit, skip=skip, sort=sort, order=order)
        iteration_result.convert_to(UserModel)
        return iteration_result

    def get(self, public_id: Union[PublicID, int]) -> UserModel:
        """
        Get a single user by its id.

        Args:
            public_id (int): ID of the user.

        Returns:
            UserModel: Instance of UserModel with data.
        """
        result = super(UserManager, self).get(public_id=public_id)
        return UserModel.from_data(result)

    def insert(self, user: dict) -> PublicID:
        """
        Insert a single user into the system.

        Args:
            user (dict): Raw data of the user.

        Notes:
            If no public id was given, the database manager will auto insert the next available ID.

        Returns:
            int: The Public ID of the new inserted user
        """
        return super(UserManager, self).insert(resource=user)

    def update(self, public_id: Union[PublicID, int], user: Union[UserModel, dict]):
        """
        Update a existing user in the system.

        Args:
            public_id (int): PublicID of the user in the system.
            user(UserModel): Instance or dict of UserModel

        Notes:
            If a UserModel instance was passed as user argument, \
            it will be auto converted via the model `to_json` method.
        """
        if isinstance(user, UserModel):
            user = UserModel.to_dict(user)
        return super(UserManager, self).update(public_id=public_id, resource=user)

    def delete(self, public_id: Union[PublicID, int]) -> UserModel:
        """
        Delete a existing user by its PublicID.

        Args:
            public_id (int): PublicID of the user in the system.

        Returns:
            UserModel: The deleted user as its model.
        """
        user: UserModel = self.get(public_id=public_id)
        super(UserManager, self).delete(public_id=public_id)
        return user
