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
from cmdb.manager.objects_manager import ObjectsManager
from cmdb.manager.categories_manager import CategoriesManager

from cmdb.models.user_model.user import UserModel
from cmdb.framework.search.search_param import SearchParam
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.security.acl.builder import AccessControlQueryBuilder
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                             SearchPipelineBuilder - CLASS                                            #
# -------------------------------------------------------------------------------------------------------------------- #
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

        def gen_dict_extract(key, var):
            for k, v in var.items():
                if k == key:
                    yield v
                if isinstance(v, dict):
                    yield from gen_dict_extract(key, v)
                elif isinstance(v, list):
                    for d in v:
                        if isinstance(d, dict):
                            yield from gen_dict_extract(key, d)

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