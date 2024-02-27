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
"""
This module contains the implementation of the SectionTemplatesManager
"""
import logging
from queue import Queue
from typing import Union

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.framework.managers.type_manager import TypeManager

from cmdb.event_management.event import Event
from cmdb.framework import CategoryModel
from cmdb.framework.models.category import CategoryTree
from cmdb.framework.results.iteration import IterationResult
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel

from cmdb.errors.manager import ManagerInsertError,\
                                ManagerGetError,\
                                ManagerIterationError,\
                                ManagerUpdateError

from .base_manager import BaseManager
from .query_builder.base_query_builder import BaseQueryBuilder
from . query_builder.builder_parameters import BuilderParameters
# -------------------------------------------------------------------------------------------------------------------- #
LOGGER = logging.getLogger(__name__)


class CategoriesManager(BaseManager):
    """
    The CategoriesManager handles the interaction between the Categories-API and the Database
    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, event_queue: Union[Queue, Event] = None):
        """
        Set the database connection and the queue for sending events

        Args:
            database_manager (DatabaseManagerMongo): Active database managers instance.
            event_queue (Queue, Event): The queue for sending events or the created event to send
        """
        self.event_queue = event_queue
        self.query_builder = BaseQueryBuilder()
        self.type_manager = TypeManager(dbm)
        super().__init__(CategoryModel.COLLECTION, dbm)


    @property
    def tree(self) -> CategoryTree:
        """
        Get the complete category list as nested tree.

        Returns:
            CategoryTree: Categories as tree structure.
        """
        # Find all types
        types = self.type_manager.find({}).results
        build_params = BuilderParameters({})
        categories = self.iterate(build_params).results

        return CategoryTree(categories, types)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_category(self, category: dict) -> int:
        """
        Insert a ategory into the database

        Args:
            category (dict): Raw data of the category
        Returns:
            int: The public_id of the new inserted category
        """
        if isinstance(category, CategoryModel):
            category = CategoryModel.to_json(category)

        try:
            ack = self.insert(category)
        except Exception as error:
            raise ManagerInsertError(error) from error

        return ack

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def iterate(self,
                builder_params: BuilderParameters,
                user: UserModel = None,
                permission: AccessControlPermission = None) -> IterationResult[CategoryModel]:
        """
        Performs an aggregation on the database
        Args:
            builder_params (BuilderParameters): Contains input to identify the target of action
            user (UserModel, optional): User requesting this action
            permission (AccessControlPermission, optional): Permission which should be checked for the user
        Raises:
            ManagerIterationError: Raised when something goes wrong during the aggregate part
            ManagerIterationError: Raised when something goes wrong during the building of the IterationResult
        Returns:
            IterationResult[CategoryModel]: Result which matches the Builderparameters
        """
        try:
            query: list[dict] = self.query_builder.build(builder_params,user, permission)
            count_query: list[dict] = self.query_builder.count(builder_params.get_criteria())

            aggregation_result = list(self.aggregate(query))
            total_cursor = self.aggregate(count_query)

            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']

        except ManagerGetError as err:
            raise ManagerIterationError(err) from err

        try:
            iteration_result: IterationResult[CategoryModel] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CategoryModel)
        except Exception as err:
            raise ManagerIterationError(err) from err

        return iteration_result

# ------------------------------------------------- HELPER FUNCTIONS ------------------------------------------------- #

    def reset_children_categories(self, public_id: int) -> None:
        """
        Sets the parent attribute to null for all children of a category

        Args:
            public_id (int): public_id of parent category
        """
        try:
            # Get all children
            cursor_result = self.get(filter={'parent': public_id})

            # Update all child categories
            for category in cursor_result:
                category['parent'] = None
                category_public_id = category['public_id']
                self.update({'public_id':category_public_id}, category)
        except ManagerGetError as err:
            raise ManagerGetError(err) from err
        except ManagerUpdateError as err:
            raise ManagerUpdateError(err) from err
