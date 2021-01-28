# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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

from cmdb.database.managers import DatabaseManagerMongo
from cmdb.exportd import ExportdJob
from cmdb.framework.managers.framework_manager import FrameworkManager as ExportDManager
from cmdb.framework.results import IterationResult
from cmdb.manager import ManagerIterationError, ManagerGetError
from cmdb.search import Query


class ExportDJobManager(ExportDManager):

    def __init__(self, database_manager: DatabaseManagerMongo):
        """
        Constructor of `ExportDJobManager`

        Args:
            database_manager: Connection to the database class.
        """
        super(ExportDJobManager, self).__init__(ExportdJob.COLLECTION, database_manager=database_manager)

    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) \
            -> IterationResult[ExportdJob]:
        """
        Iterate over a collection of exportd jobs resources.

        Args:
            filter: match requirements of field values
            limit: max number of elements to return
            skip: number of elements to skip first
            sort: sort field
            order: sort order

        Returns:
            IterationResult: Instance of IterationResult with generic ExportdJob.
        """

        try:
            query: Query = self.builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order)
            aggregation_result = next(self._aggregate(self.collection, query))
        except ManagerGetError as err:
            raise ManagerIterationError(err=err)
        iteration_result: IterationResult[ExportdJob] = IterationResult.from_aggregation(aggregation_result)
        iteration_result.convert_to(ExportdJob)
        return iteration_result
