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

from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.exportd.exportd_logs.exportd_log import ExportdJobLog
from cmdb.manager.managers import ManagerBase as ExportDManager
from cmdb.framework.results import IterationResult
from cmdb.manager import ManagerIterationError, ManagerGetError
from cmdb.search import Pipeline


class ExportDLogManager(ExportDManager):

    def __init__(self, database_manager: DatabaseManagerMongo):
        """
        Constructor of `ExportDLogManager`

        Args:
            database_manager: Connection to the database class.
        """
        super(ExportDLogManager, self).__init__(ExportdJobLog.COLLECTION, database_manager=database_manager)

    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) \
            -> IterationResult[ExportdJobLog]:
        """
        Iterate over a collection of exportd logs resources.

        Args:
            filter: match requirements of field values
            limit: max number of elements to return
            skip: number of elements to skip first
            sort: sort field
            order: sort order

        Returns:
            IterationResult: Instance of IterationResult with generic ExportdJobLog.
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
            raise ManagerIterationError(err=err)
        iteration_result: IterationResult[ExportdJobLog] = IterationResult(aggregation_result, total)
        iteration_result.convert_to(ExportdJobLog)
        return iteration_result
