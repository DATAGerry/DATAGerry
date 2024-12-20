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
from flask import request, abort

from cmdb.manager.rights_manager import RightsManager

from cmdb.framework.results import IterationResult
from cmdb.models.right_model.base_right import BaseRight
from cmdb.models.right_model.constants import NAME_TO_LEVEL
from cmdb.models.right_model.all_rights import __all__ as right_tree
from cmdb.interface.route_utils import verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.rest_api.responses import GetMultiResponse, GetSingleResponse

from cmdb.errors.manager import ManagerGetError, ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

rights_blueprint = APIBlueprint('rights', __name__)

# -------------------------------------------------------------------------------------------------------------------- #

@rights_blueprint.route('/', methods=['GET', 'HEAD'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@rights_blueprint.protect(auth=False, right=None)
@rights_blueprint.parse_collection_parameters(sort='name', view='list')
def get_rights(params: CollectionParameters):
    """
    HTTP `GET`/`HEAD` route for getting a iterable collection of resources.

    Args:
        params (CollectionParameters): Passed parameters over the http query string

    Returns:
        GetMultiResponse: Which includes a IterationResult of the BaseRight.

    Notes:
        Calling the route over HTTP HEAD method will result in an empty body.

    Raises:
        ManagerIterationError: If the collection could not be iterated.
        ManagerGetError: If the collection/resources could not be found.
    """
    rights_manager = RightsManager(right_tree)
    body = request.method == 'HEAD'

    try:
        if params.optional['view'] == 'tree':
            api_response = GetMultiResponse(rights_manager.tree_to_json(right_tree),
                                            total=len(right_tree),
                                            params=params,
                                            url=request.url,
                                            body=body)

            return api_response.make_response(pagination=False)

        iteration_result: IterationResult[BaseRight] = rights_manager.iterate_rights(
                                                                            limit=params.limit,
                                                                            skip=params.skip,
                                                                            sort=params.sort,
                                                                            order=params.order)

        rights = [BaseRight.to_dict(type) for type in iteration_result.results]

        api_response = GetMultiResponse(rights,
                                        total=iteration_result.total,
                                        params=params,
                                        url=request.url,
                                        body=request.method == 'HEAD')

        return api_response.make_response()
    except ManagerIterationError:
        #TODO: ERROR-FIX
        return abort(400)
    except ManagerGetError:
        #TODO: ERROR-FIX
        return abort(404)


@rights_blueprint.route('/<string:name>', methods=['GET', 'HEAD'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@rights_blueprint.protect(auth=False, right='None')
def get_right(name: str):
    """
    HTTP `GET`/`HEAD` route for a single right resource.

    Args:
        name (str): Name of the right.

    Raises:
        ManagerGetError: When the selected right does not exists.

    Notes:
        Calling the route over HTTP HEAD method will result in an empty body.

    Returns:
        GetSingleResponse: Which includes the json data of a BaseRight.
    """
    rights_manager: RightsManager = RightsManager(right_tree)

    try:
        right = rights_manager.get_right(name)
    except ManagerGetError:
        #TODO: ERROR-FIX
        return abort(404)

    api_response = GetSingleResponse(BaseRight.to_dict(right), body=request.method == 'HEAD')

    return api_response.make_response()


@rights_blueprint.route('/levels', methods=['GET', 'HEAD'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@rights_blueprint.protect(auth=False, right='None')
def get_levels():
    """
    HTTP `GET`/`HEAD` route for a static collection of levels.

    Returns:
        GetSingleResponse: Which includes a levels as enum.

    Notes:
        Calling the route over HTTP HEAD method will result in an empty body.
    """

    api_response = GetSingleResponse(NAME_TO_LEVEL, body=request.method == 'HEAD')

    return api_response.make_response()
