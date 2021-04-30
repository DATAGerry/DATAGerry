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

import json
import logging

from flask import current_app, request, abort

from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.interface.route_utils import make_response, insert_request_user, login_required
from cmdb.search import Search
from cmdb.search.params import SearchParam
from cmdb.search.query import Pipeline
from cmdb.search.searchers import SearcherFramework, SearchPipelineBuilder, QuickSearchPipelineBuilder
from cmdb.user_management.models.user import UserModel
from cmdb.interface.blueprint import APIBlueprint
from cmdb.security.acl.permission import AccessControlPermission

with current_app.app_context():
    object_manager: CmdbObjectManager = CmdbObjectManager(current_app.database_manager, current_app.event_queue)

LOGGER = logging.getLogger(__name__)
search_blueprint = APIBlueprint('search_rest', __name__, url_prefix='/search')


@search_blueprint.route('/quick/count', methods=['GET'])
@search_blueprint.route('/quick/count/', methods=['GET'])
@search_blueprint.protect(auth=True)
@insert_request_user
def quick_search_result_counter(request_user: UserModel):
    search_term = request.args.get('searchValue', Search.DEFAULT_REGEX, str)
    builder = QuickSearchPipelineBuilder()
    only_active = _fetch_only_active_objs()
    pipeline: Pipeline = builder.build(search_term=search_term, user=request_user,
                                       permission=AccessControlPermission.READ,
                                       active_flag=only_active)
    try:
        result = list(object_manager.aggregate(collection='framework.objects', pipeline=pipeline))
    except Exception as err:
        LOGGER.error(f'[Search count]: {err}')
        return abort(400)
    if len(result) > 0:
        return make_response(result[0])
    else:
        return make_response({'active': 0, 'inactive': 0, 'total': 0})


@search_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@insert_request_user
def search_framework(request_user: UserModel):
    try:
        limit = request.args.get('limit', Search.DEFAULT_LIMIT, int)
        skip = request.args.get('skip', Search.DEFAULT_SKIP, int)
        only_active = _fetch_only_active_objs()
        search_params: dict = request.args.get('query') or '{}'
        resolve_object_references: bool = request.args.get('resolve', False)
    except ValueError as err:
        return abort(400, err)
    try:
        if request.method == 'GET':
            search_parameters = json.loads(search_params)
        elif request.method == 'POST':
            search_params = json.loads(request.data)
            search_parameters = SearchParam.from_request(search_params)
        else:
            return abort(405)
    except Exception as err:
        LOGGER.error(f'[Search Framework]: {err}')
        return abort(400, err)
    try:
        searcher = SearcherFramework(manager=object_manager)
        builder = SearchPipelineBuilder()

        query: Pipeline = builder.build(search_parameters, object_manager,
                                        user=request_user,
                                        permission=AccessControlPermission.READ, active_flag=only_active)

        result = searcher.aggregate(pipeline=query, request_user=request_user, limit=limit, skip=skip,
                                    resolve=resolve_object_references, permission=AccessControlPermission.READ,
                                    active=only_active)

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
