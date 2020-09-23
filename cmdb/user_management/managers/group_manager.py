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

from .account_manager import AccountManager
from .right_manager import RightManager
from .. import UserGroupModel
from ..models.right import BaseRight
from ...data_storage.database_manager import DatabaseManagerMongo
from ...framework.managers import ManagerDeleteError
from ...framework.results import IterationResult
from ...framework.utils import PublicID


class GroupManager(AccountManager):

    def __init__(self, database_manager: DatabaseManagerMongo, right_manager: RightManager = None):
        self.right_manager: RightManager = right_manager
        super(GroupManager, self).__init__(UserGroupModel.COLLECTION, database_manager=database_manager)

    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) \
            -> IterationResult[UserGroupModel]:
        """
        Iterate over a collection of group resources.

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
        iteration_result: IterationResult[UserGroupModel] = super(GroupManager, self).iterate(
            filter=filter, limit=limit, skip=skip, sort=sort, order=order)
        iteration_result.results = [UserGroupModel.from_data(result, self.right_manager.rights) for result in
                                    iteration_result.results]
        return iteration_result

    def get(self, public_id: Union[PublicID, int]) -> UserGroupModel:
        """
        Get a single group by its id.

        Args:
            public_id (int): ID of the group.

        Returns:
            UserModel: Instance of UserGroupModel with data.
        """
        result = super(GroupManager, self).get(public_id=public_id)
        return UserGroupModel.from_data(result, self.right_manager.rights)

    def insert(self, group: dict) -> PublicID:
        """
        Insert a single group into the system.

        Args:
            group (dict): Raw data of the group.

        Notes:
            If no public id was given, the database manager will auto insert the next available ID.

        Returns:
            int: The Public ID of the new inserted group
        """
        return super(GroupManager, self).insert(resource=group)

    def update(self, public_id: Union[PublicID, int], group: UserGroupModel):
        """
        Update a existing group in the system.

        Args:
            public_id (int): PublicID of the user in the system.
            group (UserGroupModel): Instance of UserGroupModel

        """
        return super(GroupManager, self).update(public_id=public_id, resource=UserGroupModel.to_data(group))

    def delete(self, public_id: Union[PublicID, int]) -> UserGroupModel:
        """
        Delete a existing group by its PublicID.

        Args:
            public_id (int): PublicID of the group in the system.

        Raises:
            ManagerDeleteError: If you try to delete the admin or user group

        Returns:
            UserGroupModel: The deleted group as its model.
        """
        if public_id in [1, 2]:
            raise ManagerDeleteError(f'Group with ID: {public_id} can not be deleted!')
        group: UserGroupModel = self.get(public_id=public_id)
        super(GroupManager, self).delete(public_id=public_id)
        return group
