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
from flask import current_app

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.settings_reader_manager import SettingsReaderManager

from cmdb.interface.route_utils import login_required, insert_request_user, right_required
from cmdb.interface.blueprint import RootBlueprint
from cmdb.interface.rest_api.responses import DefaultResponse
from cmdb.models.user_model.user import UserModel
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

settings_blueprint = RootBlueprint('settings_rest', __name__, url_prefix='/settings')

with current_app.app_context():
    from cmdb.interface.rest_api.routes.settings_routes.system_routes import system_blueprint
    settings_blueprint.register_nested_blueprint(system_blueprint)

# -------------------------------------------------------------------------------------------------------------------- #

@settings_blueprint.route('/<string:section>/', methods=['GET'])
@settings_blueprint.route('/<string:section>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.system.view')
def get_settings_from_section(section: str, request_user: UserModel):
    """TODO: document"""
    settings_reader: SettingsReaderManager = ManagerProvider.get_manager(ManagerType.SETTINGS_READER_MANAGER,
                                                                               request_user)

    section_settings = settings_reader.get_all_values_from_section(section=section)

    if len(section_settings) < 1:
        return DefaultResponse([]).make_response(204)

    api_response = DefaultResponse(section_settings)

    return api_response.make_response()


@settings_blueprint.route('/<string:section>/<string:name>/', methods=['GET'])
@settings_blueprint.route('/<string:section>/<string:name>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.system.view')
def get_value_from_section(section: str, name: str, request_user: UserModel):
    """TODO: document"""
    settings_reader: SettingsReaderManager = ManagerProvider.get_manager(ManagerType.SETTINGS_READER_MANAGER,
                                                                               request_user)

    section_settings = settings_reader.get_value(name=name, section=section)

    if len(section_settings) < 1:
        return DefaultResponse([]).make_response(204)

    api_response = DefaultResponse(section_settings)

    return api_response.make_response()
