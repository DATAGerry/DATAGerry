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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from typing import List, Union

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.framework import CategoryDAO
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.dao.category import CategoryTree
from cmdb.framework.manager import ManagerGetError
from cmdb.framework.manager.error.framework_errors import FrameworkDeleteError
from cmdb.framework.manager.framework_manager import FrameworkManager
from cmdb.framework.manager.results import IterationResult
from cmdb.framework.utils import PublicID


class CategoryManager(FrameworkManager):

    def __init__(self, database_manager: DatabaseManagerMongo):
        super(CategoryManager, self).__init__(CategoryDAO.COLLECTION, database_manager=database_manager)

    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) \
            -> IterationResult[CategoryDAO]:
        iteration_result: IterationResult[CategoryDAO] = super(CategoryManager, self).iterate(
            filter=filter, limit=limit, skip=skip, sort=sort, order=order)
        iteration_result.convert_to(CategoryDAO)
        return iteration_result

    def get(self, public_id: Union[PublicID, int]) -> CategoryDAO:
        result = super(CategoryManager, self).get(public_id=public_id)
        return CategoryDAO.from_data(result)

    def insert(self, category: dict) -> PublicID:
        return super(CategoryManager, self).insert(resource=category)

    def delete(self, public_id: Union[PublicID, int]) -> CategoryDAO:
        raw_category = self.get(public_id=public_id)
        delete_result = super(CategoryManager, self).delete(public_id=public_id)
        if delete_result.deleted_count == 0:
            raise FrameworkDeleteError(err='No document matched this public id')
        return raw_category

    @property
    def tree(self) -> CategoryTree:
        # Currently only a work around until the other manager were converted to the new format - MH
        types = CmdbObjectManager(database_manager=self._database_manager).get_all_types()
        categories = [CategoryDAO.from_data(category) for category in
                      super(CategoryManager, self).get_many({})]

        return CategoryTree(categories=categories, types=types)
