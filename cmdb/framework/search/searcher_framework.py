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

from cmdb.manager.query_builder.search_pipeline_builder import SearchPipelineBuilder
from cmdb.manager.objects_manager import ObjectsManager

from cmdb.models.user_model.user import UserModel
from cmdb.models.object_model.cmdb_object import CmdbObject
from cmdb.models.type_model.type import TypeModel
from cmdb.framework.rendering.render_list import RenderList
from cmdb.framework.rendering.render_result import RenderResult
from cmdb.framework.search.search_result import SearchResult
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               SearcherFramework - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class SearcherFramework:
    """Framework searcher implementation for object search"""
    DEFAULT_LIMIT: int = 10
    DEFAULT_REGEX: str = ''


    def __init__(self, objects_manager: ObjectsManager):
        self.objects_manager = objects_manager
        super().__init__(objects_manager)


    def aggregate(self, pipeline: list[dict],
                  request_user: UserModel = None,
                  limit: int = DEFAULT_LIMIT,
                  skip: int = 0, **kwargs) -> SearchResult[RenderResult]:
        """
        Use mongodb aggregation system with pipeline queries
        Args:
            pipeline (list[dict]): list of requirement pipes
            request_user (UserModel): user who started this search
            permission (AccessControlPermission) : Permission enum for possible ACL operations..
            limit (int): max number of documents to return
            skip (int): number of documents to be skipped
            **kwargs:
        Returns:
            SearchResult with generic list of RenderResults
        """

        # Insert skip and limit
        plb = SearchPipelineBuilder(pipeline)

        # define search output
        stages: dict = {}

        stages.update({'metadata': [SearchPipelineBuilder.count_('total')]})
        stages.update({'data': [
            SearchPipelineBuilder.skip_(skip),
            SearchPipelineBuilder.limit_(limit)
        ]})

        group_stage: dict = {
            'group': [
                SearchPipelineBuilder.lookup_(TypeModel.COLLECTION, 'type_id', 'public_id', 'lookup_data'),
                SearchPipelineBuilder.unwind_('$lookup_data'),
                SearchPipelineBuilder.project_({'_id': 0, 'type_id': 1, 'label': '$lookup_data.label'}),
                SearchPipelineBuilder.group_('$$ROOT.type_id', {'types': {'$first': '$$ROOT'}, 'total': {'$sum': 1}}),
                SearchPipelineBuilder.project_(
                    {'_id': 0,
                     'searchText': '$types.label',
                     'searchForm': 'type',
                     'searchLabel': '$types.label',
                     'settings': {'types': ['$types.type_id']},
                     'total': 1
                     }),
                SearchPipelineBuilder.sort_('total', -1)
            ]
        }
        stages.update(group_stage)
        plb.add_pipe(SearchPipelineBuilder.facet_(stages))
        raw_search_result = self.objects_manager.aggregate_objects(pipeline=plb.pipeline)
        raw_search_result_list = list(raw_search_result)

        try:
            matches_regex = plb.get_regex_pipes_values()
        except Exception as err:
            #TODO: ERROR-FIX
            LOGGER.error('Extract regex pipes: %s',err)
            matches_regex = []

        if len(raw_search_result_list[0]['data']) > 0:
            raw_search_result_list_entry = raw_search_result_list[0]
            # parse result list
            pre_rendered_result_list = [CmdbObject(**raw_result) for raw_result in raw_search_result_list_entry['data']]

            rendered_result_list = RenderList(pre_rendered_result_list,
                                              request_user,
                                              objects_manager=self.objects_manager).render_result_list()

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


    def search(self, query: dict, request_user: UserModel = None, limit: int = DEFAULT_LIMIT,
               skip: int = 0) -> SearchResult[RenderResult]:
        """Uses mongodb find query system"""
        raise NotImplementedError()
