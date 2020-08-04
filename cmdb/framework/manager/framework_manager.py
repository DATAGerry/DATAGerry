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
from typing import TypeVar, Union
from functools import wraps

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.framework import CmdbDAO
from cmdb.framework.manager import ManagerBase
from cmdb.framework.utils import PublicID, Collection
from cmdb.search import Query, Pipeline
from cmdb.search.query.builder import Builder
from cmdb.search.query.pipe_builder import PipelineBuilder

C = TypeVar('C', bound=CmdbDAO)


class FrameworkQueryBuilder(Builder):
    """Query/Pipeline builder class for the framework manager"""

    def __init__(self):
        self.query: Union[Query, Pipeline] = None
        super(FrameworkQueryBuilder, self).__init__()

    def __len__(self):
        return len(self.query)

    def clear(self):
        self.query = None

    def build(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) -> \
            Union[Query, Pipeline]:
        self.clear()
        self.query = [
            {'$match': filter},
            {'$sort': {f'{sort}': order}},
            {'$facet': {
                'meta': [{ '$count': "total"}, { '$addFields': {'page': 3}}],
                'data': [{ '$skip': skip}, { '$limit': limit}]
        }}
        ]
        return self.query


class FrameworkManager(ManagerBase):

    def __init__(self, collection: Collection, database_manager: DatabaseManagerMongo):
        self.collection: Collection = collection
        self.query_builder = FrameworkQueryBuilder()
        super(FrameworkManager, self).__init__(database_manager)

    def get(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs):
        query: Query = self.query_builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order)
        return list(super(FrameworkManager, self)._get(self.collection, filter=filter, limit=limit, skip=skip,
                                                       sort=[(sort, order)]))

    def get_one(self, public_id: PublicID):
        cursor_result = super(FrameworkManager, self)._get(self.collection, filter={'public_id': public_id}, limit=1)
        for result in cursor_result.limit(-1):
            return result
        return None
