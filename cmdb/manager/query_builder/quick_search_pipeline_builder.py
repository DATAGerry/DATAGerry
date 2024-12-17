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

from cmdb.manager.query_builder.pipeline_builder import PipelineBuilder
from cmdb.manager.query_builder.search_references_pipeline_builder import SearchReferencesPipelineBuilder

from cmdb.models.user_model.user import UserModel
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.security.acl.builder import AccessControlQueryBuilder
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                          QuickSearchPipelineBuilder - CLASS                                          #
# -------------------------------------------------------------------------------------------------------------------- #
class QuickSearchPipelineBuilder(PipelineBuilder):
    """TODO: document"""

    def __init__(self, pipeline: list[dict] = None):
        """Init constructor

        Args:
            pipeline: preset a for defined pipeline
        """
        super().__init__(pipeline=pipeline)


    def build(self, search_term, user: UserModel = None, permission: AccessControlPermission = None,
              active_flag: bool = False) -> list[dict]:
        """Build a pipeline query out of search search term"""

        regex = self.regex_('fields.value', f'{search_term}', 'ims')
        pipe_and = self.and_([regex, {'active': {"$eq": True}} if active_flag else {}])
        pipe_match = self.match_(pipe_and)

        # load reference fields in runtime.
        self.pipeline = SearchReferencesPipelineBuilder().build()

        # permission builds
        if user and permission:
            self.pipeline = [*self.pipeline, *(AccessControlQueryBuilder().build(group_id=int(user.group_id),
                                                                                 permission=permission))]
        self.add_pipe(pipe_match)
        self.add_pipe({'$group': {"_id": {'active': '$active'}, 'count': {'$sum': 1}}})
        self.add_pipe({'$group': {'_id': 0,
                                  'levels': {'$push': {'_id': '$_id.active', 'count': '$count'}},
                                  'total': {'$sum': '$count'}}
                      })
        self.add_pipe({'$unwind': '$levels'})
        self.add_pipe({'$sort': {"levels._id": -1}})
        self.add_pipe(
            {'$group': {'_id': 0, 'levels': {'$push': {'count': "$levels.count"}}, "total": {'$avg': '$total'}}})
        self.add_pipe({
            '$project': {
                'total': "$total",
                'active': {'$arrayElemAt': ["$levels", 0]},
                'inactive': {'$arrayElemAt': ["$levels", 1]}
            }})
        self.add_pipe({
            '$project': {
                '_id': 0,
                'active': {'$cond': [{'$ifNull': ["$active", False]}, '$active.count', 0]},
                'inactive': {'$cond': [{'$ifNull': ['$inactive', False]}, '$inactive.count', 0]},
                'total': '$total'
            }})

        return self.pipeline
