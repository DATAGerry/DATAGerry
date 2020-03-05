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

from cmdb.interface.route_utils import make_response, RootBlueprint, login_required, insert_request_user, right_required
from cmdb.security.auth import AuthModule, AuthSettingsDAO
from cmdb.security.auth.auth_errors import AuthenticationProviderNotExistsError, \
    AuthenticationProviderNotActivated
from cmdb.security.token.generator import TokenGenerator
from cmdb.user_management import User
from cmdb.user_management.user_manager import UserManager
from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils.system_writer import SystemSettingsWriter

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

auth_blueprint = RootBlueprint('auth_rest', __name__, url_prefix='/auth')
LOGGER = logging.getLogger(__name__)

with current_app.app_context():
    user_manager: UserManager = current_app.user_manager
    system_settings_reader: SystemSettingsReader = SystemSettingsReader(current_app.database_manager)
    system_setting_writer: SystemSettingsWriter = SystemSettingsWriter(current_app.database_manager)


@auth_blueprint.route('/settings/', methods=['GET'])
@auth_blueprint.route('/settings', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.system.view')
def get_auth_settings(request_user: User):
    auth_module = AuthModule(system_settings_reader)
    return make_response(auth_module.settings)


@auth_blueprint.route('/settings/', methods=['POST', 'PUT'])
@auth_blueprint.route('/settings', methods=['POST', 'PUT'])
@login_required
@insert_request_user
@right_required('base.system.edit')
def update_auth_settings(request_user: User):
    new_auth_settings_values = request.get_json()
    if not new_auth_settings_values:
        return abort(400, 'No new data was provided')
    try:
        new_auth_setting_instance = AuthSettingsDAO(**new_auth_settings_values, default=AuthModule.__DEFAULT_SETTINGS__)
    except Exception as err:
        return abort(400, err)
    update_result = system_setting_writer.write(_id='auth', data=new_auth_setting_instance.__dict__)
    if update_result.acknowledged:
        return make_response(system_settings_reader.get_section('auth'))
    return abort(400, 'Could not update auth settings')


@auth_blueprint.route('/providers/', methods=['GET'])
@auth_blueprint.route('/providers', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.system.view')
def get_installed_providers(request_user: User):
    provider_names: List[dict] = []
    auth_module = AuthModule(system_settings_reader)
    for provider in auth_module.providers:
        provider_names.append({'class_name': provider.get_name(), 'external': provider.EXTERNAL_PROVIDER})
    return make_response(provider_names)


@auth_blueprint.route('/providers/<string:provider_class>/config/', methods=['GET'])
@auth_blueprint.route('/providers/<string:provider_class>/config', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.system.view')
def get_provider_config(provider_class: str, request_user: User):
    auth_module = AuthModule(system_settings_reader)
    try:
        provider_class_config = auth_module.get_provider(provider_class).get_config()
    except StopIteration:
        return abort(404, 'Provider not found')
    return make_response(provider_class_config)


@auth_blueprint.route('/providers/<string:provider_class>/config_form/', methods=['GET'])
@auth_blueprint.route('/providers/<string:provider_class>/config_form', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.system.view')
def get_provider_config_form(provider_class: str, request_user: User):
    auth_module = AuthModule(system_settings_reader)
    try:
        provider_class_config = auth_module.get_provider(provider_class).get_config().PROVIDER_CONFIG_FORM
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

    auth_module = AuthModule(system_settings_reader)
    user_instance = None
    try:
        user_instance = auth_module.login(user_manager, request_user_name, request_password)
    except (AuthenticationProviderNotExistsError, AuthenticationProviderNotActivated) as err:
        return abort(503, err.message)
    except Exception as e:
        return abort(401)
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
