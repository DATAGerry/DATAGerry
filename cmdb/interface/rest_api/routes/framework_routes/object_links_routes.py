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
"""Definition of all routes for object links"""
import logging
from flask import abort, request

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.manager.object_links_manager import ObjectLinksManager

from cmdb.models.user_model.user import UserModel
from cmdb.models.object_link_model.link import ObjectLinkModel
from cmdb.framework.results import IterationResult
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import DeleteSingleResponse, InsertSingleResponse, GetMultiResponse

from cmdb.errors.security import AccessDeniedError
from cmdb.errors.manager import ManagerGetError, ManagerDeleteError, ManagerInsertError, ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

links_blueprint = APIBlueprint('links', __name__)

LOGGER = logging.getLogger(__name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@links_blueprint.route('/', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@links_blueprint.protect(auth=True, right='base.framework.object.add')
def create_object_link(request_user: UserModel):
    """
    Creates a new object link in the database

    Args:
        request_user (UserModel): User requesting this operation
    Returns:
        InsertSingleResponse: Object containing the created public_id of the new object link
    """
    object_link_creation_data: dict = request.json

    try:
        primary_id = object_link_creation_data['primary']
        secondary_id = object_link_creation_data['secondary']
    except KeyError:
        return abort(400, "The 'primary' or 'secondary' key does not exist in the request data!")

    object_links_manager: ObjectLinksManager = ManagerProvider.get_manager(ManagerType.OBJECT_LINKS_MANAGER,
                                                                           request_user)

    # Confirm that this exact link does not exist
    object_link_exists = object_links_manager.check_link_exists(object_link_creation_data)

    if object_link_exists:
        return abort(400, f"The link between {primary_id} and {secondary_id} already exists!")

    try:
        result_id = object_links_manager.insert_object_link(object_link_creation_data,
                                                            request_user,
                                                            AccessControlPermission.CREATE)

        raw_doc = object_links_manager.get_link(result_id, request_user, AccessControlPermission.CREATE)
    except ManagerInsertError as err:
        LOGGER.debug("[create_object_link] ManagerInsertError: %s", err.message)
        return abort(400, "Could not create the ObjectLink!")
    except ManagerGetError as err:
        LOGGER.debug("[create_object_link] ManagerGetError: %s", err.message)
        return abort(400, "Could not retrieve the created ObjectLink!")
    except AccessDeniedError as err:
        #TODO: ERROR-FIX
        return abort(403, "No permission to create an ObjectLink!")

    api_response = InsertSingleResponse(ObjectLinkModel.to_json(raw_doc), result_id)

    return api_response.make_response()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@links_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@links_blueprint.protect(auth=True, right='base.framework.object.view')
@links_blueprint.parse_collection_parameters()
def get_links(params: CollectionParameters, request_user: UserModel):
    """
    Retrieves all object links with given parameters

    Args:
        params (CollectionParameters): Filter for the request
        request_user (UserModel): User making the request
    Returns:
        GetMultiResponse: Retrived object links from db
    """
    object_links_manager: ObjectLinksManager = ManagerProvider.get_manager(ManagerType.OBJECT_LINKS_MANAGER,
                                                                           request_user)

    try:
        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))
        iteration_result: IterationResult[ObjectLinkModel] = object_links_manager.iterate(builder_params)

        object_links = [ObjectLinkModel.to_json(object_link) for object_link in iteration_result.results]

        api_response = GetMultiResponse(object_links,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        request.method == 'HEAD')

    except ManagerIterationError:
        #TODO: ERROR-FIX
        return abort(400)
    except ManagerGetError:
        return abort(404, "No object links found!")

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@links_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@links_blueprint.protect(auth=True, right='base.framework.object.delete')
def delete_link(public_id: int, request_user: UserModel):
    """
    Deletes an object link with the given public_id

    Args:
        public_id (int): public_id of the object_link
        request_user (UserModel): User requesting this operation
    Returns:
        DeleteSingleResponse: with the deleted object link
    """
    object_links_manager: ObjectLinksManager = ManagerProvider.get_manager(ManagerType.OBJECT_LINKS_MANAGER,
                                                                           request_user)

    try:
        deleted_link = object_links_manager.delete_object_link(public_id, request_user, AccessControlPermission.DELETE)

        api_response = DeleteSingleResponse(raw=deleted_link)

    except ManagerGetError as err:
        LOGGER.debug("[delete_link] ManagerGetError: %s", err.message)
        return abort(404, "Could not retrieve the ObjectLink which should be deleted!")
    except ManagerDeleteError as err:
        LOGGER.debug("[delete_link] ManagerDeleteError: %s", err.message)
        return abort(400, f"Could not delete the ObjectLink with public_id: {public_id}!")
    except AccessDeniedError as err:
        #TODO: ERROR-FIX
        return abort(403, "No permission to delete an ObjectLink!")

    return api_response.make_response()
