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

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.framework.cmdb_dao import CmdbDAO
from cmdb.framework.manager import ManagerBase, ManagerGetError, ManagerDeleteError
from cmdb.framework.manager.error.framework_errors import FrameworkGetError, FrameworkNotFoundError, \
    FrameworkIterationError, FrameworkQueryEmptyError, FrameworkDeleteError, FrameworkUpdateError
from cmdb.framework.manager.results import IterationResult
from cmdb.framework.utils import PublicID, Collection
from cmdb.search import Query, Pipeline
from cmdb.search.query.builder import Builder


class FrameworkQueryBuilder(Builder):
    """Query/Pipeline builder class for the framework manager"""

    def __init__(self):
        """Init a query or a pipeline to None"""
        self.query: Union[Query, Pipeline] = Pipeline([])
        super(FrameworkQueryBuilder, self).__init__()

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
            The `FrameworkQueryBuilder` query pipeline with the parameter contents.
        """
        self.clear()
        self.query = Pipeline([])

        if isinstance(filter, dict):
            self.query.append(self.match_(filter))
        elif isinstance(filter, list):
            for f in filter:
                self.query.append(self.match_(f))

        self.query.append(self.sort_(sort=sort, order=order))
        self.query.append(self.facet_({
            'meta': [self.count_('total')],
            'results': [self.skip_(skip), self.limit_(limit)]
        }))
        return self.query


class FrameworkManager(ManagerBase):
    """Framework manager implementation for all framework based CRUD operations."""

    def __init__(self, collection: Collection, database_manager: DatabaseManagerMongo):
        """
        Set the collection name and the database connection.
        Args:
            collection: Name of the database collection
            database_manager: Active database manager instance
        """
        self.collection: Collection = collection
        self.builder = FrameworkQueryBuilder()
        super(FrameworkManager, self).__init__(database_manager)

    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) -> IterationResult:
        """
        Get multi elements from a collection by passed parameters.

        Notes:
            If you want to get all elements in a collection, just pass a empty dict as filter.

        Args:
            filter: match requirements of field values
            limit: max number of elements to return
            skip: number of elements to skip first
            sort: sort field
            order: sort order
            *args:
            **kwargs:

        Returns:
            IterationResult

        Raises:
            FrameworkIterationError - if something happens during the database aggregation.
        """
        try:
            query: Query = self.builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order)
            aggregation_result = next(super(FrameworkManager, self)._aggregate(self.collection, query))
        except ManagerGetError as err:
            raise FrameworkIterationError(err=err)
        return IterationResult.from_aggregation(aggregation_result)

    def get_many(self, *args, **kwarg) -> List[dict]:
        try:
            cursor_result = super(FrameworkManager, self)._get(self.collection, *args, **kwarg)
        except ManagerGetError as err:
            raise FrameworkGetError(err)
        return list(cursor_result)

    def get(self, public_id: PublicID) -> dict:
        """
        Get a single framework resource by its id.
        Args:
            public_id: ID of the element inside the database.

        Returns:
            Raw result of the element.

        Raises:
            - FrameworkGetError if something breaks with loading the resource from the database.
            - FrameworkNotFoundError if the PublicID is not in the selected database collection.
        """
        try:
            cursor_result = super(FrameworkManager, self)._get(self.collection, filter={'public_id': public_id},
                                                               limit=1)
        except ManagerGetError as err:
            raise FrameworkGetError(err)
        for resource_result in cursor_result.limit(-1):
            return resource_result
        else:
            raise FrameworkNotFoundError(
                f'A resource with the PublicID {public_id} was not found inside {self.collection}')

    def insert(self, resource: dict) -> PublicID:
        return super(FrameworkManager, self)._insert(self.collection, resource)

    def update(self, public_id: PublicID, resource: dict):
        update_result = super(FrameworkManager, self)._update(self.collection, filter={'public_id': public_id},
                                                              data=resource, upsert=False)
        if update_result.matched_count != 1:
            raise FrameworkUpdateError(f'Something happened during the update!')
        return update_result

    def delete(self, public_id: PublicID):
        try:
            delete_result = super(FrameworkManager, self)._delete(self.collection, public_id=public_id)
        except ManagerDeleteError as err:
            raise FrameworkDeleteError(err=err)
        return delete_result
