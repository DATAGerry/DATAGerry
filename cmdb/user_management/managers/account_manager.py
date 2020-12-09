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
from typing import Union, List

from cmdb.database.managers import DatabaseManagerMongo
from cmdb.framework.results import IterationResult
from cmdb.framework.utils import Collection, PublicID
from cmdb.manager import ManagerBase
from cmdb.search import Pipeline, Query
from cmdb.search.query.builder import Builder


class AccountManagerQueryBuilder(Builder):
    """Query/Pipeline builder class for the user management managers"""

    def __init__(self):
        """Init a query or a pipeline to None"""
        self.query: Union[Query, Pipeline] = Pipeline([])
        super(AccountManagerQueryBuilder, self).__init__()

    def __len__(self):
        """Get the length of the query"""
        return len(self.query)

    def clear(self):
        """`Delete` the query content"""
        self.query = None

    def build(self, filter: Union[List[dict], dict], limit: int, skip: int, sort: str, order: int, *args, **kwargs) -> \
            Union[Query, Pipeline]:
        """
        Converts the parameters from the call to a mongodb aggregation pipeline

        Args:
            filter: dict or list of dict query/queries which the elements have to match.
            limit: max number of documents to return.
            skip: number of documents to skip first.
            sort: sort field
            order: sort order
            *args:
            **kwargs:

        Returns:
            The `AccountManagerQueryBuilder` query pipeline with the parameter contents.
        """
        self.clear()
        self.query = Pipeline([])

        if isinstance(filter, dict):
            self.query.append(self.match_(filter))
        elif isinstance(filter, list):
            for pipe in filter:
                self.query.append(pipe)

        if limit == 0:
            results_query = [self.skip_(limit)]
        else:
            results_query = [self.skip_(skip), self.limit_(limit)]

        self.query.append(self.sort_(sort=sort, order=order))
        self.query.append(self.facet_({
            'meta': [self.count_('total')],
            'results': results_query
        }))
        return self.query


class AccountManager(ManagerBase):
    """Framework managers implementation for all framework based CRUD operations."""

    def __init__(self, collection: Collection, database_manager: DatabaseManagerMongo = None):
        """
        Set the collection name and the database connection.

        Args:
            collection: Name of the database collection
            database_manager: Active database managers instance
        """
        self.collection: Collection = collection
        self.builder = AccountManagerQueryBuilder()
        super(AccountManager, self).__init__(database_manager)

    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) -> IterationResult:
        raise NotImplementedError

    def get(self, *args, **kwargs) -> dict:
        raise NotImplementedError

    def insert(self, resource: dict, *args, **kwargs) -> PublicID:
        raise NotImplementedError

    def update(self, resource: dict, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError
