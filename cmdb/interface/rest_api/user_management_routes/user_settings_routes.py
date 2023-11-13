# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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

from flask import current_app, abort, request

from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetListResponse, GetSingleResponse, InsertSingleResponse, DeleteSingleResponse, \
    UpdateSingleResponse
from cmdb.manager import ManagerGetError, ManagerInsertError, ManagerDeleteError, ManagerUpdateError
from cmdb.user_management import UserSettingModel
from cmdb.user_management.managers.setting_manager import UserSettingsManager
# -------------------------------------------------------------------------------------------------------------------- #

user_settings_blueprint = APIBlueprint('user_settings', __name__)


@user_settings_blueprint.route('/', methods=['GET', 'HEAD'])
def get_user_settings(user_id: int):
    """
    HTTP `GET`/`HEAD` route for getting a complete collection of resources.

    Args:
        user_id (int): PublicID of the current user.

    Returns:
        GetListResponse: Which includes all of the `UserSettingModel`.

    Notes:
        Calling the route over HTTP HEAD method will result in an empty body.

    Raises:
        ManagerGetError: If the collection/resources could not be found.
    """
    settings_manager = UserSettingsManager(database_manager=current_app.database_manager)
    try:
        settings: List[UserSettingModel] = settings_manager.get_user_settings(user_id=user_id)
        raw_settings = [UserSettingModel.to_dict(setting) for setting in settings]
        api_response = GetListResponse(results=raw_settings, url=request.url, model=UserSettingModel.MODEL,
                                       body=request.method == 'HEAD')
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()



@user_settings_blueprint.route('/<string:resource>', methods=['GET', 'HEAD'])
def get_user_setting(user_id: int, resource: str):
    """
    HTTP `GET`/`HEAD` route for a single user setting resource.

    Args:
        user_id (int): Public ID of the user.
        resource (str): Identifier/Name of the user setting.

    Raises:
        ManagerGetError: When the selected user setting does not exists.

    Notes:
        Calling the route over HTTP HEAD method will result in an empty body.

    Returns:
        GetSingleResponse: Which includes the json data of a UserSettingModel.
    """
    settings_manager = UserSettingsManager(database_manager=current_app.database_manager)
    try:
        setting: UserSettingModel = settings_manager.get_user_setting(user_id, resource)
        api_response = GetSingleResponse(UserSettingModel.to_dict(setting), url=request.url,
                                         model=UserSettingModel.MODEL, body=request.method == 'HEAD')
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()



@user_settings_blueprint.route('/', methods=['POST'])
@user_settings_blueprint.validate(UserSettingModel.SCHEMA)
def insert_setting(user_id: int, data: dict):
    """
    HTTP `POST` route for insert a single user setting resource.

    Args:
        user_id (int): Public ID of the user.
        data (UserModel.SCHEMA): Insert data of a new user.

    Raises:
        ManagerGetError: If the inserted user could not be found after inserting.
        ManagerInsertError: If something went wrong during insertion.

    Returns:
        InsertSingleResponse: Insert response with the new user and its identifier.
    """
    settings_manager: UserSettingsManager = UserSettingsManager(database_manager=current_app.database_manager)
    try:
        settings_manager.insert(data)
        setting: UserSettingModel = settings_manager.get_user_setting(user_id=user_id,
                                                                      resource=data.get('resource'))
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerInsertError as err:
        return abort(400, err.message)
    api_response = InsertSingleResponse(raw=UserSettingModel.to_dict(setting), result_id=setting.resource,
                                        url=request.url, model=UserSettingModel.MODEL)
    return api_response.make_response(prefix=f'users/{user_id}/settings/{setting.resource}')



@user_settings_blueprint.route('/<string:resource>', methods=['PUT', 'PATCH'])
@user_settings_blueprint.validate(UserSettingModel.SCHEMA)
def update_setting(user_id: int, resource: str, data: dict):
    """
    HTTP `PUT`/`PATCH` route for update a single user setting resource.

    Args:
        user_id (int): Public ID of the user.
        resource (str): Identifier/Name of the user setting.
        data (UserModel.SCHEMA): New setting data to update.

    Raises:
        ManagerGetError: When the setting with the `identifier` was not found.
        ManagerUpdateError: When something went wrong during the update.

    Returns:
        UpdateSingleResponse: With update result of the new updated user setting.
    """
    settings_manager: UserSettingsManager = UserSettingsManager(database_manager=current_app.database_manager)
    try:
        setting = UserSettingModel.from_data(data=data)
        settings_manager.update(user_id=user_id, resource=resource, setting=setting)
        api_response = UpdateSingleResponse(result=data, url=request.url, model=UserSettingModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerUpdateError as err:
        return abort(400, err.message)

    return api_response.make_response()



@user_settings_blueprint.route('/<string:resource>', methods=['DELETE'])
def delete_setting(user_id: int, resource: str):
    """
    HTTP `DELETE` route for delete a single user setting resource.

    Args:
        user_id (int): Public ID of the user.
        resource (str): Identifier/Name of the user setting.

    Raises:
        ManagerGetError: When the setting with the `identifier` was not found.
        ManagerDeleteError: When something went wrong during the deletion.

    Returns:
        DeleteSingleResponse: Delete result with the deleted setting as data.
    """
    settings_manager: UserSettingsManager = UserSettingsManager(database_manager=current_app.database_manager)
    try:
        deleted_setting = settings_manager.delete(user_id=user_id, resource=resource)
        api_response = DeleteSingleResponse(raw=UserSettingModel.to_dict(deleted_setting), model=UserSettingModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerDeleteError as err:
        return abort(404, err.message)
    return api_response.make_response()
