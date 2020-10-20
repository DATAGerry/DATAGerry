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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from typing import List

from cmdb.framework import CategoryModel, TypeModel
from cmdb.framework.cmdb_errors import ObjectManagerInsertError
from cmdb.updater.updater import Updater

LOGGER = logging.getLogger(__name__)


class Update20200512(Updater):

    def author(self):
        return 'mh'

    def creation_date(self):
        return '20200512'

    def description(self):
        return 'Restructure category system'

    def increase_updater_version(self, value):
        raise NotImplementedError

    def start_update(self):
        collection = CategoryModel.COLLECTION
        new_categories: List[CategoryModel] = []
        raw_categories_old_structure: List[dict] = self.database_manager.find_all(collection=collection,
                                                                                  filter={})
        for idx, old_raw_category in enumerate(raw_categories_old_structure):
            new_categories.append(self.__convert_category_to_new_structure(old_raw_category, index=idx))

        """qb = QueryBuilder()
        qb.query = QueryBuilder.and_(
            [QueryBuilder.gt_('parent_id', 0), {'parent_id': QueryBuilder.not_(QueryBuilder.type_(10))}])

        raw_sub_categories_old_structure: List[dict] = self.database_manager.find_all(collection=collection,
                                                                                      filter=qb.query)"""

        self.database_manager.delete_collection(collection=CategoryModel.COLLECTION)
        self.database_manager.create_collection(CategoryModel.COLLECTION)
        self.database_manager.create_indexes(CategoryModel.COLLECTION, CategoryModel.get_index_keys())
        for category in new_categories:
            try:
                self.object_manager.insert_category(category)
            except ObjectManagerInsertError:
                continue
        self.__clear_up_types()
        super(Update20200512, self).increase_updater_version(20200512)

    def __convert_category_to_new_structure(self, old_raw_category: dict, index: int) -> CategoryModel:
        """Converts a category from old < 20200512 structure to new format """
        old_raw_category['meta'] = {
            'icon': old_raw_category.get('icon', None),
            'order': index
        }
        parent = old_raw_category.get('parent_id', None)
        if parent == 0:
            parent = None

        old_raw_category['parent'] = parent
        category = CategoryModel.from_data(old_raw_category)
        category.types = self.__get_types_in_category(old_raw_category.get('public_id'))
        return category

    def __get_types_in_category(self, category_id: int) -> List[int]:
        """Get a list of type ids by calling the old structure and load the category_id field from types
        Notes:
            Do not use type_instance.category_id here - doesnt exists anymore
        """
        return [type.get('public_id') for type in
                self.database_manager.find_all(collection=TypeModel.COLLECTION,
                                               filter={'category_id': category_id})]

    def __clear_up_types(self):
        """Removes the category_id field from type collection"""
        self.database_manager.unset_update_many(collection=TypeModel.COLLECTION, filter={}, data='category_id')
