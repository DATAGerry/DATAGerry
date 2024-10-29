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
"""This module contains the implementation of the SectionTemplatesManager"""
import logging
from queue import Queue
from typing import Union

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.types_manager import TypesManager
from cmdb.manager.base_manager import BaseManager

from cmdb.event_management.event import Event
from cmdb.framework.models.category import CategoryModel
from cmdb.framework.models.category_model.category_tree import CategoryTree
from cmdb.framework.results.iteration import IterationResult
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management.models.user import UserModel
from cmdb.manager.query_builder.builder_parameters import BuilderParameters

from cmdb.errors.manager import ManagerInsertError,\
                                ManagerGetError,\
                                ManagerIterationError,\
                                ManagerUpdateError,\
                                ManagerDeleteError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               CategoriesManager - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class CategoriesManager(BaseManager):
    """
    The CategoriesManager handles the interaction between the Categories-API and the Database
    Extends: BaseManager
    Depends: TypesManager
    """

    def __init__(self, dbm: MongoDatabaseManager, event_queue: Union[Queue, Event] = None, database:str = None):
        """
        Set the database connection and the queue for sending events

        Args:
            database_manager (MongoDatabaseManager): Active database managers instance.
            event_queue (Queue, Event): The queue for sending events or the created event to send
        """
        self.event_queue = event_queue

        if database:
            dbm.connector.set_database(database)

        self.types_manager = TypesManager(dbm)
        super().__init__(CategoryModel.COLLECTION, dbm)


    @property
    def tree(self) -> CategoryTree:
        """
        Get the complete category list as nested tree.

        Returns:
            CategoryTree: Categories as tree structure.
        """
        # Find all types
        types = self.types_manager.find_types({}).results
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

    def get_category(self, public_id: int):
        """TODO: document"""
        try:
            return self.get_one(public_id)
        except Exception as err:
            #ERROR-FIX
            raise ManagerGetError(str(err)) from err


    def iterate(self,
                builder_params: BuilderParameters,
                user: UserModel = None,
                permission: AccessControlPermission = None) -> IterationResult[CategoryModel]:
        """
        TODO: document
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params, user, permission)

            iteration_result: IterationResult[CategoryModel] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CategoryModel)
        except Exception as err:
            raise ManagerIterationError(err) from err

        return iteration_result


    def get_categories_by(self, sort='public_id', **requirements: dict) -> list[CategoryModel]:
        """Get a list of categories by special requirements"""
        try:
            raw_categories = self.get_many_from_other_collection(collection=CategoryModel.COLLECTION,
                                                                 sort=sort,
                                                                 **requirements)
        except Exception as error:
            #ERROR-FIX (need category get error)
            raise ManagerGetError(error) from error
        try:
            return [CategoryModel.from_data(category) for category in raw_categories]
        except Exception as error:
            #ERROR-FIX (need category init error)
            raise ManagerGetError(error) from error


    def count_categories(self):
        """
        Returns the number of categories

        Args:
            criteria (dict): Filter for counting documents like {'type_id: 1} 

        Raises:
            ObjectManagerGetError: When an error occures during counting objects

        Returns:
            (int): Returns the number of documents with the given criteria
        """
        try:
            categories_count = self.count_documents(self.collection)
        except Exception as err:
            #ERROR-FIX (CategoriesManagerGetError)
            raise ManagerGetError(err) from err

        return categories_count

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_category(self, public_id:int, data: dict):
        """TODO: document"""
        try:
            self.update({'public_id':public_id}, CategoryModel.to_json(data))
        except Exception as err:
            #ERROR-FIX
            raise ManagerUpdateError(str(err)) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_category(self, public_id: int):
        """TODO: document"""
        try:
            return self.delete({'public_id':public_id})
        except Exception as err:
            #ERROR-FIX
            raise ManagerDeleteError(str(err)) from err

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
            LOGGER.debug("[reset_children_categories] ManagerUpdateError: %s", err.message)
            raise ManagerUpdateError(err) from err
