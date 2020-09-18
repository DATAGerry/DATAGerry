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
import logging
from typing import TypeVar, Generic, List

from bson import Regex

LOGGER = logging.getLogger(__name__)
R: TypeVar = TypeVar('R')


class SearchResultMap(Generic[R]):
    """Result mapper for Result/Match binding
    """

    def __init__(self, result: R, matches: List[str] = None):
        self.result = result
        self.matches: List[str] = matches

    def to_json(self) -> dict:
        """Quick convert for the database"""
        return {'result': self.result.__dict__, 'matches': self.matches}


class SearchResult(Generic[R]):
    """Generic search result base"""

    def __init__(self, results: List[R], total_results: int, groups: List[R], alive: bool, limit: int, skip: int,
                 matches_regex: List[str] = None):
        """
        Constructor for search result
        Args:
            results: List of generic search results
            total_results: total number of results
            alive: flag if spliced search result has more data in database
            limit: max number of results to return
            skip: start of index value for the search
            matches_regex: list of text regex values
        """
        self.limit: int = limit
        self.skip: int = skip
        self.total_results: int = total_results
        self.alive = alive
        self.groups = groups
        self.results: List[SearchResultMap] = [
            SearchResultMap[R](result=result, matches=self.find_match_fields(result, matches_regex)) for result in
            results]

    def __len__(self):
        """
        Call number of results
        Returns:
            number of found objects
        """
        return len(self.results)

    @staticmethod
    def find_match_fields(result: R, possible_regex_list=None):
        """
        Get list of matched fields inside the searchresult
        Args:
            result: Generic search result
            possible_regex_list: list of text regex from the pipeline builder

        Returns:
            list of fields where the regex matched
        """
        matched_fields = []
        fields = result.fields
        if not possible_regex_list:
            return None
        for regex_ in possible_regex_list:
            try:
                runtime_regex = Regex(regex_, 'imsx').try_compile()
            except Exception:
                runtime_regex = regex_
            for field in fields:
                try:
                    res = runtime_regex.findall(str(field.get('value')))
                    if len(res) > 0:
                        matched_fields.append(field)
                except Exception:
                    continue
        if len(matched_fields) > 0:
            return matched_fields
        return None

    def to_json(self) -> dict:
        return {
            'limit': self.limit,
            'skip': self.skip,
            'groups': self.groups,
            'total_results': self.total_results,
            'number_of_results': len(self),
            'results': self.results
        }
