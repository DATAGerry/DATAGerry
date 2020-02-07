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
from typing import List, Any

from cmdb.search.query import Query

LOGGER = logging.getLogger(__name__)


class QueryBuilder:

    def __init__(self, preset: Query = None):
        self._query: Query = preset or Query({})

    @property
    def query(self) -> Query:
        return self._query

    @query.setter
    def query(self, value: dict):
        self._query = Query(value)

    def clear(self):
        self.query = Query({})

    def __len__(self) -> int:
        return len(self.query)

    def build(self, params: dict) -> Query:
        """Build query from form data"""
        LOGGER.debug(f'[QueryBuilder] Build query out of {params}')

        # Generate text searches
        text_searches: List[dict] = [
            QueryBuilder.element_match_('fields', QueryBuilder.regex_('value', text_search["searchText"], 'imsx'))
            for text_search in params if text_search['searchForm'] == 'textSearch']
        if len(text_searches) > 0:
            self.query = QueryBuilder.or_(text_searches)

        # Generate public id searches
        public_id_searches: List[dict] = [QueryBuilder.eq_('public_id', int(text_search["searchText"]))
                                          for text_search in params if
                                          text_search['searchForm'] == 'publicID']
        if len(public_id_searches) > 0:
            self.query = QueryBuilder.and_([self.query, QueryBuilder.and_(public_id_searches)])

        # Generate type id searches
        type_id_searches: List[dict] = [QueryBuilder.eq_('type_id', int(text_search['settings']['publicID']))
                                        for text_search in params if
                                        text_search['searchForm'] == 'typeID']
        if len(type_id_searches) > 0:
            self.query = QueryBuilder.and_([self.query, QueryBuilder.and_(type_id_searches)])

        return self.query

    # Logical Query Operators
    @staticmethod
    def and_(expressions: List[dict]) -> dict:
        """Joins query clauses with a logical AND."""
        return {'$and': expressions}

    @staticmethod
    def or_(expressions: List[dict]) -> dict:
        """Joins query clauses with a logical OR."""
        return {'$or': expressions}

    @staticmethod
    def not_(expression: dict) -> dict:
        """Inverts the effect of a query expression."""
        return {'$not': expression}

    @staticmethod
    def nor_(expressions: List[dict]) -> dict:
        """Joins query clauses with a logical NOR."""
        return {'$nor': expressions}

    # Comparison
    @staticmethod
    def eq_(field: str, value: Any) -> dict:
        """Matches values that are equal to a specified value."""
        return {field: {'$eq': value}}

    @staticmethod
    def gt_(field: str, value: Any) -> dict:
        """Matches values that are greater than a specified value."""
        return {field: {'$gt': value}}

    @staticmethod
    def gte_(field: str, value: Any) -> dict:
        """Matches values that are greater than or equal to a specified value."""
        return {field: {'$gte': value}}

    @staticmethod
    def in_(field: str, values: List[Any]) -> dict:
        """Matches any of the values specified in an array."""
        return {field: {'$in': values}}

    @staticmethod
    def lt_(field: str, value: Any) -> dict:
        """Matches values that are less than a specified value."""
        return {field: {'$lt': value}}

    @staticmethod
    def lte_(field: str, value: Any) -> dict:
        """Matches values that are less than or equal to a specified value."""
        return {field: {'$lte': value}}

    @staticmethod
    def ne_(field: str, value: Any) -> dict:
        """Matches all values that are not equal to a specified value."""
        return {field: {'$ne': value}}

    @staticmethod
    def nin_(field: str, values: List[Any]) -> dict:
        """Matches none of the values specified in an array."""
        return {field: {'$nin': values}}

    # Element
    @staticmethod
    def exists_(field: str, exist: bool = True) -> dict:
        """Matches documents that have the specified field."""
        return {field: {'$exists': exist}}

    @staticmethod
    def element_match_(field: str, criteria: dict) -> dict:
        """If element in the array field matches all the specified $elemMatch conditions."""
        return {field: {'$elemMatch': criteria}}

    # Evaluation
    @staticmethod
    def regex_(field: str, regex: str, options: str = '') -> dict:
        """Where values match a specified regular expression"""
        return {field: {'$regex': regex, '$options': options}}
