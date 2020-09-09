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
from cmdb.framework import TypeModel
from cmdb.framework.managers.error.framework_errors import FrameworkDeleteError
from cmdb.framework.managers.framework_manager import FrameworkManager
from cmdb.framework.managers.results import IterationResult
from cmdb.framework.utils import PublicID


class TypeManager(FrameworkManager):

    def __init__(self, database_manager: DatabaseManagerMongo):
        super(TypeManager, self).__init__(TypeModel.COLLECTION, database_manager=database_manager)

    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) \
            -> IterationResult[TypeModel]:
        iteration_result: IterationResult[TypeModel] = super(TypeManager, self).iterate(
            filter=filter, limit=limit, skip=skip, sort=sort, order=order)
        iteration_result.convert_to(TypeModel)
        return iteration_result

    def get(self, public_id: Union[PublicID, int]) -> TypeModel:
        result = super(TypeManager, self).get(public_id=public_id)
        return TypeModel.from_data(result)

    def insert(self, type: dict) -> PublicID:
        return super(TypeManager, self).insert(resource=type)

    def update(self, public_id: Union[PublicID, int], type: dict):
        return super(TypeManager, self).update(public_id=public_id, resource=type)

    def delete(self, public_id: Union[PublicID, int]) -> TypeModel:
        raw_category = self.get(public_id=public_id)
        super(TypeManager, self).delete(public_id=public_id)
        return raw_category
