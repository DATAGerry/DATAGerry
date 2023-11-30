# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
from typing import Union, List

from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.user_management.models.user import UserModel
from ...framework.results import IterationResult
from ...framework.utils import PublicID
from ...manager import ManagerGetError, ManagerIterationError, ManagerDeleteError, ManagerUpdateError
from ...manager.managers import ManagerBase
from ...search import Query, Pipeline
# -------------------------------------------------------------------------------------------------------------------- #

class UserManager(ManagerBase):
    """TODO: document"""

    def __init__(self, database_manager: DatabaseManagerMongo):
        super().__init__(UserModel.COLLECTION, database_manager=database_manager)



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
        try:
            query: Pipeline = self.builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order)
            count_query: Pipeline = self.builder.count(filter=filter)
            aggregation_result = list(self._aggregate(self.collection, query))
            total_cursor = self._aggregate(self.collection, count_query)
            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']
        except ManagerGetError as err:
            raise ManagerIterationError(err) from err

        iteration_result: IterationResult[UserModel] = IterationResult(aggregation_result, total)
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
        result = self._get(self.collection, filter={'public_id': public_id}, limit=1)
        for resource_result in result.limit(-1):
            return UserModel.from_data(resource_result)
        raise ManagerGetError(f'User with ID: {public_id} not found!')



    def get_by(self, query: Query) -> UserModel:
        """
        Get a single user by a query.

        Args:
            query (Query): Query filter of user parameters.

        Returns:
            UserModel: Instance of UserModel with matching data.
        """
        result = self._get(self.collection, filter=query, limit=1)
        for resource_result in result.limit(-1):
            return UserModel.from_data(resource_result)
        raise ManagerGetError(f'User with the query: {query} not found!')



    def get_many(self, query: Query = None) -> List[UserModel]:
        """
        Get a collection of users by a query. Passing no query means all users.

        Args:
            query (Query): A database query for filtering.

        Returns:
            List[UserModel]: A list of all users which matches the query.
        """
        query = query or {}
        results = self._get(self.collection, filter=query)
        return [UserModel.from_data(user) for user in results]



    def insert(self, user: Union[UserModel, dict]) -> PublicID:
        """
        Insert a single user into the system.

        Args:
            user (dict): Raw data of the user.

        Notes:
            If no public id was given, the database manager will auto insert the next available ID.

        Returns:
            int: The Public ID of the new inserted user
        """
        if isinstance(user, UserModel):
            user = UserModel.to_data(user)
        return self._insert(self.collection, resource=user)



    def update(self, public_id: Union[PublicID, int], user: Union[UserModel, dict]):
        """
        Update a existing user in the system.

        Args:
            public_id (int): PublicID of the user in the system.
            user(UserModel): Instance or dict of UserModel

        Notes:
            If a UserModel instance was passed as user argument, \
            it will be auto converted via the model `to_dict` method.
        """
        if isinstance(user, UserModel):
            user = UserModel.to_dict(user)
        update_result = self._update(collection=self.collection, filter={'public_id': public_id}, resource=user)

        if update_result.matched_count != 1:
            raise ManagerUpdateError('Something happened during the update!')
        return update_result



    def delete(self, public_id: Union[PublicID, int]) -> UserModel:
        """
        Delete a existing user by its PublicID.

        Args:
            public_id (int): PublicID of the user in the system.

        Raises:
            ManagerDeleteError: If you try to delete the admin \
                                or something happened during the database operation.

        Returns:
            UserModel: The deleted user as its model.
        """
        if public_id in [1]:
            raise ManagerDeleteError('You cant delete the admin user')
        user: UserModel = self.get(public_id=public_id)
        delete_result = self._delete(self.collection, filter={'public_id': public_id})

        if delete_result.deleted_count == 0:
            raise ManagerDeleteError(err='No user matched this public id')
        return user
