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
import logging
from typing import Union

from cmdb.security.acl.permission import AccessControlPermission
from cmdb.security.acl.builder import AccessControlQueryBuilder
from cmdb.user_management import UserModel

from cmdb.framework.models.log import CmdbObjectLog, LogAction

from .builder import Builder
from .builder_parameters import BuilderParameters
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class BaseQueryBuilder(Builder):
    """TODO: document"""
    def __init__(self):
        self.query: list[dict] = []
        super().__init__()


    def __len__(self):
        """Get the length of the query"""
        return len(self.query)

# ------------------------------------------------- PUBLIC FUNCTIONS ------------------------------------------------- #

    def build(self,
              builder_params: BuilderParameters,
              user: UserModel = None,
              permission: AccessControlPermission = None) -> list[dict]:
        """
        Converts the parameters from the call to a MongoDB aggregation pipeline
        Args:
            criteria Union[dict, list[dict]]: Query/Queries which the elements have to match
            limit: Max number of documents to return
            skip: Number of documents to skip first
            sort: Sort field
            order: Sort order
        Returns:
            Union[dict, list[dict]]: The build query
        """
        self.query = self.__init_query(builder_params.get_criteria())

        self.query.append(self.sort_(builder_params.get_sort(), builder_params.get_order()))
        self.query.append(self.skip_(builder_params.get_skip()))

        if user and permission:
            self.query.extend(AccessControlQueryBuilder().build(user.group_id, permission))

        if builder_params.has_limit():
            self.query.append(self.limit_(builder_params.get_limit()))

        return self.query


    def count(self,
              criteria: Union[dict, list[dict]],
              user: UserModel = None,
              permission: AccessControlPermission = None) -> list[dict]:
        """
        Count the number of documents
        Args:
            criteria: Filter for documents

        Returns:
            Query with count stages
        """
        self.query = self.__init_query(criteria)

        if user and permission:
            self.query.extend(AccessControlQueryBuilder().build(user.group_id, permission))

        self.query.append(self.count_('total'))

        return self.query

# ------------------------------------------------- HELPER - SECTION ------------------------------------------------- #

    def clear(self):
        """`Delete` the query content"""
        self.query = None


    def __init_query(self, criteria: Union[dict, list[dict]]) -> list[dict]:
        """
        Initialises the query with valid format

        Args:
            criteria (Union[dict, list[dict]]): Filter which should be applied

        Returns:
            list[dict]: The initialised query
        """
        self.clear()
        query: list[dict] = []

        if isinstance(criteria, dict):
            query.append(self.match_(criteria))

        elif isinstance(criteria, list):
            for pipe in criteria:
                query.append(pipe)

        return query


    def prepare_log_query(self, object_exists: bool = True) -> list[dict]:
        """
        Prepares the query for logs

        Args:
            object_exists (bool): If the referenced object of the log still exists

        Returns:
            list[dict]: the prepared query for object logs
        """
        query = []

        query.append({'$match': {
            'log_type': CmdbObjectLog.__name__,
            'action': {
                '$ne': LogAction.DELETE.value
            }
        }})

        # query.append({"$lookup": {
        #     "from": "framework.objects",
        #     "let": {"ref_id": "$object_id"},
        #     "pipeline": [{'$match': {'$expr': {'$eq': ["$public_id", '$$ref_id']}}}],
        #     "as": "object"
        # }})

        query.append({
            "$lookup": {
                "from": "framework.objects",
                "localField": "object_id",
                "foreignField": "public_id",
                "as": "object"
            }
        })

        query.append({'$unwind': {'path': '$object', 'preserveNullAndEmptyArrays': True}})
        query.append({'$match': {'object': {'$exists': object_exists}}})

        return query
