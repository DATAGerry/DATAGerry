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

from datetime import datetime
from flask import abort, request, current_app

from cmdb.framework.utils import PublicID
from cmdb.manager.errors import ManagerGetError, ManagerInsertError, ManagerUpdateError, ManagerDeleteError, \
    ManagerIterationError
from cmdb.framework.results import IterationResult
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetMultiResponse, GetSingleResponse, InsertSingleResponse, UpdateSingleResponse, \
    DeleteSingleResponse
from cmdb.security.security import SecurityManager
from cmdb.user_management import UserModel
from cmdb.user_management.managers.user_manager import UserManager

users_blueprint = APIBlueprint('users', __name__)


@users_blueprint.route('/', methods=['GET', 'HEAD'])
@users_blueprint.protect(auth=True, right='base.user-management.user.view')
@users_blueprint.parse_collection_parameters()
def get_users(params: CollectionParameters):
    """
    HTTP `GET`/`HEAD` route for getting a iterable collection of resources.

    Args:
        params (CollectionParameters): Passed parameters over the http query string

    Returns:
        GetMultiResponse: Which includes a IterationResult of the UserModel.

    Notes:
        Calling the route over HTTP HEAD method will result in an empty body.

    Raises:
        ManagerIterationError: If the collection could not be iterated.
        ManagerGetError: If the collection/resources could not be found.
    """
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)

    try:
        iteration_result: IterationResult[UserModel] = user_manager.iterate(
            filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
        users = [UserModel.to_dict(user) for user in iteration_result.results]
        api_response = GetMultiResponse(users, total=iteration_result.total, params=params,
                                        url=request.url, model=UserModel.MODEL, body=request.method == 'HEAD')
    except ManagerIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


@users_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@users_blueprint.protect(auth=True, right='base.user-management.user.view', excepted={'public_id': 'public_id'})
def get_user(public_id: int):
    """
    HTTP `GET`/`HEAD` route for a single user resource.

    Args:
        public_id (int): Public ID user.

    Raises:
        ManagerGetError: When the selected user does not exists.

    Notes:
        Calling the route over HTTP HEAD method will result in an empty body.

    Returns:
        GetSingleResponse: Which includes the json data of a UserModel.
    """
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)

    try:
        user: UserModel = user_manager.get(public_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    api_response = GetSingleResponse(UserModel.to_dict(user), url=request.url,
                                     model=UserModel.MODEL, body=request.method == 'HEAD')
    return api_response.make_response()


@users_blueprint.route('/', methods=['POST'])
@users_blueprint.protect(auth=True, right='base.user-management.user.add')
@users_blueprint.validate(UserModel.SCHEMA)
def insert_user(data: dict):
    """
    HTTP `POST` route for insert a single user resource.

    Args:
        data (UserModel.SCHEMA): Insert data of a new user.

    Raises:
        ManagerGetError: If the inserted user could not be found after inserting.
        ManagerInsertError: If something went wrong during insertion.

    Returns:
        InsertSingleResponse: Insert response with the new user and its public_id.
    """
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)
    security_manager: SecurityManager = SecurityManager(database_manager=current_app.database_manager)
    try:
        data['password'] = security_manager.generate_hmac(data['password'])
        data['registration_time'] = datetime.now()
        result_id: PublicID = user_manager.insert(data)
        user = user_manager.get(public_id=result_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerInsertError as err:
        return abort(400, err.message)
    api_response = InsertSingleResponse(result_id=result_id, raw=UserModel.to_dict(user), url=request.url,
                                        model=UserModel.MODEL)
    return api_response.make_response(prefix='users')


@users_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@users_blueprint.protect(auth=True, right='base.user-management.user.edit', excepted={'public_id': 'public_id'})
@users_blueprint.validate(UserModel.SCHEMA)
def update_user(public_id: int, data: dict):
    """
    HTTP `PUT`/`PATCH` route for update a single user resource.

    Args:
        public_id (int): Public ID of the updatable user.
        data (UserModel.SCHEMA): New user data to update.

    Raises:
        ManagerGetError: When the user with the `public_id` was not found.
        ManagerUpdateError: When something went wrong during the update.

    Returns:
        UpdateSingleResponse: With update result of the new updated user.
    """
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)
    try:
        user = UserModel.from_data(data=data)
        user_manager.update(public_id=PublicID(public_id), user=user)
        api_response = UpdateSingleResponse(result=UserModel.to_dict(user), url=request.url, model=UserModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerUpdateError as err:
        return abort(400, err.message)
    return api_response.make_response()


@users_blueprint.route('/<int:public_id>', methods=['DELETE'])
@users_blueprint.protect(auth=True, right='base.user-management.user.delete')
def delete_user(public_id: int):
    """
    HTTP `DELETE` route for delete a single user resource.

    Args:
        public_id (int): Public ID of the user.

    Raises:
        ManagerGetError: When the user with the `public_id` was not found.
        ManagerDeleteError: When something went wrong during the deletion.

    Returns:
        DeleteSingleResponse: Delete result with the deleted user as data.
    """
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)
    try:
        deleted_group = user_manager.delete(public_id=PublicID(public_id))
        api_response = DeleteSingleResponse(raw=UserModel.to_dict(deleted_group), model=UserModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerDeleteError as err:
        return abort(404, err.message)
    return api_response.make_response()


@users_blueprint.route('/<int:public_id>/password', methods=['PATCH'])
@users_blueprint.protect(auth=True, right='base.user-management.user.edit', excepted={'public_id': 'public_id'})
def change_user_password(public_id: int):
    """
    HTTP `PATCH` route for updating a single user password.

    Args:
        public_id (int): Public ID of the user.

    Raises:
        ManagerGetError: When the user with the `public_id` was not found.
        ManagerUpdateError: When something went wrong during the updated.

    Returns:
        UpdateSingleResponse: User with new password
    """
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)
    security_manager: SecurityManager = SecurityManager(database_manager=current_app.database_manager)
    try:
        user = user_manager.get(public_id=public_id)
        password = security_manager.generate_hmac(request.json.get('password'))
        user.password = password
        user_manager.update(public_id=PublicID(public_id), user=user)
        api_response = UpdateSingleResponse(result=UserModel.to_dict(user), url=request.url, model=UserModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerUpdateError as err:
        return abort(400, err.message)

    return api_response.make_response()
