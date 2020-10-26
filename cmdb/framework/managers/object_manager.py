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
from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.framework import CmdbObject
from cmdb.framework.managers.framework_manager import FrameworkManager
from cmdb.framework.results import IterationResult
from cmdb.manager import ManagerGetError, ManagerIterationError
from cmdb.search import Query


class ObjectManager(FrameworkManager):

    def __init__(self, database_manager: DatabaseManagerMongo):

        super(ObjectManager, self).__init__(CmdbObject.COLLECTION, database_manager=database_manager)

    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) \
            -> IterationResult[CmdbObject]:

        try:
            query: Query = self.builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order)
            aggregation_result = next(self._aggregate(self.collection, query))
        except ManagerGetError as err:
            raise ManagerIterationError(err=err)
        iteration_result: IterationResult[CmdbObject] = IterationResult.from_aggregation(aggregation_result)
        iteration_result.convert_to(CmdbObject)
        return iteration_result
