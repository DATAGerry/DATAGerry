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

import logging
from flask import abort, request, current_app

from cmdb.framework.managers import ManagerGetError
from cmdb.framework.managers.error.framework_errors import FrameworkIterationError
from cmdb.framework.results import IterationResult
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetMultiResponse, GetSingleResponse
from cmdb.user_management import UserModel
from cmdb.user_management.managers.user_manager import UserManager

LOGGER = logging.getLogger(__name__)

users_blueprint = APIBlueprint('users', __name__)


@users_blueprint.route('/', methods=['GET', 'HEAD'])
@users_blueprint.protect(auth=True, right='base.user-management.user.*')
@users_blueprint.parse_collection_parameters()
def get_users(params: CollectionParameters):
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)
    body = True if not request.method != 'HEAD' else False

    try:
        iteration_result: IterationResult[UserModel] = user_manager.iterate(
            filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
        users = [UserModel.to_json(user) for user in iteration_result.results]
        api_response = GetMultiResponse(users, total=iteration_result.total, params=params,
                                        url=request.url, model=UserModel.MODEL, body=body)
    except FrameworkIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


@users_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@users_blueprint.protect(auth=True, right='base.user-management.user.view')
def get_user(public_id: int):
    user_manager: UserManager = UserManager(database_manager=current_app.database_manager)
    body = True if not request.method != 'HEAD' else False

    try:
        user: UserModel = user_manager.get(public_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    api_response = GetSingleResponse(UserModel.to_json(user), url=request.url,
                                     model=UserModel.MODEL, body=body)
    return api_response.make_response()
