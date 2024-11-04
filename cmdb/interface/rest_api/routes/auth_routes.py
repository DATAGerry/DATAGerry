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
from typing import Tuple
from datetime import datetime, timezone
from flask import request, current_app, abort

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.security.security import SecurityManager
from cmdb.manager.users_manager import UsersManager

from cmdb.user_management.models.user import UserModel
from cmdb.security.auth.auth_settings import AuthSettingsDAO
from cmdb.security.auth.auth_module import AuthModule
from cmdb.security.auth.response import LoginResponse
from cmdb.security.token.generator import TokenGenerator
from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils.system_writer import SystemSettingsWriter
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.route_utils import check_user_in_mysql_db
from cmdb.interface.route_utils import make_response,\
                                       insert_request_user,\
                                       check_db_exists,\
                                       init_db_routine,\
                                       create_new_admin_user,\
                                       retrive_user
from cmdb.interface.rest_api.responses import GetSingleValueResponse

from cmdb.errors.manager.user_manager import UserManagerInsertError, UserManagerGetError
from cmdb.errors.provider import AuthenticationProviderNotActivated, AuthenticationProviderNotFoundError
# -------------------------------------------------------------------------------------------------------------------- #
LOGGER = logging.getLogger(__name__)

auth_blueprint = APIBlueprint('auth', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@auth_blueprint.route('/login', methods=['POST'])
def post_login():
    """TODO: document"""
    LOGGER.debug("[post_login] called")
    users_manager = UsersManager(current_app.database_manager)
    security_manager = SecurityManager(current_app.database_manager)
    login_data = request.json

    if not login_data:
        return abort(400, 'No valid JSON data was provided')

    request_user_name = login_data['user_name']
    request_password = login_data['password']

    try:
        if current_app.cloud_mode:
            user_data = check_user_in_mysql_db(request_user_name, request_password)

            if not user_data:
                return abort(401, 'Could not login')

            ### no db with this name, create it
            if not check_db_exists(user_data['database']):
                LOGGER.debug("[post_login] start init routine")
                init_db_routine(user_data['database'])
                create_new_admin_user(user_data)

            ### Get the user
            user = retrive_user(user_data)
            # User does not exist
            if not user:
                return abort(401, 'Could not login')

            current_app.database_manager.connector.set_database(user_data['database'])
            token, token_issued_at, token_expire = generate_token_with_params(user,
                                                                              current_app.database_manager,
                                                                              True)

            login_response = LoginResponse(user, token, token_issued_at, token_expire)

            return login_response.make_response()
    except UserManagerGetError as err:
        LOGGER.debug("[post_login] UserManagerGetError: %s", err)
        return abort(500, "Could not login because user can't be retrieved from database!")
    except UserManagerInsertError as err:
        LOGGER.debug("[post_login] UserManagerInsertError: %s", err)
        return abort(500, "Could not login because user can't be inserted in database!")
    except Exception as err: #pylint: disable=broad-exception-caught
        LOGGER.debug("[post_login] Exception: %s, Type: %s", err, type(err))
        return abort(500, "Could not login")

    #PATH when its not cloud mode
    system_settings_reader: SystemSettingsReader = SystemSettingsReader(current_app.database_manager)

    auth_module = AuthModule(
        system_settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__),
        security_manager=security_manager,
        users_manager=users_manager)

    user_instance = None

    try:
        user_instance = auth_module.login(request_user_name, request_password)

        if user_instance:
            token, token_issued_at, token_expire = generate_token_with_params(user_instance,
                                                                              current_app.database_manager)

            login_response = LoginResponse(user_instance, token, token_issued_at, token_expire)

            return login_response.make_response()

        return abort(401, 'Could not login!')
    except (AuthenticationProviderNotFoundError, AuthenticationProviderNotActivated):
        #ERROR-FIX
        return abort(503)
    except Exception as err: #pylint: disable=broad-exception-caught
        LOGGER.debug("[post_login] Exception: %s, Type: %s", err, type(err))
        return abort(500, "Could not login")

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@auth_blueprint.route('/settings', methods=['GET'])
@insert_request_user
@auth_blueprint.protect(auth=True, right='base.system.view')
def get_auth_settings(request_user: UserModel):
    """TODO: document"""
    system_settings_reader: SystemSettingsReader = ManagerProvider.get_manager(ManagerType.SYSTEM_SETTINGS_READER,
                                                                               request_user)

    auth_settings = system_settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__)
    auth_module = AuthModule(auth_settings)
    api_response = GetSingleValueResponse(auth_module.settings)

    return api_response.make_response()


@auth_blueprint.route('/providers', methods=['GET'])
@insert_request_user
@auth_blueprint.protect(auth=True, right='base.system.view')
def get_installed_providers(request_user: UserModel):
    """TODO: document"""
    provider_names: list[dict] = []

    system_settings_reader: SystemSettingsReader = ManagerProvider.get_manager(ManagerType.SYSTEM_SETTINGS_READER,
                                                                               request_user)

    auth_module = AuthModule(
        system_settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__))

    for provider in auth_module.providers:
        provider_names.append({'class_name': provider.get_name(), 'external': provider.EXTERNAL_PROVIDER})

    return make_response(provider_names)


@auth_blueprint.route('/providers/<string:provider_class>', methods=['GET'])
@insert_request_user
@auth_blueprint.protect(auth=True, right='base.system.view')
def get_provider_config(provider_class: str, request_user: UserModel):
    """TODO: document"""
    system_settings_reader: SystemSettingsReader = ManagerProvider.get_manager(ManagerType.SYSTEM_SETTINGS_READER,
                                                                               request_user)

    auth_module = AuthModule(
        system_settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__))

    try:
        provider_class_config = auth_module.get_provider(provider_class).get_config()
    except StopIteration:
        return abort(404, 'Provider not found')

    return make_response(provider_class_config)

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@auth_blueprint.route('/settings', methods=['POST', 'PUT'])
@insert_request_user
@auth_blueprint.protect(auth=True, right='base.system.edit')
def update_auth_settings(request_user: UserModel):
    """TODO: document"""
    new_auth_settings_values = request.get_json()

    system_settings_reader: SystemSettingsReader = ManagerProvider.get_manager(ManagerType.SYSTEM_SETTINGS_READER,
                                                                               request_user)
    system_setting_writer: SystemSettingsWriter = ManagerProvider.get_manager(ManagerType.SYSTEM_SETTINGS_WRITER,
                                                                               request_user)

    if not new_auth_settings_values:
        return abort(400, 'No new data was provided')

    try:
        new_auth_setting_instance = AuthSettingsDAO(**new_auth_settings_values)
    except Exception as err:
        return abort(400, err)

    update_result = system_setting_writer.write(_id='auth', data=new_auth_setting_instance.__dict__)

    if update_result.acknowledged:
        api_response = GetSingleValueResponse(system_settings_reader.get_section('auth'))
        return api_response.make_response()

    return abort(400, 'Could not update auth settings')

# ------------------------------------------------------ HELPERS ----------------------------------------------------- #

def generate_token_with_params(
        login_user: UserModel,
        database_manager: MongoDatabaseManager,
        cloud_mode: bool = False
    ) -> Tuple[bytes, int, int]:
    """TODO: document"""
    tg = TokenGenerator(database_manager)

    user_data = {'public_id': login_user.get_public_id()}

    if cloud_mode:
        user_data['database'] = login_user.get_database()

    token: bytes = tg.generate_token(payload={'user': user_data})

    token_issued_at = int(datetime.now(timezone.utc).timestamp())
    token_expire = int(tg.get_expire_time().timestamp())

    return token, token_issued_at, token_expire