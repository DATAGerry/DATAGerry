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


class ListResult(Generic[C]):
    """Framework Result for a list call over a collection."""

    def __init__(self, results: List[Union[C, dict]]):
        """
        Constructor of `ListResult`.

        Args:
            results: List of results
        """
        self.results = results
        self._total = None

    @property
    def total(self):
        """Property setter for total lazy calc"""
        if not self._total:
            self._total = len(self.results)
        return self._total
