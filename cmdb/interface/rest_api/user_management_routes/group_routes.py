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

from flask import request, current_app

from cmdb.interface.rest_api.user_management_routes.group_parameters import GroupDeletionParameters
from cmdb.manager.errors import ManagerGetError, ManagerInsertError, ManagerUpdateError, ManagerDeleteError
from cmdb.framework.managers.error.framework_errors import FrameworkIterationError
from cmdb.framework.results import IterationResult
from cmdb.framework.utils import PublicID
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import GetMultiResponse, GetSingleResponse, InsertSingleResponse, UpdateSingleResponse, \
    DeleteSingleResponse
from cmdb.interface.route_utils import abort
from cmdb.interface.blueprint import APIBlueprint
from cmdb.user_management.managers.group_manager import GroupManager
from cmdb.user_management.managers.right_manager import RightManager
from cmdb.user_management.models.group import UserGroupModel
from cmdb.user_management.rights import __all__ as rights

groups_blueprint = APIBlueprint('groups', __name__)


@groups_blueprint.route('/', methods=['GET', 'HEAD'])
@groups_blueprint.protect(auth=False, right='base.user-management.group.*')
@groups_blueprint.parse_collection_parameters()
def get_groups(params: CollectionParameters):
    group_manager: GroupManager = GroupManager(database_manager=current_app.database_manager,
                                               right_manager=RightManager(rights))
    try:
        iteration_result: IterationResult[UserGroupModel] = group_manager.iterate(
            filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
        groups = [UserGroupModel.to_dict(group) for group in iteration_result.results]
        api_response = GetMultiResponse(groups, total=iteration_result.total, params=params,
                                        url=request.url, model=UserGroupModel.MODEL, body=request.method == 'HEAD')
    except FrameworkIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


@groups_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@groups_blueprint.protect(auth=False, right='base.user-management.group.view')
def get_group(public_id: int):
    group_manager: GroupManager = GroupManager(database_manager=current_app.database_manager,
                                               right_manager=RightManager(rights))
    try:
        group = group_manager.get(public_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    api_response = GetSingleResponse(UserGroupModel.to_dict(group), url=request.url, model=UserGroupModel.MODEL,
                                     body=request.method == 'HEAD')
    return api_response.make_response()


@groups_blueprint.route('/', methods=['POST'])
@groups_blueprint.protect(auth=False, right='base.user-management.group.add')
@groups_blueprint.validate(UserGroupModel.SCHEMA)
def insert_group(data: dict):
    group_manager: GroupManager = GroupManager(database_manager=current_app.database_manager,
                                               right_manager=RightManager(rights))
    try:
        result_id: PublicID = group_manager.insert(data)
        raw_doc = group_manager.get(public_id=result_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerInsertError as err:
        return abort(400, err.message)
    api_response = InsertSingleResponse(result_id, raw=UserGroupModel.to_dict(raw_doc), url=request.url,
                                        model=UserGroupModel.MODEL)
    return api_response.make_response(prefix='groups')


@groups_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@groups_blueprint.protect(auth=False, right='base.user-management.group.edit')
@groups_blueprint.validate(UserGroupModel.SCHEMA)
def update_group(public_id: int, data: dict):
    group_manager: GroupManager = GroupManager(database_manager=current_app.database_manager,
                                               right_manager=RightManager(rights))
    try:
        group = UserGroupModel.from_data(data=data)
        group_manager.update(public_id=PublicID(public_id), group=group)
        api_response = UpdateSingleResponse(result=data, url=request.url, model=UserGroupModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerUpdateError as err:
        return abort(400, err.message)
    return api_response.make_response()


@groups_blueprint.route('/<int:public_id>', methods=['DELETE'])
@groups_blueprint.protect(auth=False, right='base.user-management.group.delete')
@groups_blueprint.parse_parameters(GroupDeletionParameters)
def delete_category(public_id: int, params: GroupDeletionParameters):
    group_manager: GroupManager = GroupManager(database_manager=current_app.database_manager,
                                               right_manager=RightManager(rights))
    try:
        deleted_group = group_manager.delete(public_id=PublicID(public_id))
        api_response = DeleteSingleResponse(raw=UserGroupModel.to_dict(deleted_group), model=UserGroupModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerDeleteError as err:
        return abort(404, err.message)
    return api_response.make_response()
