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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from typing import List

from flask import current_app, abort, request

from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetListResponse, GetSingleResponse, InsertSingleResponse, DeleteSingleResponse, \
    UpdateSingleResponse
from cmdb.manager import ManagerGetError, ManagerInsertError, ManagerDeleteError, ManagerUpdateError
from cmdb.user_management import UserSettingModel
from cmdb.user_management.managers.setting_manager import UserSettingsManager

user_settings_blueprint = APIBlueprint('user_settings', __name__)


@user_settings_blueprint.route('/', methods=['GET', 'HEAD'])
def get_user_settings(user_id: int):
    settings_manager = UserSettingsManager(database_manager=current_app.database_manager)
    try:
        settings: List[UserSettingModel] = settings_manager.get_user_settings(user_id=user_id)
        raw_settings = [UserSettingModel.to_dict(setting) for setting in settings]
        api_response = GetListResponse(results=raw_settings, url=request.url, model=UserSettingModel.MODEL,
                                       body=request.method == 'HEAD')
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


@user_settings_blueprint.route('/<string:identifier>', methods=['GET', 'HEAD'])
def get_user_setting(user_id: int, identifier: str):
    settings_manager = UserSettingsManager(database_manager=current_app.database_manager)
    try:
        setting: UserSettingModel = settings_manager.get_user_setting(user_id, identifier)
        api_response = GetSingleResponse(UserSettingModel.to_dict(setting), url=request.url,
                                         model=UserSettingModel.MODEL, body=request.method == 'HEAD')
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


@user_settings_blueprint.route('/', methods=['POST'])
@user_settings_blueprint.validate(UserSettingModel.SCHEMA)
def insert_setting(user_id: int, data: dict):
    settings_manager: UserSettingsManager = UserSettingsManager(database_manager=current_app.database_manager)
    try:
        settings_manager.insert(data)
        setting: UserSettingModel = settings_manager.get_user_setting(user_id=user_id,
                                                                      identifier=data.get('identifier'))
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerInsertError as err:
        return abort(400, err.message)
    api_response = InsertSingleResponse(raw=UserSettingModel.to_dict(setting), result_id=setting.identifier,
                                        url=request.url, model=UserSettingModel.MODEL)
    return api_response.make_response(prefix=f'users/{user_id}/settings/{setting.identifier}')


@user_settings_blueprint.route('/<string:identifier>', methods=['PUT', 'PATCH'])
@user_settings_blueprint.validate(UserSettingModel.SCHEMA)
def update_setting(user_id: int, identifier: str, data: dict):
    settings_manager: UserSettingsManager = UserSettingsManager(database_manager=current_app.database_manager)
    try:
        setting = UserSettingModel.from_data(data=data)
        settings_manager.update(user_id=user_id, identifier=identifier, setting=setting)
        api_response = UpdateSingleResponse(result=data, url=request.url, model=UserSettingModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerUpdateError as err:
        return abort(400, err.message)

    return api_response.make_response()


@user_settings_blueprint.route('/<string:identifier>', methods=['DELETE'])
def delete_setting(user_id: int, identifier: str):
    settings_manager: UserSettingsManager = UserSettingsManager(database_manager=current_app.database_manager)
    try:
        deleted_setting = settings_manager.delete(user_id=user_id, identifier=identifier)
        api_response = DeleteSingleResponse(raw=UserSettingModel.to_dict(deleted_setting), model=UserSettingModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerDeleteError as err:
        return abort(404, err.message)
    return api_response.make_response()
