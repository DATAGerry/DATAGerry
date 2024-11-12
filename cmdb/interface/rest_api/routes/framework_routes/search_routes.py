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

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.objects_manager import ObjectsManager

from cmdb.search.params import SearchParam
from cmdb.search.searchers import SearcherFramework, SearchPipelineBuilder, QuickSearchPipelineBuilder
from cmdb.models.user_model.user import UserModel
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, login_required
from cmdb.interface.rest_api.responses import DefaultResponse
from cmdb.security.acl.permission import AccessControlPermission
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
        return DefaultResponse(result[0]).make_response()

    return DefaultResponse({'active': 0, 'inactive': 0, 'total': 0}).make_response()


@search_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@insert_request_user
def search_framework(request_user: UserModel):
    """TODO: document"""
    objects_manager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

    try:
        limit = request.args.get('limit', SearcherFramework.DEFAULT_LIMIT, int)
        skip = request.args.get('skip', 0, int)
        only_active = _fetch_only_active_objs()
        search_params: dict = request.args.get('query') or '{}'
        resolve_object_references: bool = request.args.get('resolve', False)
    except ValueError:
        return abort(400, "Could not retrieve the parameters from the request!")

    try:
        if request.method == 'GET':
            search_parameters = json.loads(search_params)
        elif request.method == 'POST':
            search_params = json.loads(request.data)
            search_parameters = SearchParam.from_request(search_params)
        else:
            return abort(405, f"Method: {request.method} not allowed!")
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
                                    resolve=resolve_object_references, active=only_active)
    except Exception as err:
        LOGGER.error("[search_framework]: Exception: %s, Type: %s",err, type(err))
        return DefaultResponse([]).make_response(204)

    api_response = DefaultResponse(result)

    return api_response.make_response()


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
