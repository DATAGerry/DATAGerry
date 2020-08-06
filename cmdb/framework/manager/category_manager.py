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
from cmdb.framework.manager import ManagerGetError
from cmdb.framework.manager.framework_manager import FrameworkManager
from cmdb.framework.utils import PublicID


class CategoryManager(FrameworkManager):

    def __init__(self, database_manager: DatabaseManagerMongo):
        super(CategoryManager, self).__init__(CategoryDAO.COLLECTION, database_manager=database_manager)

    def get_many(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) \
            -> List[CategoryDAO]:
        return [CategoryDAO.from_data(category) for category in
                super(CategoryManager, self).get_many(filter=filter, limit=limit, skip=skip, sort=sort, order=order)]

    def get(self, public_id: Union[PublicID, int]) -> CategoryDAO:
        result = super(CategoryManager, self).get(public_id=public_id)
        if not result:
            raise ManagerGetError('Category not found!')
        return CategoryDAO.from_data(result)

    def insert(self, category: dict) -> PublicID:
        return super(CategoryManager, self).insert(category)
