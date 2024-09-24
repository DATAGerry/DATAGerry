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

from cmdb.manager.object_links_manager import ObjectLinksManager

from cmdb.interface.route_utils import insert_request_user
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.framework.models.link import ObjectLinkModel
from cmdb.framework.results import IterationResult
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import DeleteSingleResponse,\
                                    InsertSingleResponse,\
                                    GetMultiResponse,\
                                    ErrorMessage
from cmdb.interface.blueprint import APIBlueprint
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel
from cmdb.manager.manager_provider import ManagerType, ManagerProvider

from cmdb.security.acl.errors import AccessDeniedError

from cmdb.errors.manager import ManagerGetError, ManagerDeleteError, ManagerInsertError, ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

links_blueprint = APIBlueprint('links', __name__)

LOGGER = logging.getLogger(__name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@links_blueprint.route('/', methods=['POST'])
@insert_request_user
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
        return ErrorMessage(400, "The 'primary' or 'secondary' key does not exist in the request data!").response()

    object_links_manager: ObjectLinksManager = ManagerProvider.get_manager(ManagerType.OBJECT_LINKS_MANAGER,
                                                                           request_user)

    # Confirm that this exact link does not exist
    object_link_exists = object_links_manager.check_link_exists(object_link_creation_data)

    if object_link_exists:
        return ErrorMessage(400, f"The link between {primary_id} and {secondary_id} already exists!").response()

    try:
        result_id = object_links_manager.insert_object_link(object_link_creation_data,
                                                            request_user,
                                                            AccessControlPermission.CREATE)

        raw_doc = object_links_manager.get_link(result_id, request_user, AccessControlPermission.CREATE)
    except ManagerInsertError as err:
        LOGGER.debug("[create_object_link] ManagerInsertError: %s", err.message)
        return ErrorMessage(400, "Could not create the ObjectLink!").response()
    except ManagerGetError as err:
        LOGGER.debug("[create_object_link] ManagerGetError: %s", err.message)
        return ErrorMessage(400, "Could not retrieve the created ObjectLink!").response()
    except AccessDeniedError as err:
        return ErrorMessage(403, "No permission to create an ObjectLink!").response()

    api_response = InsertSingleResponse(ObjectLinkModel.to_json(raw_doc),
                                        result_id,
                                        request.url,
                                        ObjectLinkModel.MODEL)

    return api_response.make_response(prefix='objects/links')

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@links_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
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
                                        ObjectLinkModel.MODEL,
                                        request.method == 'HEAD')

    except ManagerIterationError as err:
        return abort(400, err)
    except ManagerGetError:
        return abort(404, "No object links found!")

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@links_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
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

        api_response = DeleteSingleResponse(raw=deleted_link, model=ObjectLinkModel.MODEL)

    except ManagerGetError as err:
        LOGGER.debug("[delete_link] ManagerGetError: %s", err.message)
        return ErrorMessage(404, "Could not retrieve the ObjectLink which should be deleted!").response()
    except ManagerDeleteError as err:
        LOGGER.debug("[delete_link] ManagerDeleteError: %s", err.message)
        return ErrorMessage(400, f"Could not delete the ObjectLink with public_id: {public_id}!").response()
    except AccessDeniedError as err:
        return ErrorMessage(403, "No permission to delete an ObjectLink!").response()

    return api_response.make_response()
