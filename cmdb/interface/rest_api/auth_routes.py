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
from datetime import datetime, timezone
from typing import List

from flask import request, current_app, abort

from cmdb.interface.route_utils import make_response, insert_request_user
from cmdb.interface.blueprint import APIBlueprint
from cmdb.security.auth import AuthModule, AuthSettingsDAO
from cmdb.security.auth.auth_errors import AuthenticationProviderNotExistsError, \
    AuthenticationProviderNotActivated
from cmdb.security.auth.response import LoginResponse
from cmdb.security.security import SecurityManager
from cmdb.security.token.generator import TokenGenerator
from cmdb.user_management import UserModel, RightManager
from cmdb.user_management.managers.group_manager import GroupManager
from cmdb.user_management.managers.user_manager import UserManager
from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils.system_writer import SystemSettingsWriter
from cmdb.user_management.rights import __all__ as rights
# -------------------------------------------------------------------------------------------------------------------- #
auth_blueprint = APIBlueprint('auth', __name__)

LOGGER = logging.getLogger(__name__)

with current_app.app_context():
    system_settings_reader: SystemSettingsReader = SystemSettingsReader(current_app.database_manager)
    system_setting_writer: SystemSettingsWriter = SystemSettingsWriter(current_app.database_manager)


@auth_blueprint.route('/settings', methods=['GET'])
@auth_blueprint.protect(auth=True, right='base.system.view')
def get_auth_settings():
    """TODO: document"""
    auth_settings = system_settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__)
    auth_module = AuthModule(auth_settings)
    return make_response(auth_module.settings)


@auth_blueprint.route('/settings', methods=['POST', 'PUT'])
@auth_blueprint.protect(auth=True, right='base.system.edit')
@insert_request_user
def update_auth_settings(request_user: UserModel):
    """TODO: document"""
    new_auth_settings_values = request.get_json()
    if not new_auth_settings_values:
        return abort(400, 'No new data was provided')
    try:
        new_auth_setting_instance = AuthSettingsDAO(**new_auth_settings_values)
    except Exception as err:
        return abort(400, err)
    update_result = system_setting_writer.write(_id='auth', data=new_auth_setting_instance.__dict__)
    if update_result.acknowledged:
        return make_response(system_settings_reader.get_section('auth'))
    return abort(400, 'Could not update auth settings')


@auth_blueprint.route('/providers', methods=['GET'])
@auth_blueprint.protect(auth=True, right='base.system.view')
@insert_request_user
def get_installed_providers(request_user: UserModel):
    """TODO: document"""
    provider_names: List[dict] = []
    auth_module = AuthModule(
        system_settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__))
    for provider in auth_module.providers:
        provider_names.append({'class_name': provider.get_name(), 'external': provider.EXTERNAL_PROVIDER})
    return make_response(provider_names)


@auth_blueprint.route('/providers/<string:provider_class>', methods=['GET'])
@auth_blueprint.protect(auth=True, right='base.system.view')
@insert_request_user
def get_provider_config(provider_class: str, request_user: UserModel):
    """TODO: document"""
    auth_module = AuthModule(
        system_settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__))
    try:
        provider_class_config = auth_module.get_provider(provider_class).get_config()
    except StopIteration:
        return abort(404, 'Provider not found')
    return make_response(provider_class_config)


@auth_blueprint.route('/login', methods=['POST'])
def post_login():
    """TODO: document"""
    user_manager: UserManager = UserManager(current_app.database_manager)
    group_manager: GroupManager = GroupManager(current_app.database_manager, right_manager=RightManager(rights))
    security_manager: SecurityManager = SecurityManager(current_app.database_manager)
    login_data = request.json
    if not request.json:
        return abort(400, 'No valid JSON data was provided')

    request_user_name = login_data['user_name']
    request_password = login_data['password']

    auth_module = AuthModule(
        system_settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__),
        user_manager=user_manager, group_manager=group_manager,
        security_manager=security_manager)
    user_instance = None
    try:
        user_instance = auth_module.login(request_user_name, request_password)
    except (AuthenticationProviderNotExistsError, AuthenticationProviderNotActivated) as err:
        return abort(503, err.message)
    except Exception as err:
        return abort(401, err)
    finally:
        # If login success generate user instance with token
        if user_instance:
            tg = TokenGenerator(database_manager=current_app.database_manager)
            token: bytes = tg.generate_token(payload={'user': {
                'public_id': user_instance.get_public_id()
            }})
            token_issued_at = int(datetime.now(timezone.utc).timestamp())
            token_expire = int(tg.get_expire_time().timestamp())

            login_response = LoginResponse(user_instance, token, token_issued_at, token_expire)
            return login_response.make_response()

        # Login not success
        return abort(401, 'Could not login')
