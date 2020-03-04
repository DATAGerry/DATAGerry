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
import json
import logging

from flask import current_app, request, abort

from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.interface.route_utils import RootBlueprint, make_response, insert_request_user, login_required
from cmdb.search import Search
from cmdb.search.params import SearchParam
from cmdb.search.query import Query, Pipeline
from cmdb.search.query.pipe_builder import PipelineBuilder
from cmdb.search.query.query_builder import QueryBuilder
from cmdb.search.searchers import SearcherFramework
from cmdb.user_management.user import User

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

with current_app.app_context():
    object_manager: CmdbObjectManager = current_app.object_manager

LOGGER = logging.getLogger(__name__)
search_blueprint = RootBlueprint('search_rest', __name__, url_prefix='/search')


@search_blueprint.route('/quick/count/<string:regex>', methods=['GET'])
@login_required
@insert_request_user
def quick_search_result_counter(regex: str, request_user: User):
    plb = PipelineBuilder()
    regex = plb.regex_('fields.value', f'{regex}', 'ims')
    pipe_match = plb.match_(regex)
    plb.add_pipe(pipe_match)
    pipe_count = plb.count_('count')
    plb.add_pipe(pipe_count)
    pipeline = plb.pipeline
    try:
        result = list(object_manager.aggregate(collection='framework.objects', pipeline=pipeline))
    except Exception as err:
        LOGGER.error(f'[Search count]: {err}')
        return abort(400)
    if len(result) > 0:
        return make_response(result[0]['count'])
    else:
        return make_response(0)


@search_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@insert_request_user
def search_framework(request_user: User):
    try:
        limit = request.args.get('limit', Search.DEFAULT_LIMIT, int)
        skip = request.args.get('skip', Search.DEFAULT_SKIP, int)
        only_active = _fetch_only_active_objs()
        search_params: dict = request.args.get('query') or '{}'
    except ValueError as err:
        return abort(400, err)
    try:
        if request.method == 'GET':
            search_params = json.loads(search_params)
        elif request.method == 'POST':
            search_params = json.loads(request.data)
        else:
            return abort(405)
    except Exception as err:
        LOGGER.error(f'[Search Framework]: {err}')
        return abort(400, err)

    try:
        builder = PipelineBuilder()
        search_parameters = SearchParam.from_request(search_params)
        query: Pipeline = builder.build(search_parameters, object_manager, only_active)

        searcher = SearcherFramework(manager=object_manager)
        result = searcher.aggregate(pipeline=query, request_user=request_user, limit=limit, skip=skip)
        LOGGER.debug(result.__dict__)
    except Exception as err:
        LOGGER.error(f'[Search Framework Rest]: {err}')
        return make_response([], 204)

    return make_response(result)


def _fetch_only_active_objs():
    """
        Checking if request have cookie parameter for object active state
        Returns:
            True if cookie is set or value is true else false
        """
    if request.args.get('onlyActiveObjCookie') is not None:
        value = request.args.get('onlyActiveObjCookie')
        if value in ['True', 'true']:
            return True
    return False
