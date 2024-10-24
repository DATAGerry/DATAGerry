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

from cmdb.user_management.rights import flat_rights_tree, __all__ as rights
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.user_management.models.group import UserGroupModel
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import ManagerUpdateError, ManagerDeleteError, ManagerGetError, ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GroupsManager - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class GroupsManager(BaseManager):
    """TODO: document"""
    def __init__(self, dbm: MongoDatabaseManager = None, database :str = None):
        self.rights = flat_rights_tree(rights)

        if database:
            dbm.connector.set_database(database)

        super().__init__(UserGroupModel.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_group(self, group: Union[UserGroupModel, dict]) -> int:
        """
        Insert a single group into the system.

        Args:
            group (dict): Raw data of the group.

        Notes:
            If no public id was given, the database manager will auto insert the next available ID.

        Returns:
            int: The Public ID of the new inserted UserGroupModel
        """
        if isinstance(group, UserGroupModel):
            group = UserGroupModel.to_data(group)

        return self.insert(group)

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_group(self, public_id: int) -> UserGroupModel:
        """
        Get a single group by its id.

        Args:
            public_id (int): ID of the group.

        Returns:
            UserGroupModel: Instance of UserGroupModel with data.
        """
        requested_group = self.get_one(public_id)

        try:
            return UserGroupModel.from_data(requested_group, self.rights)
        except Exception as err:
            #ERROR-FIX
            raise ManagerGetError(str(err)) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[UserGroupModel]:
        """
        TODO: document
        """
        aggregation_result, total = self.iterate_query(builder_params)

        iteration_result: IterationResult[UserGroupModel] = IterationResult(aggregation_result, total)
        iteration_result.convert_to(UserGroupModel)

        return iteration_result

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_group(self, public_id: int, group: Union[UserGroupModel, dict]):
        """
        Update a existing group in the system.

        Args:
            public_id (int): PublicID of the user in the system.
            group (UserGroupModel): Instance of UserGroupModel
        """

        update_result = self.update(criteria={'public_id': public_id}, data=group)

        if update_result.matched_count != 1:
            raise ManagerUpdateError('Something happened during the update!')

        return update_result

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_group(self, public_id: int) -> UserGroupModel:
        """
        Delete a existing group by its PublicID.

        Args:
            public_id (int): PublicID of the group in the system.

        Raises:
            ManagerDeleteError: If you try to delete the admin or user group \
                                or something happened during the database operation.

        Returns:
            UserGroupModel: The deleted group as its model.
        """
        if public_id in [1, 2]:
            raise ManagerDeleteError(f'Group with ID: {public_id} can not be deleted!')
        group: UserGroupModel = self.get_group(public_id)

        try:
            self.delete({'public_id': public_id})
        except Exception as err:
            raise ManagerDeleteError('No group matched this public id') from err

        return group
