# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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


import logging
from typing import List

from cmdb.framework.cmdb_object import CmdbObject
from cmdb.framework.models.type import TypeModel
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.cmdb_render import RenderResult, RenderList
from cmdb.search import Search
from cmdb.search.params import SearchParam
from cmdb.search.query import Query, Pipeline
from cmdb.search.query.pipe_builder import PipelineBuilder
from cmdb.search.search_result import SearchResult
from cmdb.user_management import UserModel
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.security.acl.builder import AccessControlQueryBuilder

LOGGER = logging.getLogger(__name__)


class QuickSearchPipelineBuilder(PipelineBuilder):

    def __init__(self, pipeline: Pipeline = None):
        """Init constructor
        Args:
            pipeline: preset a for defined pipeline
        """
        super(QuickSearchPipelineBuilder, self).__init__(pipeline=pipeline)

    def build(self, search_term, user: UserModel = None, permission: AccessControlPermission = None,
              active_flag: bool = False, *args, **kwargs) -> Pipeline:
        """Build a pipeline query out of search search term"""

        regex = self.regex_('fields.value', f'{search_term}', 'ims')
        pipe_and = self.and_([regex, {'active': {"$eq": True}} if active_flag else {}])
        pipe_match = self.match_(pipe_and)

        # permission builds
        if user and permission:
            self.pipeline = [*self.pipeline, *(AccessControlQueryBuilder().build(group_id=user.group_id,
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


class SearchPipelineBuilder(PipelineBuilder):

    def __init__(self, pipeline: Pipeline = None):
        """Init constructor
        Args:
            pipeline: preset a for defined pipeline
        """
        super(SearchPipelineBuilder, self).__init__(pipeline=pipeline)

    def get_regex_pipes_values(self) -> List[str]:
        """Extract the regex pipes value from the pipeline"""
        regex_pipes: List[str] = []

        def gen_dict_extract(key, var) -> str:
            for k, v in var.items():
                if k == key:
                    yield v
                if isinstance(v, dict):
                    for result in gen_dict_extract(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in gen_dict_extract(key, d):
                            yield result

        for pipe in self.pipeline:
            pipe_extract = []
            extract_generator = gen_dict_extract('$regex', pipe)
            while True:
                try:
                    pipe_extract.append(next(extract_generator))
                except StopIteration:
                    break
                except Exception:
                    continue

            if len(pipe_extract) > 0:
                for px in pipe_extract:
                    regex_pipes.append(px)

        return regex_pipes

    def build_resolve_reference_pipeline(self, query: Query, active: bool = False,
                                         user: UserModel = None, permission: AccessControlPermission = None,
                                         *args, **kwargs):
        """Build a resolve reference pipeline query"""
        __pipeline = Pipeline([])
        if isinstance(query, dict):
            __pipeline.append(filter)
        elif isinstance(query, list):
            __pipeline += query

        # get only active objects
        if active:
            __pipeline = [*__pipeline, *[{'$match': {'active': {"$eq": True}}}]]

        # permission builds
        if user and permission:
            __pipeline = [*__pipeline, *(AccessControlQueryBuilder().build(group_id=user.group_id,
                                                                           permission=permission))]
        return __pipeline

    def build(self, params: List[SearchParam],
              obj_manager: CmdbObjectManager = None,
              user: UserModel = None, permission: AccessControlPermission = None,
              active_flag: bool = False, *args, **kwargs) -> Pipeline:
        """Build a pipeline query out of frontend params"""
        # clear pipeline
        self.clear()

        # fetch only active objects
        if active_flag:
            self.add_pipe(self.match_({'active': {"$eq": True}}))

        # text builds
        text_params = [_ for _ in params if _.search_form == 'text' or _.search_form == 'regex']
        for param in text_params:
            regex = self.regex_('fields.value', param.search_text, 'ims')
            self.add_pipe(self.match_(regex))

        # type builds
        disjunction_query = []
        type_params = [_ for _ in params if _.search_form == 'type']
        for param in type_params:
            if param.settings and len(param.settings.get('types', [])) > 0:
                type_id_in = self.in_('type_id', param.settings['types'])
                if param.disjunction:
                    disjunction_query.append(type_id_in)
                else:
                    self.add_pipe(self.match_(type_id_in))
        if len(disjunction_query) > 0:
            self.add_pipe(self.match_(self.or_(disjunction_query)))

        # category builds
        category_params = [_ for _ in params if _.search_form == 'category']
        for param in category_params:
            if param.settings and len(param.settings.get('categories', [])) > 0:
                categories = obj_manager.get_categories_by(**self.regex_('label', param.search_text))
                for curr_category in categories:
                    type_id_in = self.in_('type_id', curr_category.types)
                    self.add_pipe(self.match_(type_id_in))

        # public builds
        id_params = [_ for _ in params if _.search_form == 'publicID']
        for param in id_params:
            self.add_pipe(self.match_({'public_id': int(param.search_text)}))

        # permission builds
        if user and permission:
            self.pipeline = [*self.pipeline, *(AccessControlQueryBuilder().build(group_id=user.group_id,
                                                                                 permission=permission))]
        return self.pipeline


class SearcherFramework(Search[CmdbObjectManager]):
    """Framework searcher implementation for object search"""

    def __init__(self, manager: CmdbObjectManager):
        """Normally uses a instance of CmdbObjectManager as managers"""
        super(SearcherFramework, self).__init__(manager=manager)

    def aggregate(self, pipeline: Pipeline, request_user: UserModel = None, permission: AccessControlPermission = None,
                  limit: int = Search.DEFAULT_LIMIT,
                  skip: int = Search.DEFAULT_SKIP, **kwargs) -> SearchResult[RenderResult]:
        """
        Use mongodb aggregation system with pipeline queries
        Args:
            pipeline (Pipeline): list of requirement pipes
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

        # build resolve reference pipeline
        # plb.build_resolve_reference_pipeline(pipeline=pipeline, user=request_user, permission=permission, **kwargs)

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
            rendered_result_list = RenderList(pre_rendered_result_list, request_user, database_manager=self.manager.dbm,
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

    def search(self, query: Query, request_user: UserModel = None, limit: int = Search.DEFAULT_LIMIT,
               skip: int = Search.DEFAULT_SKIP) -> SearchResult[RenderResult]:
        """
        Uses mongodb find query system
        """
        raise NotImplementedError()
