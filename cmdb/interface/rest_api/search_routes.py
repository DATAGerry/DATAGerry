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
import json
import logging
from flask import request, abort

from cmdb.manager.objects_manager import ObjectsManager

from cmdb.interface.route_utils import make_response, insert_request_user, login_required
from cmdb.search.params import SearchParam
from cmdb.search.searchers import SearcherFramework, SearchPipelineBuilder, QuickSearchPipelineBuilder
from cmdb.user_management.models.user import UserModel
from cmdb.interface.blueprint import APIBlueprint
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.manager.manager_provider import ManagerType, ManagerProvider
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

search_blueprint = APIBlueprint('search_rest', __name__, url_prefix='/search')

# -------------------------------------------------------------------------------------------------------------------- #

@search_blueprint.route('/quick/count', methods=['GET'])
@search_blueprint.route('/quick/count/', methods=['GET'])
@search_blueprint.protect(auth=True)
@insert_request_user
def quick_search_result_counter(request_user: UserModel):
    """TODO: document"""
    objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

    search_term = request.args.get('searchValue', SearcherFramework.DEFAULT_REGEX, str)
    builder = QuickSearchPipelineBuilder()
    only_active = _fetch_only_active_objs()
    pipeline: list[dict] = builder.build(search_term=search_term,
                                       user=request_user,
                                       permission=AccessControlPermission.READ,
                                       active_flag=only_active)

    try:
        result = list(objects_manager.aggregate_objects(pipeline=pipeline))
    except Exception as err:
        LOGGER.error('[Search count]: %s',err)
        return abort(400)

    if len(result) > 0:
        return make_response(result[0])

    return make_response({'active': 0, 'inactive': 0, 'total': 0})


@search_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@insert_request_user
def search_framework(request_user: UserModel):
    """TODO: document"""
    objects_manager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

    try:
        limit = request.args.get('limit', SearcherFramework.DEFAULT_LIMIT, int)
        skip = request.args.get('skip', SearcherFramework.DEFAULT_SKIP, int)
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
        LOGGER.error('[search_framework]: %s', err)
        return abort(400, err)

    try:
        searcher = SearcherFramework(objects_manager)
        builder = SearchPipelineBuilder()

        query: list[dict] = builder.build(search_parameters,
                                        objects_manager,
                                        user=request_user,
                                        permission=AccessControlPermission.READ,
                                        active_flag=only_active)

        result = searcher.aggregate(pipeline=query, request_user=request_user, limit=limit, skip=skip,
                                    resolve=resolve_object_references, permission=AccessControlPermission.READ,
                                    active=only_active)
    except Exception as err:
        LOGGER.error('[search_framework]: %s',err)
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
