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
from typing import List

from flask import request

from cmdb.user_management.managers.group_manager import GroupManager
from cmdb.user_management.managers.right_manager import RightManager
from cmdb.user_management.managers.user_manager import UserManager

from cmdb.interface.rest_api.user_management_routes.group_parameters import GroupDeletionParameters, GroupDeleteMode
from cmdb.errors.manager import ManagerGetError, ManagerInsertError, ManagerUpdateError, ManagerDeleteError
from cmdb.framework.managers.error.framework_errors import FrameworkIterationError
from cmdb.framework.results import IterationResult
from cmdb.framework.utils import PublicID
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import GetMultiResponse, GetSingleResponse, InsertSingleResponse, UpdateSingleResponse, \
    DeleteSingleResponse
from cmdb.interface.route_utils import abort
from cmdb.interface.blueprint import APIBlueprint
from cmdb.search import Query
from cmdb.user_management import UserModel

from cmdb.user_management.models.group import UserGroupModel
from cmdb.user_management.rights import __all__ as rights
from cmdb.interface.route_utils import insert_request_user
from cmdb.manager.manager_provider import ManagerType, ManagerProvider
# -------------------------------------------------------------------------------------------------------------------- #
groups_blueprint = APIBlueprint('groups', __name__)


@groups_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@groups_blueprint.protect(auth=True, right='base.user-management.group.view')
@groups_blueprint.parse_collection_parameters()
def get_groups(params: CollectionParameters, request_user: UserModel):
    """
    HTTP `GET`/`HEAD` route for getting a iterable collection of resources.

    Args:
        params (CollectionParameters): Passed parameters over the http query string

    Returns:
        GetMultiResponse: Which includes a IterationResult of the UserGroupModel.

    Notes:
        Calling the route over HTTP HEAD method will result in an empty body.

    Raises:
        ManagerIterationError: If the collection could not be iterated.
        ManagerGetError: If the collection/resources could not be found.
    """
    group_manager: GroupManager = ManagerProvider.get_manager(ManagerType.GROUP_MANAGER, request_user)

    try:
        iteration_result: IterationResult[UserGroupModel] = group_manager.iterate(
            filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
        groups = [UserGroupModel.to_dict(group) for group in iteration_result.results]

        api_response = GetMultiResponse(groups, total=iteration_result.total, params=params,
                                        url=request.url, model=UserGroupModel.MODEL, body=request.method == 'HEAD')
    except FrameworkIterationError as err:
        return abort(400, err)
    except ManagerGetError as err:
        return abort(404, err)

    return api_response.make_response()


@groups_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@groups_blueprint.protect(auth=True, right='base.user-management.group.view')
def get_group(public_id: int, request_user: UserModel):
    """
    HTTP `GET`/`HEAD` route for a single group resource.

    Args:
        public_id (int): Public ID of the group.

    Raises:
        ManagerGetError: When the selected group does not exists.

    Notes:
        Calling the route over HTTP HEAD method will result in an empty body.

    Returns:
        GetSingleResponse: Which includes the json data of a UserGroupModel.
    """
    group_manager: GroupManager = ManagerProvider.get_manager(ManagerType.GROUP_MANAGER, request_user)

    try:
        group = group_manager.get(public_id)
    except ManagerGetError as err:
        return abort(404, err)
    api_response = GetSingleResponse(UserGroupModel.to_dict(group), url=request.url,
                                     model=UserGroupModel.MODEL, body=request.method == 'HEAD')

    return api_response.make_response()


@groups_blueprint.route('/', methods=['POST'])
@insert_request_user
@groups_blueprint.protect(auth=True, right='base.user-management.group.add')
@groups_blueprint.validate(UserGroupModel.SCHEMA)
def insert_group(data: dict, request_user: UserModel):
    """
    HTTP `POST` route for insert a single group resource.

    Args:
        data (UserGroupModel.SCHEMA): Insert data of a new group.

    Raises:
        ManagerGetError: If the inserted group could not be found after inserting.
        ManagerInsertError: If something went wrong during insertion.

    Returns:
        InsertSingleResponse: Insert response with the new group and its public_id.
    """
    group_manager: GroupManager = ManagerProvider.get_manager(ManagerType.GROUP_MANAGER, request_user)

    try:
        result_id: PublicID = group_manager.insert(data)
        group = group_manager.get(public_id=result_id)
    except ManagerGetError as err:
        return abort(404, err)
    except ManagerInsertError as err:
        return abort(400, err)

    api_response = InsertSingleResponse(result_id=result_id, raw=UserGroupModel.to_dict(group), url=request.url,
                                        model=UserGroupModel.MODEL)

    return api_response.make_response(prefix='groups')


@groups_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@groups_blueprint.protect(auth=True, right='base.user-management.group.edit')
@groups_blueprint.validate(UserGroupModel.SCHEMA)
def update_group(public_id: int, data: dict, request_user: UserModel):
    """
    HTTP `PUT`/`PATCH` route for update a single group resource.

    Args:
        public_id (int): Public ID of the updatable group.
        data (UserGroupModel.SCHEMA): New group data to update.

    Raises:
        ManagerGetError: When the group with the `public_id` was not found.
        ManagerUpdateError: When something went wrong during the update.

    Returns:
        UpdateSingleResponse: With update result of the new updated group.
    """
    group_manager: GroupManager = ManagerProvider.get_manager(ManagerType.GROUP_MANAGER, request_user)

    try:
        group = UserGroupModel.from_data(data=data, rights=RightManager(rights).rights)
        group_dict = UserGroupModel.to_dict(group)
        group_dict['rights'] = [right.get('name') for right in group_dict.get('rights', [])]
        group_manager.update(public_id=PublicID(public_id), group=group_dict)
        api_response = UpdateSingleResponse(result=group_dict, url=request.url,
                                            model=UserGroupModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err)
    except ManagerUpdateError as err:
        return abort(400, err)

    return api_response.make_response()


@groups_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@groups_blueprint.protect(auth=True, right='base.user-management.group.delete')
@groups_blueprint.parse_parameters(GroupDeletionParameters)
def delete_group(public_id: int, params: GroupDeletionParameters, request_user: UserModel):
    """
    HTTP `DELETE` route for delete a single group resource.

    Args:
        public_id (int): Public ID of the user.
        params (GroupDeletionParameters): Optional action parameters for handling users when the group \
                                          is going to be deleted.

    Notes:
        Based on the params attribute. Users can be moved or deleted.

    Raises:
        ManagerGetError: When the group with the `public_id` was not found.
        ManagerDeleteError: When something went wrong during the deletion.

    Returns:
        DeleteSingleResponse: Delete result with the deleted group as data.
    """
    group_manager: GroupManager = ManagerProvider.get_manager(ManagerType.GROUP_MANAGER, request_user)
    user_manager: UserManager = ManagerProvider.get_manager(ManagerType.USER_MANAGER, request_user)

    # Check of action is set
    if params.action:
        users_in_group: List[UserModel] = user_manager.get_many(Query({'group_id': public_id}))

        if len(users_in_group) > 0:
            if params.action == GroupDeleteMode.MOVE.value:
                if params.group_id:
                    for user in users_in_group:
                        user.group_id = int(params.group_id)

                        try:
                            user_manager.update(user.public_id, user)
                        except ManagerUpdateError as err:
                            return abort(400,
                                         f'Could not move user: {user.public_id} to group: {params.group_id} | '
                                         f'Error: {err}')

            if params.action == GroupDeleteMode.DELETE.value:
                for user in users_in_group:
                    try:
                        user_manager.delete(user.public_id)
                    except ManagerDeleteError as err:
                        return abort(400, f'Could not delete user: {user.public_id} | Error: {err}')

    try:
        deleted_group = group_manager.delete(public_id=PublicID(public_id))
        api_response = DeleteSingleResponse(raw=UserGroupModel.to_dict(deleted_group), model=UserGroupModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err)
    except ManagerDeleteError as err:
        return abort(404, err)

    return api_response.make_response()
