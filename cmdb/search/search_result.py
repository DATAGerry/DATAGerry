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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import TypeVar, Generic, List

R: TypeVar = TypeVar('R')


class SearchResultMap(Generic[R]):

    def __init__(self, result: R, matches: [] = None):
        self.result = result
        self.matches = matches

    def to_json(self) -> dict:
        return {'result': self.result.__dict__, 'matches': self.matches}


class SearchResults(Generic[R]):

    def __init__(self, results: List[R], total_results: int, limit: int, skip: int):
        self.limit: int = limit
        self.skip: int = skip
        self.total_results: int = total_results
        self.results: List[SearchResultMap] = [SearchResultMap[R](result=result) for result in results]

    def __len__(self):
        return len(self.results)

    def to_json(self) -> dict:
        return {
            'limit': self.limit,
            'skip': self.skip,
            'total_results': self.total_results,
            'number_of_results': len(self),
            'results': self.results
        }
