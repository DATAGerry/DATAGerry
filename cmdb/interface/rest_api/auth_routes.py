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
from datetime import datetime
from typing import List

from flask import request, current_app, abort

from cmdb.interface.route_utils import make_response, RootBlueprint
from cmdb.security.auth import AuthModule, AuthSettingsDAO
from cmdb.security.auth.auth_errors import AuthenticationError
from cmdb.security.token.generator import TokenGenerator
from cmdb.user_management.user_manager import UserManager
from cmdb.user_management.user_manager import user_manager, UserManagerGetError
from cmdb.utils import SystemSettingsReader

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

auth_blueprint = RootBlueprint('auth_rest', __name__, url_prefix='/auth')
LOGGER = logging.getLogger(__name__)

with current_app.app_context():
    user_manager: UserManager = current_app.user_manager
    system_settings_reader: SystemSettingsReader = SystemSettingsReader(current_app.database_manager)


@auth_blueprint.route('/settings/', methods=['GET'])
@auth_blueprint.route('/settings', methods=['GET'])
def get_auth_settings():
    auth_settings_values = system_settings_reader.get_all_values_from_section('auth')
    auth_module = AuthModule(AuthSettingsDAO(**auth_settings_values))
    return make_response(auth_module.settings)


@auth_blueprint.route('/providers/', methods=['GET'])
@auth_blueprint.route('/providers', methods=['GET'])
def get_installed_providers():
    provider_names: List[str] = []
    auth_module = AuthModule()
    for provider in auth_module.providers:
        provider_names.append(provider.get_name())
    return make_response(provider_names)


@auth_blueprint.route('/providers/config/<string:provider_class>/', methods=['GET'])
@auth_blueprint.route('/providers/config/<string:provider_class>', methods=['GET'])
def get_provider_config(provider_class: str):
    auth_settings_values = system_settings_reader.get_all_values_from_section('auth')
    auth_module = AuthModule(AuthSettingsDAO(**auth_settings_values))
    try:
        provider_class_config = auth_module.settings.get_provider_settings(provider_class).config
    except StopIteration:
        return abort(404, 'Provider not found')
    return make_response(provider_class_config)


@auth_blueprint.route('/login/', methods=['POST'])
@auth_blueprint.route('/login', methods=['POST'])
def post_login():
    login_data = request.json
    if not request.json:
        return abort(400, 'No valid JSON data was provided')

    request_user_name = login_data['user_name']
    request_password = login_data['password']

    auth_settings_values = system_settings_reader.get_all_values_from_section('auth')
    auth_module = AuthModule(AuthSettingsDAO(**auth_settings_values))
    user_instance = None
    # search for user in db
    try:
        founded_user = user_manager.get_user_by_name(user_name=request_user_name)
        provider_class_name = founded_user.get_authenticator()
        LOGGER.debug(f'[LOGIN] Founded user: {founded_user} with provider: {provider_class_name}')
        if not auth_module.provider_exists(provider_class_name):
            return abort(501, f'[LOGIN] Provider {provider_class_name} does not exists or is not installed')

        provider = auth_module.get_provider(provider_class_name)
        provider_config_class = provider.PROVIDER_CONFIG_CLASS
        provider_settings = auth_module.settings.get_provider_settings(provider.get_name())
        provider_config_instance = provider_config_class(**provider_settings)
        provider_instance = provider(config=provider_config_instance)
        if not provider_config_instance.is_active():
            return abort(503, f'Provider {provider_class_name} is deactivated')
        try:
            user_instance = provider_instance.authenticate(request_user_name, request_password)
        except AuthenticationError as ae:
            LOGGER.error(f'[LOGIN] User could not login: {ae}')

    # user is not in database - check for other providers
    except UserManagerGetError as umge:
        LOGGER.error(f'[LOGIN] {request_user_name} not in database: {umge}')
        LOGGER.info(f'[LOGIN] Check for other providers - request_user: {request_user_name}')

        # get installed providers
        provider_list = auth_module.providers
        LOGGER.debug(f'[LOGIN] Provider list: {provider_list}')
        external_enabled = auth_module.settings.enable_external
        for provider in provider_list:
            LOGGER.debug(f'[LOGIN] using provider: {provider}')
            provider_config_class = provider.PROVIDER_CONFIG_CLASS
            provider_settings = auth_module.settings.get_provider_settings(provider.get_name())
            provider_config_instance = provider_config_class(**provider_settings)

            if not provider_config_instance.is_active():
                LOGGER.info(f'[LOGIN] Provider {provider} is not activated -> skip')

            if not external_enabled:
                continue

            provider_instance = provider(config=provider_config_instance)
            try:
                user_instance = provider_instance.authenticate(request_user_name, request_password)
                # If successfully logged in
                if user_instance:
                    break
            except AuthenticationError as ae:
                LOGGER.error(
                    f'[LOGIN] User {request_user_name} could not validate with provider {provider}: {ae}')

            LOGGER.info(f'[LOGIN] Provider instance: {provider_instance}')
    finally:
        # If login success generate user instance with token
        if user_instance:
            user_instance.last_login_time = datetime.utcnow()
            user_manager.update_user(user_instance.public_id, user_instance.to_database())
            tg = TokenGenerator()
            token = tg.generate_token(payload={'user': {
                'public_id': user_instance.get_public_id()
            }})
            user_instance.token = token
            user_instance.token_issued_at = int(datetime.now().timestamp())
            user_instance.token_expire = int(tg.get_expire_time().timestamp())
            return make_response(user_instance)
        # Login not success
        else:
            return abort(401, 'Could not login')
