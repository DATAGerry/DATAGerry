# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.exportd import ExportdJob
from cmdb.manager.managers import ManagerBase as ExportDManager
from cmdb.framework.results import IterationResult
from cmdb.manager import ManagerIterationError, ManagerGetError
from cmdb.search import Pipeline
# -------------------------------------------------------------------------------------------------------------------- #

class ExportDJobManager(ExportDManager):
    """TODO: document"""
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
            query: Pipeline = self.builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order)
            count_query: Pipeline = self.builder.count(filter=filter)
            aggregation_result = list(self._aggregate(self.collection, query))
            total_cursor = self._aggregate(self.collection, count_query)
            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']
        except ManagerGetError as err:
            raise ManagerIterationError(err) from err
        iteration_result: IterationResult[ExportdJob] = IterationResult(aggregation_result, total)
        iteration_result.convert_to(ExportdJob)
        return iteration_result
