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
from typing import TypeVar, Generic, Union, Type

from cmdb.framework import CmdbDAO
# -------------------------------------------------------------------------------------------------------------------- #

C = TypeVar('C', bound=CmdbDAO)


class IterationResult(Generic[C]):
    """Framework Result for a iteration call over a collection"""

    def __init__(self, results: list[Union[C, dict]], total: int):
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
