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
from typing import List

from cmdb.framework.cmdb_object import CmdbObject
from cmdb.framework.cmdb_type import CmdbType
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.cmdb_render import RenderResult, RenderList
from cmdb.search import Search
from cmdb.search.query import Query, Pipeline
from cmdb.search.query.pipe_builder import PipelineBuilder
from cmdb.search.search_result import SearchResult
from cmdb.user_management import User

LOGGER = logging.getLogger(__name__)


class SearcherFramework(Search[CmdbObjectManager]):
    """Framework searcher implementation for object search"""

    def __init__(self, manager: CmdbObjectManager):
        """Normally uses a instance of CmdbObjectManager as manager"""
        super(SearcherFramework, self).__init__(manager=manager)

    def aggregate(self, pipeline: Pipeline, request_user: User = None, limit: int = Search.DEFAULT_LIMIT,
                  skip: int = Search.DEFAULT_SKIP, **kwargs) -> SearchResult[RenderResult]:
        """
        Use mongodb aggregation system with pipeline queries
        Args:
            pipeline (Pipeline): list of requirement pipes
            request_user (User): user who started this search
            limit (int): max number of documents to return
            skip (int): number of documents to be skipped
            **kwargs:
        Returns:
            SearchResult with generic list of RenderResults
        """
        # Insert skip and limit
        plb = PipelineBuilder(pipeline)

        # define search output
        stages: dict = {
            'metadata': [PipelineBuilder.count_('total')],
            'data': [
                PipelineBuilder.skip_(skip),
                PipelineBuilder.limit_(limit)
            ],
            'group': [
                PipelineBuilder.lookup_(CmdbType.COLLECTION, 'type_id', 'public_id', 'lookup_data'),
                PipelineBuilder.unwind_('$lookup_data'),
                PipelineBuilder.project_({'_id': 0, 'type_id': 1, 'label': "$lookup_data.label"}),
                PipelineBuilder.group_("$$ROOT.type_id", {'types': {'$first': "$$ROOT"}, 'total': {'$sum': 1}}),
                PipelineBuilder.project_(
                    {'_id': 0,
                     'searchText': '$types.label',
                     'searchForm': 'type',
                     'searchLabel': '$types.label',
                     'settings': {'types': ['$types.type_id']},
                     'total': 1
                     }),
                PipelineBuilder.sort_("total", -1)
            ]
        }
        plb.add_pipe(PipelineBuilder.facet_(stages))

        raw_search_result = self.manager.aggregate(collection=CmdbObject.COLLECTION, pipeline=plb.pipeline)
        raw_search_result_list = list(raw_search_result)
        try:
            matches_regex = plb.get_regex_pipes_values()
        except Exception as err:
            LOGGER.error(f'Extract regex pipes: {err}')
            matches_regex = []

        if len(raw_search_result_list[0]['data']) > 0:
            raw_search_result_list_entry = raw_search_result_list[0]
            # parse result list
            pre_rendered_result_list = [CmdbObject(**raw_result) for raw_result in raw_search_result_list_entry['data']]
            rendered_result_list = RenderList(pre_rendered_result_list, request_user,
                                              object_manager=self.manager).render_result_list()
            total_results = raw_search_result_list_entry['metadata'][0].get('total', 0)
            group_result_list = raw_search_result_list[0]['group']
        else:
            rendered_result_list = []
            group_result_list = []
            total_results = 0
        # generate output
        search_result = SearchResult[RenderResult](
            results=rendered_result_list,
            total_results=total_results,
            groups=group_result_list,
            alive=raw_search_result.alive,
            matches_regex=matches_regex,
            limit=limit,
            skip=skip
        )
        return search_result

    def search(self, query: Query, request_user: User = None, limit: int = Search.DEFAULT_LIMIT,
               skip: int = Search.DEFAULT_SKIP) -> SearchResult[RenderResult]:
        """
        Uses mongodb find query system
        """
        raise NotImplementedError()
