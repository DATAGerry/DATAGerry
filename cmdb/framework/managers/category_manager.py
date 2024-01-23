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
from typing import Union

from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.framework import CategoryModel
from cmdb.framework.managers.type_manager import TypeManager
from cmdb.framework.models.category import CategoryTree
from cmdb.framework.managers.error.framework_errors import FrameworkDeleteError
from cmdb.manager.managers import ManagerBase
from cmdb.framework.results.iteration import IterationResult
from cmdb.framework.utils import PublicID
from cmdb.manager import ManagerGetError, ManagerIterationError, ManagerUpdateError
from cmdb.search import Pipeline
# -------------------------------------------------------------------------------------------------------------------- #

class CategoryManager(ManagerBase):
    """TODO: document"""

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.__type_manager = TypeManager(database_manager=database_manager)
        super().__init__(CategoryModel.COLLECTION, database_manager=database_manager)


    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) \
            -> IterationResult[CategoryModel]:
        """
        Iterate over a collection of type resources.

        Args:
             filter: match requirements of field values
            limit: max number of elements to return
            skip: number of elements to skip first
            sort: sort field
            order: sort order

        Returns:
            IterationResult: Instance of IterationResult with generic CategoryModel.
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

        iteration_result: IterationResult[CategoryModel] = IterationResult(aggregation_result, total)
        iteration_result.convert_to(CategoryModel)

        return iteration_result


    def get(self, public_id: Union[PublicID, int]) -> CategoryModel:
        """
        Get a single type by its id.

        Args:
            public_id (int): ID of the type.

        Returns:
            CategoryModel: Instance of CategoryModel with data.
        """
        cursor_result = self._get(self.collection, filter={'public_id': public_id}, limit=1)
        for resource_result in cursor_result.limit(-1):
            return CategoryModel.from_data(resource_result)
        raise ManagerGetError(f'Category with ID: {public_id} not found!')


    def insert(self, category: dict) -> PublicID:
        """
        Insert a single category into the system.

        Args:
            category (dict): Raw data of the category.

        Notes:
            If no public id was given, the database manager will auto insert the next available ID.

        Returns:
            int: The Public ID of the new inserted category
        """
        if isinstance(category, CategoryModel):
            category = CategoryModel.to_json(category)
        return self._insert(self.collection, resource=category)


    def update(self, public_id: Union[PublicID, int], category: Union[CategoryModel, dict]):
        """
        Update a existing category in the system.

        Args:
            public_id (int): PublicID of the category in the system.
            category: New category data

        Notes:
            If a CategoryModel instance was passed as type argument, \
            it will be auto converted via the model `to_json` method.
        """
        if isinstance(category, CategoryModel):
            category = CategoryModel.to_json(category)
        update_result = self._update(self.collection, filter={'public_id': public_id}, resource=category)
        if update_result.matched_count != 1:
            raise ManagerUpdateError('Something happened during the update!')
        return update_result


    def delete(self, public_id: Union[PublicID, int]) -> CategoryModel:
        """
        Delete a existing category by its PublicID.

        Args:
            public_id (int): PublicID of the type in the system.

        Returns:
            CategoryModel: The deleted type as its model.
        """
        raw_category = self.get(public_id=public_id)
        delete_result = self._delete(self.collection, filter={'public_id': public_id})
        if delete_result.deleted_count == 0:
            raise FrameworkDeleteError(err='No category matched this public id')
        return raw_category


    @property
    def tree(self) -> CategoryTree:
        """
        Get the complete category list as nested tree.

        Returns:
            CategoryTree: Categories as tree structure.
        """
        # Find all types
        types = self.__type_manager.find({}).results
        categories = self.iterate(
            filter={}, limit=0, skip=0, sort='public_id', order=1).results

        return CategoryTree(categories=categories, types=types)
