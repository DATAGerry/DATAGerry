import logging
from typing import List

from cmdb.framework import CmdbCategory, CmdbType
from cmdb.framework.cmdb_errors import ObjectManagerInsertError
from cmdb.search.query.query_builder import QueryBuilder
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
        collection = CmdbCategory.COLLECTION
        new_categories: List[CmdbCategory] = []
        raw_root_categories_old_structure: List[dict] = self.database_manager.find_all(collection=collection,
                                                                                       filter={'parent_id': 0})
        for old_raw_root_category in raw_root_categories_old_structure:
            new_categories.append(self.__convert_category_to_new_structure(old_raw_root_category))

        qb = QueryBuilder()
        qb.query = QueryBuilder.gt_('parent_id', 0)
        raw_sub_categories_old_structure: List[dict] = self.database_manager.find_all(collection=collection,
                                                                                      filter=qb.query)
        for old_raw_sub_category in raw_sub_categories_old_structure:
            parent_id = old_raw_sub_category.get('parent_id')
            parent_index, parent_category = next(
                (parent_index, parent_category) for parent_index, parent_category in enumerate(new_categories) if
                parent_category.get_public_id() == parent_id)
            parent_category.children.append(self.__convert_category_to_new_structure(old_raw_sub_category))
            new_categories[parent_index] = parent_category

        self.database_manager.delete_collection(collection=CmdbCategory.COLLECTION)
        self.database_manager.create_collection(CmdbCategory.COLLECTION)
        self.database_manager.create_indexes(CmdbCategory.COLLECTION, CmdbCategory.get_index_keys())
        for category in new_categories:
            try:
                self.object_manager.insert_category(category)
            except ObjectManagerInsertError as err:
                LOGGER.debug(err)
        super(Update20200512, self).increase_updater_version(20200512)

    def __convert_category_to_new_structure(self, old_raw_category: dict) -> CmdbCategory:
        old_raw_category['meta'] = {
            'icon': old_raw_category.get('icon', '')
        }
        category = CmdbCategory.from_database(old_raw_category)
        category.types = self.__get_types_in_category(old_raw_category.get('public_id'))
        return category

    def __get_types_in_category(self, category_id: int):
        return [type.get('public_id') for type in
                self.database_manager.find_all(collection=CmdbType.COLLECTION,
                                               filter={'category_id': category_id})]

    def __clear_up_types(self):
        pass
