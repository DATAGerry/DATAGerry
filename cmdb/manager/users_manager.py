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

from cmdb.user_management.models.user import UserModel
from cmdb.framework.results import IterationResult
from cmdb.manager.query_builder.builder_parameters import BuilderParameters

from cmdb.errors.manager import ManagerUpdateError,\
                                ManagerDeleteError,\
                                ManagerGetError,\
                                ManagerIterationError,\
                                ManagerInsertError
from cmdb.errors.manager.user_manager import UserManagerGetError,\
                                             UserManagerInsertError,\
                                             UserManagerDeleteError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 UsersManager - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class UsersManager(BaseManager):
    """
    TODO: document
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        if database:
            dbm.connector.set_database(database)

        super().__init__(UserModel.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_user(self, user: Union[UserModel, dict]) -> int:
        """
        Insert a single user into the system

        Args:
            user (dict): Raw data of the user
        Notes:
            If no public id was given, the database manager will auto insert the next available ID
        Returns:
            int: The Public ID of the new inserted user
        """
        if isinstance(user, UserModel):
            user = UserModel.to_data(user)

        try:
            return self.insert(user)
        except ManagerInsertError as err:
            raise UserManagerInsertError(err) from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_user(self, public_id: int) -> UserModel:
        """
        Get a single user by its id.

        Args:
            public_id (int): ID of the user.

        Returns:
            UserModel: Instance of UserModel with data.
        """
        try:
            requested_user = self.get_one(public_id)
        except ManagerGetError as err:
            raise UserManagerGetError(err) from err

        if requested_user:
            return UserModel.from_data(requested_user)

        raise UserManagerGetError("User not found!")


    def get_user_by(self, query: dict) -> UserModel:
        """
        Get a single user by a query.

        Args:
            query (dict): Query filter of user parameters.

        Returns:
            UserModel: Instance of UserModel with matching data.
        """
        try:
            result = self.get(filter=query, limit=1)

            for resource_result in result.limit(-1):
                return UserModel.from_data(resource_result)
        except Exception as err:
            raise UserManagerGetError(err) from err


    def get_many_users(self, query: list = None) -> list[UserModel]:
        """
        Get a collection of users by a query. Passing no query means all users

        Args:
            query (dict): A database query for filtering
        Raises:
            UserManagerGetError: Raised when users cant be retrieved or not transformed into UserModel
        Returns:
            list[UserModel]: A list of all users which matches the query
        """
        query = query or {}

        try:
            results = self.get(filter=query)

            return [UserModel.from_data(user) for user in results]
        except Exception as err:
            LOGGER.debug("[get_many_users] Error: %s, Type: %s", err, type(err))
            raise UserManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[UserModel]:
        """
        Iterate over a collection of user resources

        Args:
            TODO: document

        Returns:
            IterationResult: Instance of IterationResult with generic UserModel.
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)
        except ManagerGetError as err:
            raise ManagerIterationError(err) from err

        iteration_result: IterationResult[UserModel] = IterationResult(aggregation_result, total)
        iteration_result.convert_to(UserModel)

        return iteration_result

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_user(self, public_id: int, user: Union[UserModel, dict]):
        """
        Update a existing user in the system

        Args:
            public_id (int): PublicID of the user in the system
            user(UserModel): Instance or dict of UserModel

        Notes:
            If a UserModel instance was passed as user argument,
            it will be auto converted via the model `to_dict` method
        """
        if isinstance(user, UserModel):
            user = UserModel.to_dict(user)

        update_result = self.update(criteria={'public_id': public_id}, data=user)

        if update_result.matched_count != 1:
            raise ManagerUpdateError('Something happened during the update!')

        return update_result

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_user(self, public_id: int) -> UserModel:
        """
        Delete an existing user by its PublicID

        Args:
            public_id (int): PublicID of the user

        Raises:
            UserManagerDeleteError:
                - If you try to delete the admin
                - If user which should be deleted could not be retrieved
                - No user matches the public_id
                - User could not be deleted

        Returns:
            UserModel: Model of the deleted user
        """
        if public_id == 1:
            raise UserManagerDeleteError("You can't delete the admin user")

        try:
            user: UserModel = self.get_user(public_id)
        except UserManagerGetError as err:
            raise UserManagerDeleteError(f"Could not retrieve user with ID: {public_id}") from err

        try:
            delete_result = self.delete({'public_id': public_id})

            if not delete_result:
                raise UserManagerDeleteError('No user matched this public_id')
        except ManagerDeleteError as err:
            raise UserManagerDeleteError(f"Could not delete user with ID: {public_id}") from err

        return user
