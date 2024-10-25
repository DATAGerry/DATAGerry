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
from multiprocessing.managers import BaseManager

from cmdb.user_management.models.right import BaseRight
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import ManagerGetError, ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 RightsManager - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class RightsManager(BaseManager):
    """TODO: document"""
    def __init__(self, right_tree):
        self.rights = RightsManager.flat_tree(right_tree)

        super().__init__()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def iterate_rights(self, limit: int, skip: int, sort: str, order: int) -> IterationResult[BaseRight]:
        """TODO: document"""
        try:
            sorted_rights = sorted(self.rights, key=lambda right: right[sort], reverse=order == -1)

            if limit > 0:
                spliced_rights = [sorted_rights[i:i + limit] for i in range(0, len(sorted_rights),
                                  limit)][int(skip / limit)]
            else:
                spliced_rights = sorted_rights
        except (AttributeError, ValueError, IndexError) as err:
            raise ManagerIterationError(err) from err

        result: IterationResult[BaseRight] = IterationResult(spliced_rights, len(self.rights))

        return result


    def get_right(self, name: str) -> BaseRight:
        """
        Get a right by its name

        Args:
            name: Name of the right

        Returns:
            BaseRight: Right instance
        """
        try:
            return next(right for right in self.rights if right.name == name)
        except Exception as err:
            raise ManagerGetError(err) from err

# -------------------------------------------------- HELPER METHODS -------------------------------------------------- #

    @staticmethod
    def flat_tree(right_tree) -> list[BaseRight]:
        """
        Flat the right tree to list

        Args:
            right_tree: Tuple tree of rights

        Returns:
            list[BaseRight]: Flatted right tree
        """
        rights: list[BaseRight] = []

        for right in right_tree:
            if isinstance(right, (tuple, list)):
                rights = rights + RightsManager.flat_tree(right)
            else:
                rights.append(right)

        return rights


    @staticmethod
    def tree_to_json(right_tree) -> list:
        """
        Converts to right tree to json
        """
        raw_tree = []

        for node in right_tree:
            if isinstance(node, (tuple, list)):
                raw_tree.append(RightsManager.tree_to_json(node))
            else:
                raw_tree.append(BaseRight.to_dict(node))

        return raw_tree
