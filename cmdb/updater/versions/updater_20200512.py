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

from cmdb.framework.models.category import CategoryModel
from cmdb.framework.models.type import TypeModel
from cmdb.updater.updater import Updater

from cmdb.errors.manager.object_manager import ObjectManagerInsertError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class Update20200512(Updater):
    """TODO: document"""

    def creation_date(self):
        """TODO: document"""
        return '20200512'


    def description(self):
        """TODO: document"""
        return 'Restructure category system'


    def start_update(self):
        """TODO: document"""
        collection = CategoryModel.COLLECTION
        new_categories: list[CategoryModel] = []
        raw_categories_old_structure: list[dict] = self.dbm.find_all(collection=collection,
                                                                                  filter={})
        for idx, old_raw_category in enumerate(raw_categories_old_structure):
            new_categories.append(self.__convert_category_to_new_structure(old_raw_category, index=idx))

        self.dbm.delete_collection(collection=CategoryModel.COLLECTION)
        self.dbm.create_collection(CategoryModel.COLLECTION)
        self.dbm.create_indexes(CategoryModel.COLLECTION, CategoryModel.get_index_keys())

        for category in new_categories:
            try:
                self.categories_manager.insert_category(category.to_json())
            except ObjectManagerInsertError:
                continue
        self.__clear_up_types()
        super().increase_updater_version(20200512)


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


    def __get_types_in_category(self, category_id: int) -> list[int]:
        """Get a list of type ids by calling the old structure and load the category_id field from types
        Notes:
            Do not use type_instance.category_id here - doesnt exists anymore
        """
        return [type.get('public_id') for type in
                self.dbm.find_all(collection=TypeModel.COLLECTION,
                                               filter={'category_id': category_id})]


    def __clear_up_types(self):
        """Removes the category_id field from type collection"""
        self.dbm.unset_update_many(collection=TypeModel.COLLECTION, filter={}, data='category_id')
