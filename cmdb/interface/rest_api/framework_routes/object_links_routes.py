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
"""
Definition of all routes for object links
"""
import logging
from flask import abort, request, current_app

from cmdb.interface.route_utils import insert_request_user

from cmdb.framework.managers.object_link_manager import ObjectLinkManager

from cmdb.framework.models.link import ObjectLinkModel
from cmdb.framework.results import IterationResult
from cmdb.framework.utils import PublicID
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import GetSingleResponse, DeleteSingleResponse, InsertSingleResponse, GetMultiResponse
from cmdb.interface.blueprint import APIBlueprint
from cmdb.errors.manager import ManagerGetError, ManagerDeleteError, ManagerInsertError, ManagerIterationError
from cmdb.security.acl.errors import AccessDeniedError
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel
# -------------------------------------------------------------------------------------------------------------------- #

links_blueprint = APIBlueprint('links', __name__)

LOGGER = logging.getLogger(__name__)

link_manager = ObjectLinkManager(database_manager=current_app.database_manager)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@links_blueprint.route('/', methods=['POST'])
@links_blueprint.protect(auth=True, right='base.framework.object.add')
@insert_request_user
def insert_link(request_user: UserModel):
    """
    Creates a new object link in the database

    Args:
        request_user (UserModel): User requesting this operation

    Returns:
        InsertSingleResponse: Object containing the created public_id of the new object link
    """
    data = request.json

    try:
        result_id = link_manager.insert(data, user=request_user, permission=AccessControlPermission.CREATE)
        raw_doc = link_manager.get(public_id=result_id)
    except (ManagerGetError, ManagerInsertError) as err:
        return abort(400, err)
    except AccessDeniedError as err:
        return abort(403, err.message)

    api_response = InsertSingleResponse(result_id=result_id,
                                        raw=ObjectLinkModel.to_json(raw_doc),
                                        url=request.url,
                                        model=ObjectLinkModel.MODEL)

    return api_response.make_response(prefix='objects/links')

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@links_blueprint.route('/', methods=['GET', 'HEAD'])
@links_blueprint.protect(auth=True, right='base.framework.object.view')
@links_blueprint.parse_collection_parameters()
@insert_request_user
def get_links(params: CollectionParameters, request_user: UserModel):
    """
    Retrieves all object links with given parameters

    Args:
        params (CollectionParameters): Filter for the request
        request_user (UserModel): User making the request

    Returns:
        GetMultiResponse: Retrived object links from db
    """
    body = request.method == 'HEAD'

    try:
        iteration_result: IterationResult[ObjectLinkModel] = link_manager.iterate(
                                                                filter=params.filter,
                                                                limit=params.limit,
                                                                skip=params.skip,
                                                                sort=params.sort,
                                                                order=params.order,
                                                                user=request_user,
                                                                permission=AccessControlPermission.READ)

        types = [ObjectLinkModel.to_json(type) for type in iteration_result.results]

        api_response = GetMultiResponse(types,
                                        total=iteration_result.total,
                                        params=params,
                                        url=request.url,
                                        model=ObjectLinkModel.MODEL,
                                        body=body)

    except ManagerIterationError as err:
        return abort(400, err)
    except ManagerGetError as err:
        return abort(404, err)

    return api_response.make_response()


@links_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@links_blueprint.protect(auth=True, right='base.framework.object.view')
@insert_request_user
def get_link(public_id: int, request_user: UserModel):
    """
    Retrieves an object link with the given public_id

    Args:
        public_id (int): public_id of the object link which should be retrieved
        request_user (UserModel): User making the request

    Returns:
        GetMultiResponse: Retrived object links from db
    """
    body = request.method == 'HEAD'

    try:
        link = link_manager.get(public_id=public_id, user=request_user, permission=AccessControlPermission.READ)
    except ManagerGetError as err:
        return abort(404, err)
    except AccessDeniedError as err:
        return abort(403, err.message)

    api_response = GetSingleResponse(ObjectLinkModel.to_json(link),
                                     url=request.url,
                                     model=ObjectLinkModel.MODEL,
                                     body=body)

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@links_blueprint.route('/<int:public_id>', methods=['DELETE'])
@links_blueprint.protect(auth=True, right='base.framework.object.delete')
@insert_request_user
def delete_link(public_id: int, request_user: UserModel):
    """TODO: document"""
    try:
        deleted_type = link_manager.delete(public_id=PublicID(public_id),
                                           user=request_user,
                                           permission=AccessControlPermission.DELETE)

        api_response = DeleteSingleResponse(raw=ObjectLinkModel.to_json(deleted_type), model=ObjectLinkModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err)
    except ManagerDeleteError as err:
        return abort(400, err)
    except AccessDeniedError as err:
        return abort(403, err.message)

    return api_response.make_response()
