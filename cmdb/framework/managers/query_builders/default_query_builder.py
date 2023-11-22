
# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
"""
This module contains the implementation of the default query builder
"""
import logging
from typing import Union, List

from cmdb.manager.managers import ManagerQueryBuilder
from cmdb.framework.utils import PublicID
from cmdb.search import Query, Pipeline
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.security.acl.builder import AccessControlQueryBuilder
from cmdb.user_management import UserModel
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

class DefaultQueryBuilder(ManagerQueryBuilder):
    """
    The DefaultQueryBuilder builds queries
    """

    def build(self, filter_: Union[List[dict], dict], limit: int, skip: int, sort: str, order: int,
              user: UserModel, permission: AccessControlPermission, *args, **kwargs) -> Union[Query, Pipeline]:
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

        Returns:
            The DefaultQueryBuilder query pipeline with the parameter contents.
        """
        self.clear()
        self.query = Pipeline([])

        if isinstance(filter_, dict):
            self.query.append(self.match_(filter_))
        elif isinstance(filter_, list):
            for pipe in filter_:
                self.query.append(pipe)

        self.query.append(self.sort_(sort=sort, order=order))

        if user and permission:
            self.query += (AccessControlQueryBuilder().build(group_id=PublicID(user.group_id), permission=permission))

        if limit == 0:
            results_query = [self.skip_(limit)]
        else:
            results_query = [self.skip_(skip), self.limit_(limit)]
        self.query += results_query

        return self.query



    def count(self, filter_: Union[List[dict], dict], user: UserModel = None,
              permission: AccessControlPermission = None) -> Union[Query, Pipeline]:
        """
        Count the number of documents in the stages
        Args:
            filter: filter requirement
            user: request user
            permission: acl permission

        Returns:
            Query with count stages.
        """
        self.clear()
        self.query = Pipeline([])

        if isinstance(filter_, dict):
            self.query.append(self.match_(filter_))
        elif isinstance(filter_, list):
            for pipe in filter_:
                self.query.append(pipe)

        if user and permission:
            self.query += (AccessControlQueryBuilder().build(group_id=PublicID(user.group_id), permission=permission))

        self.query.append(self.count_('total'))

        return self.query
