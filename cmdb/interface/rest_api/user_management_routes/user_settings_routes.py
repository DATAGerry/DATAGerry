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
import logging
from flask import abort, request

from cmdb.manager.users_settings_manager import UsersSettingsManager

from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetListResponse, GetSingleResponse, InsertSingleResponse, DeleteSingleResponse, \
    UpdateSingleResponse
from cmdb.user_management.models.settings import UserSettingModel
from cmdb.interface.route_utils import insert_request_user
from cmdb.user_management.models.user import UserModel
from cmdb.manager.manager_provider import ManagerType, ManagerProvider

from cmdb.errors.manager import ManagerUpdateError, ManagerDeleteError, ManagerInsertError, ManagerGetError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

user_settings_blueprint = APIBlueprint('user_settings', __name__)

# -------------------------------------------------------------------------------------------------------------------- #

@user_settings_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
def get_user_settings(user_id: int, request_user: UserModel):
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
    users_settings_manager: UsersSettingsManager = ManagerProvider.get_manager(ManagerType.USERS_SETTINGS_MANAGER,
                                                                               request_user)

    try:
        settings: list[UserSettingModel] = users_settings_manager.get_user_settings(user_id=user_id)

        raw_settings = [UserSettingModel.to_dict(setting) for setting in settings]

        api_response = GetListResponse(results=raw_settings, url=request.url, model=UserSettingModel.MODEL,
                                       body=request.method == 'HEAD')
    except ManagerGetError:
        #ERROR-FIX
        return abort(404)

    return api_response.make_response()


@user_settings_blueprint.route('/<string:resource>', methods=['GET', 'HEAD'])
@insert_request_user
def get_user_setting(user_id: int, resource: str, request_user: UserModel):
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
    users_settings_manager: UsersSettingsManager = ManagerProvider.get_manager(ManagerType.USERS_SETTINGS_MANAGER,
                                                                               request_user)

    try:
        setting: UserSettingModel = users_settings_manager.get_user_setting(user_id, resource)

        api_response = GetSingleResponse(UserSettingModel.to_dict(setting), url=request.url,
                                         model=UserSettingModel.MODEL, body=request.method == 'HEAD')
    except ManagerGetError:
        #ERROR-FIX
        return abort(404)

    return api_response.make_response()


@user_settings_blueprint.route('/', methods=['POST'])
@insert_request_user
@user_settings_blueprint.validate(UserSettingModel.SCHEMA)
def insert_setting(user_id: int, data: dict, request_user: UserModel):
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
    users_settings_manager: UsersSettingsManager = ManagerProvider.get_manager(ManagerType.USERS_SETTINGS_MANAGER,
                                                                               request_user)

    try:
        users_settings_manager.insert_setting(data)

        setting: UserSettingModel = users_settings_manager.get_user_setting(user_id, data.get('resource'))
    except ManagerGetError as err:
        LOGGER.debug("[insert_setting] ManagerGetError: %s", err.message)
        return abort(404, "An error occured when creating the setting!")
    except ManagerInsertError as err:
        LOGGER.debug("[insert_setting] ManagerInsertError: %s", err.message)
        return abort(400, "Could not insert the setting!")

    api_response = InsertSingleResponse(raw=UserSettingModel.to_dict(setting),
                                        result_id=setting.resource,
                                        url=request.url,
                                        model=UserSettingModel.MODEL)

    return api_response.make_response(prefix=f'users/{user_id}/settings/{setting.resource}')


@user_settings_blueprint.route('/<string:resource>', methods=['PUT', 'PATCH'])
@insert_request_user
@user_settings_blueprint.validate(UserSettingModel.SCHEMA)
def update_setting(user_id: int, resource: str, data: dict, request_user: UserModel):
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
    users_settings_manager: UsersSettingsManager = ManagerProvider.get_manager(ManagerType.USERS_SETTINGS_MANAGER,
                                                                               request_user)

    try:
        setting = UserSettingModel.from_data(data=data)
        setting_found = True

        try:
            users_settings_manager.get_user_setting(user_id, data.get('resource'))
        except ManagerGetError:
            setting_found = False

        if setting_found:
            users_settings_manager.update_setting(user_id, resource, setting)
        else:
            users_settings_manager.insert_setting(data)

        api_response = UpdateSingleResponse(result=data, url=request.url, model=UserSettingModel.MODEL)
    except ManagerGetError:
        #ERROR-FIX
        return abort(404)
    except ManagerUpdateError as err:
        LOGGER.debug("[update_setting] ManagerUpdateError: %s", err.message)
        return abort(400, f"Setting for resource: {resource} could not be updated!")

    return api_response.make_response()


@user_settings_blueprint.route('/<string:resource>', methods=['DELETE'])
@insert_request_user
def delete_setting(user_id: int, resource: str, request_user: UserModel):
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
    users_settings_manager: UsersSettingsManager = ManagerProvider.get_manager(ManagerType.USERS_SETTINGS_MANAGER,
                                                                               request_user)

    try:
        deleted_setting = users_settings_manager.delete(user_id=user_id, resource=resource)
        api_response = DeleteSingleResponse(raw=UserSettingModel.to_dict(deleted_setting), model=UserSettingModel.MODEL)
    except ManagerGetError:
        #ERROR-FIX
        return abort(404)
    except ManagerDeleteError as err:
        LOGGER.debug("[delete_setting] ManagerDeleteError: %s", err.message)
        return abort(404, f"Could not delete the setting: {resource} !")

    return api_response.make_response()
