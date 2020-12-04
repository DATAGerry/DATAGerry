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
from cmdb.framework import CmdbObject
from cmdb.framework.managers.framework_manager import FrameworkManager, FrameworkQueryBuilder
from cmdb.framework.results import IterationResult
from cmdb.manager import ManagerGetError, ManagerIterationError
from cmdb.search import Query, Pipeline
from cmdb.security.acl.builder import AccessControlQueryBuilder
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel


class ObjectQueryBuilder(FrameworkQueryBuilder):

    def __init__(self):
        super(ObjectQueryBuilder, self).__init__()

    def build(self, filter: Union[List[dict], dict], limit: int, skip: int, sort: str, order: int,
              user: UserModel = None, permission: AccessControlPermission = None, *args, **kwargs) -> \
            Union[Query, Pipeline]:
        """
        Converts the parameters from the call to a mongodb aggregation pipeline
        Args:
            filter: dict or list of dict query/queries which the elements have to match.
            limit: max number of documents to return.
            skip: number of documents to skip first.
            sort: sort field
            order: sort order
            user: request user
            permission: AccessControlPermission
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
            for pipe in filter:
                self.query.append(pipe)

        if user and permission:
            self.query += (AccessControlQueryBuilder().build(group_id=user.group_id, permission=permission))

        if limit == 0:
            results_query = [self.skip_(limit)]
        else:
            results_query = [self.skip_(skip), self.limit_(limit)]

        # TODO: Remove nasty quick hack
        if sort.startswith('fields'):
            sort_value = sort[7:]
            self.query.append({"$addFields": {
                "order": {
                    "$filter": {
                        "input": "$fields",
                        "as": "fields",
                        "cond": {"$eq": ["$$fields.name", sort_value]}
                    }
                }
            }})
            self.query.append({'$sort': {'order': order}})
        else:
            self.query.append(self.sort_(sort=sort, order=order))

        self.query.append(self.facet_({
            'meta': [self.count_('total')],
            'results': results_query
        }))
        return self.query


class ObjectManager(FrameworkManager):

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.object_builder = ObjectQueryBuilder()
        super(ObjectManager, self).__init__(CmdbObject.COLLECTION, database_manager=database_manager)

    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int,
                user: UserModel = None, permission: AccessControlPermission = None, *args, **kwargs) \
            -> IterationResult[CmdbObject]:

        try:
            query: Query = self.object_builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order,
                                                     user=user, permission=permission)
            aggregation_result = next(self._aggregate(self.collection, query))
        except ManagerGetError as err:
            raise ManagerIterationError(err=err)
        iteration_result: IterationResult[CmdbObject] = IterationResult.from_aggregation(aggregation_result)
        iteration_result.convert_to(CmdbObject)
        return iteration_result
