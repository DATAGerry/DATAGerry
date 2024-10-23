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

from cmdb.manager.objects_manager import ObjectsManager
from cmdb.manager.categories_manager import CategoriesManager

from cmdb.cmdb_objects.cmdb_object import CmdbObject
from cmdb.framework.models.type import TypeModel
from cmdb.framework.cmdb_render import RenderResult, RenderList
from cmdb.search.params import SearchParam
from cmdb.search.query.pipe_builder import PipelineBuilder
from cmdb.search.search_result import SearchResult
from cmdb.user_management.models.user import UserModel
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.security.acl.builder import AccessControlQueryBuilder
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              QuickSearchPipelineBuilder                                              #
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
              active_flag: bool = False, *args, **kwargs) -> list[dict]:
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


class SearchReferencesPipelineBuilder(PipelineBuilder):
    """TODO: document"""

    def __init__(self, pipeline: list[dict] = None):
        """
        Init constructor load reference fields in runtime.
        The search should interpret reference section like normal field contents.
        This means that fields should already be loaded into the object during runtime.
        Args:
            pipeline: preset a for defined pipeline
        """
        super().__init__(pipeline=pipeline)


    def build(self, *args, **kwargs) -> list[dict]:
        # Load reference fields in runtime
        self.add_pipe(self.lookup_('framework.objects', 'fields.value', 'public_id', 'data'))
        self.add_pipe(
            self.project_({
                '_id': 1, 'public_id': 1, 'type_id': 1, 'active': 1, 'author_id': 1, 'creation_time': 1, 'version': 1,
                'last_edit_time': 1, 'fields': 1, 'relatesTo': '$data.public_id',
                'simple': {
                    '$reduce': {
                        'input': "$data.fields",
                        'initialValue': [],
                        'in': {'$setUnion': ["$$value", "$$this"]}
                    }
                }
            })
        )
        self.add_pipe(
            self.group_('$_id', {
                'public_id': {'$first': '$public_id'},
                'type_id': {'$first': '$type_id'},
                'active': {'$first': '$active'},
                'author_id': {'$first': '$author_id'},
                'creation_time': {'$first': '$creation_time'},
                'last_edit_time': {'$first': '$last_edit_time'},
                'version': {'$first': 'version'},
                'fields': {'$first': '$fields'},
                'simple': {'$first': '$simple'},
                'relatesTo': {'$first': '$relatesTo'}
            })
        )
        self.add_pipe(
            self.project_({
                '_id': 1, 'public_id': 1, 'type_id': 1, 'active': 1, 'author_id': 1, 'creation_time': 1, 'version': 1,
                'last_edit_time': 1, 'fields': {'$concatArrays': ['$fields', '$simple']}, 'relatesTo': 1,
            })
        )
        self.add_pipe(self.sort_('public_id', 1))
        return self.pipeline


class SearchPipelineBuilder(PipelineBuilder):
    """TODO: document"""

    def __init__(self, pipeline: list[dict] = None):
        """Init constructor
        Args:
            pipeline: preset a for defined pipeline
        """
        super().__init__(pipeline=pipeline)


    def get_regex_pipes_values(self) -> list[str]:
        """Extract the regex pipes value from the pipeline"""
        regex_pipes: list[str] = []

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


    def build(self, params: list[SearchParam],
              objects_manager: ObjectsManager = None,
              user: UserModel = None, permission: AccessControlPermission = None,
              active_flag: bool = False) -> list[dict]:
        """Build a pipeline query out of frontend params"""
        # clear pipeline
        self.clear()
        categories_manager = CategoriesManager(objects_manager.dbm)

        # load reference fields in runtime.
        self.pipeline = SearchReferencesPipelineBuilder().build()

        # fetch only active objects
        if active_flag:
            self.add_pipe(self.match_({'active': {"$eq": True}}))

        # text builds
        text_params = [_ for _ in params if _.search_form in ('text','regex')]
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
                categories = categories_manager.get_categories_by(**self.regex_('label', param.search_text))
                for curr_category in categories:
                    type_id_in = self.in_('type_id', curr_category.types)
                    self.add_pipe(self.match_(type_id_in))

        # public builds
        id_params = [_ for _ in params if _.search_form == 'publicID']
        for param in id_params:
            self.add_pipe(self.match_({'public_id': int(param.search_text)}))

        # permission builds
        if user and permission:
            self.pipeline = [*self.pipeline, *(AccessControlQueryBuilder().build(group_id=int(user.group_id),
                                                                                 permission=permission))]
        return self.pipeline


class SearcherFramework:
    """Framework searcher implementation for object search"""
    DEFAULT_SKIP: int = 0
    DEFAULT_LIMIT: int = 10
    DEFAULT_REGEX: str = ''


    def __init__(self, objects_manager: ObjectsManager):
        self.objects_manager = objects_manager
        super().__init__(objects_manager)


    def aggregate(self, pipeline: list[dict], request_user: UserModel = None, permission: AccessControlPermission = None,
                  limit: int = DEFAULT_LIMIT,
                  skip: int = DEFAULT_SKIP, **kwargs) -> SearchResult[RenderResult]:
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
               skip: int = DEFAULT_SKIP) -> SearchResult[RenderResult]:
        """Uses mongodb find query system"""
        raise NotImplementedError()
