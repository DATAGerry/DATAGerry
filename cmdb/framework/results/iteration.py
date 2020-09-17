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

from typing import TypeVar, Generic, List, Union, Type

from cmdb.framework import CmdbDAO

C = TypeVar('C', bound=CmdbDAO)


class IterationResult(Generic[C]):
    """Framework Result for a iteration call over a collection"""

    def __init__(self, results: List[Union[C, dict]], total: int):
        """
        Constructor of IterationResult
        Args:
            results: List of raw oder generic database results
            total: Total number of elements in the query.
        """
        self.results = results
        self.count = len(self.results)
        self.total = total

    def convert_to(self, c: Type[C]):
        """Converts the results inside the instance to a passed CmdbDAO subtype."""
        self.results = [c.from_data(result) for result in self.results]

    @classmethod
    def from_aggregation(cls, aggregation):
        """
        Creates a IterationResult instance from a aggregation result.
        This class method is wrapper if the aggregation comes from the FrameworkQueryBuilder collection iteration.

        Args:
            aggregation: The database aggregation result.

        Notes:
            The structure of the aggregation is based on the passed query from the FrameworkQueryBuilder.

        Returns:
            A IterationResult instance.
        """
        if len(aggregation['results']) == 0:
            return cls(aggregation['results'], total=0)
        return cls(aggregation['results'], total=aggregation['meta'][0]['total'])