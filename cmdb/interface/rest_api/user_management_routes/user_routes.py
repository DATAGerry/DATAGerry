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

from flask import abort, request, current_app

from cmdb.framework.utils import PublicID
from cmdb.manager.errors import ManagerGetError, ManagerInsertError, ManagerUpdateError, ManagerDeleteError
from cmdb.framework.managers.error.framework_errors import FrameworkIterationError
from cmdb.framework.results import IterationResult
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetMultiResponse, GetSingleResponse, InsertSingleResponse, UpdateSingleResponse, \
    DeleteSingleResponse
from cmdb.user_management import UserModel
from cmdb.user_management.managers.user_manager import UserManager

users_blueprint = APIBlueprint('users', __name__)


@users_blueprint.route('/', methods=['GET', 'HEAD'])
@users_blueprint.protect(auth=False, right='base.user-management.user.*')
@users_blueprint.parse_collection_parameters()
def get_users(params: CollectionParameters):
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)
    body = request.method == 'HEAD'

    try:
        iteration_result: IterationResult[UserModel] = user_manager.iterate(
            filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
        users = [UserModel.to_dict(user) for user in iteration_result.results]
        api_response = GetMultiResponse(users, total=iteration_result.total, params=params,
                                        url=request.url, model=UserModel.MODEL, body=body)
    except FrameworkIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


@users_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@users_blueprint.protect(auth=False, right='base.user-management.user.view')
def get_user(public_id: int):
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)
    body = request.method == 'HEAD'

    try:
        user: UserModel = user_manager.get(public_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    api_response = GetSingleResponse(UserModel.to_dict(user), url=request.url,
                                     model=UserModel.MODEL, body=body)
    return api_response.make_response()


@users_blueprint.route('/', methods=['POST'])
@users_blueprint.protect(auth=False, right='base.user-management.user.add')
@users_blueprint.validate(UserModel.SCHEMA)
def insert_user(data: dict):
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)
    try:
        result_id: PublicID = user_manager.insert(data)
        raw_doc = user_manager.get(public_id=result_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerInsertError as err:
        return abort(400, err.message)
    api_response = InsertSingleResponse(result_id, raw=UserModel.to_dict(raw_doc), url=request.url,
                                        model=UserModel.MODEL)
    return api_response.make_response(prefix='users')


@users_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@users_blueprint.protect(auth=False, right='base.user-management.user.edit')
@users_blueprint.validate(UserModel.SCHEMA)
def update_user(public_id: int, data: dict):
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)
    try:
        user = UserModel.from_data(data=data)
        user_manager.update(public_id=PublicID(public_id), user=user)
        api_response = UpdateSingleResponse(result=data, url=request.url, model=UserModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerUpdateError as err:
        return abort(400, err.message)
    return api_response.make_response()


@users_blueprint.route('/<int:public_id>', methods=['DELETE'])
@users_blueprint.protect(auth=False, right='base.user-management.user.delete')
def delete_user(public_id: int):
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)
    try:
        deleted_group = user_manager.delete(public_id=PublicID(public_id))
        api_response = DeleteSingleResponse(raw=UserModel.to_dict(deleted_group), model=UserModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerDeleteError as err:
        return abort(404, err.message)
    return api_response.make_response()
