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
from cmdb.search.query import Query
from cmdb.manager.query_builder.builder import Builder
# -------------------------------------------------------------------------------------------------------------------- #

class QueryBuilder(Builder):
    """Query builder for database find search"""

    def __init__(self, query: Query = None):
        self._query: Query = query or Query({})


    def __len__(self):
        return len(self.query)


    def clear(self):
        self.query = Query({})


    @property
    def query(self) -> Query:
        """TODO: document"""
        return self._query


    @query.setter
    def query(self, value: dict):
        self._query = Query(value)


    def build(self, *args, **kwargs) -> Query:
        """TODO: document"""
        raise NotImplementedError()
