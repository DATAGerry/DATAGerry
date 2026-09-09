# DataGerry - OpenSource Enterprise CMDB
# Copyright (C) 2026 becon GmbH
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
"""
Implementation of all API routes for Search requests
"""
import json
from logging import Logger, getLogger
from flask import request, abort
from werkzeug import Response
from werkzeug.exceptions import HTTPException

from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager.query_builder import QuickSearchPipelineBuilder, SearchPipelineBuilder
from cmdb.manager import ObjectsManager

from cmdb.framework.search.search_param import SearchParam

from cmdb.errors.framework_search import SearchParamError
from cmdb.framework.search.searcher_framework import SearcherFramework
from cmdb.models.user_model import CmdbUser
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.routes.routes_helper import fetch_only_active_objects
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses import DefaultResponse
from cmdb.security.acl.permission import AccessControlPermission

from cmdb.errors.manager.objects_manager import ObjectsManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER: Logger = getLogger(__name__)

search_blueprint = APIBlueprint('search_rest', __name__, url_prefix='/search')

# -------------------------------------------------------------------------------------------------------------------- #

@search_blueprint.route('/quick/count/', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@search_blueprint.protect(auth=True)
def quick_search_result_counter(request_user: CmdbUser) -> Response:
    """
    Aggregates and returns quick search result counts (active, inactive, total) for the given user

    Args:
        request_user (CmdbUser): The user making the request. Used for permission and access control

    Returns:
        Response: A Response containing the quick search result counts
    """
    try:
        objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS, request_user)

        search_term = request.args.get('searchValue', SearcherFramework.DEFAULT_REGEX, str)
        builder = QuickSearchPipelineBuilder()
        only_active = fetch_only_active_objects()
        pipeline: list[dict] = builder.build(search_term=search_term,
                                        user=request_user,
                                        permission=AccessControlPermission.READ,
                                        active_flag=only_active)

        try:
            result = list(objects_manager.aggregate_objects(pipeline=pipeline))
        except ObjectsManagerIterationError as err:
            LOGGER.error('[quick_search_result_counter] ObjectsManagerIterationError: %s',err, exc_info=True)
            abort(400, "Failed to aggregate Objects for quick search result")

        if len(result) > 0:
            return DefaultResponse(result[0]).make_response()

        return DefaultResponse({'active': 0, 'inactive': 0, 'total': 0}).make_response()
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        LOGGER.error("[quick_search_result_counter] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while processing quick search results!")


@search_blueprint.route('/', methods=['GET', 'POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def search_framework(request_user: CmdbUser) -> Response:
    """
    Processes a search request (GET or POST) using the SearcherFramework

    The criteria are built with the request user and READ permission, so the pipeline the searcher
    runs is ACL-filtered before it reaches the database. `?limit=` 0 means every match (the pager
    convention of this API), `?skip=` pages through them and `?resolve=true` renders referenced
    CmdbObjects instead of their ids

    A failure is reported as a failure: until 2026-09-09 every error in the search block answered
    **204 with an empty body**, which a client cannot tell apart from "nothing matched" - and which
    turned an unusable `?limit=0` into a silently empty page

    Args:
        request_user (CmdbUser): The user making the request, used for permission checks and data access

    Raises:
        HTTPException: 400 when the parameters or the search itself are unusable, 405 for an
                       unsupported method, 500 on an unexpected error

    Returns:
        Response: A Response object carrying the rendered page, the total and the per-type groups
    """
    try:
        objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS, request_user)

        try:
            limit = request.args.get('limit', SearcherFramework.DEFAULT_LIMIT, int)
            skip = request.args.get('skip', 0, int)
            only_active = fetch_only_active_objects()
            search_params: dict = request.args.get('query') or '{}'
            resolve_object_references: bool = request.args.get('resolve', 'false') in ['True', 'true']
        except ValueError:
            abort(400, "Could not retrieve the parameters from the request!")

        # 0 is 'every match' here as in every paginated route; a negative page size or offset is not a
        # weaker version of that but an unusable request, and MongoDB would refuse the stage anyway
        if limit < 0 or skip < 0:
            abort(400, "The 'limit' and 'skip' parameters of a search must not be negative!")

        try:
            search_parameters: dict | list = {}

            if request.method == 'GET':
                search_parameters = json.loads(search_params)
            elif request.method == 'POST':
                search_params = json.loads(request.data)
                # LOGGER.debug(f"POST search_params: {search_params}")
                search_parameters = SearchParam.from_request(search_params)
                # LOGGER.debug(f"POST search_parameters: {search_parameters}")
            else:
                abort(405, f"Method: {request.method} not allowed!")
        except SearchParamError as err:
            # The parameter list itself is unusable, and the message names which entry: a search that
            # dropped the bad one would answer 200 with more objects than the filter allows
            LOGGER.error("[search_framework] SearchParamError: %s", err)
            abort(400, str(err))
        except Exception as err:
            LOGGER.error("[search_framework] Exception: %s. Type: %s", err, type(err), exc_info=True)
            abort(400, "An unexpected error occured while processing the search request!")

        searcher = SearcherFramework(objects_manager)
        builder = SearchPipelineBuilder()

        query: list[dict] = builder.build(search_parameters,
                                          user=request_user,
                                          permission=AccessControlPermission.READ,
                                          active_flag=only_active)

        result = searcher.aggregate(
            pipeline=query,
            request_user=request_user,
            limit=limit,
            skip=skip,
            resolve=resolve_object_references,
        )

        return DefaultResponse(result).make_response()
    except HTTPException as http_err:
        raise http_err
    except ObjectsManagerIterationError as err:
        LOGGER.error("[search_framework] ObjectsManagerIterationError: %s", err, exc_info=True)
        abort(400, "Failed to aggregate the Objects for the search request!")
    except Exception as err:
        LOGGER.error("[search_framework] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while processing the search request!")
