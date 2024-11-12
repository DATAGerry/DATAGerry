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
import sys
import time
import logging

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.settings_reader_manager import SettingsReaderManager
from cmdb.utils.system_config import SystemConfigReader

from cmdb import __title__, __version__, __runtime__
from cmdb.interface.rest_api.routes.framework_routes.setting_routes import settings_blueprint
from cmdb.interface.route_utils import login_required, right_required, insert_request_user
from cmdb.interface.blueprint import NestedBlueprint
from cmdb.interface.rest_api.responses import DefaultResponse
from cmdb.models.user_model.user import UserModel
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

system_blueprint = NestedBlueprint(settings_blueprint, url_prefix='/system')

# -------------------------------------------------------------------------------------------------------------------- #

@system_blueprint.route('/', methods=['GET'])
@insert_request_user
@login_required
def get_datagerry_information(request_user: UserModel):
    """TODO: document"""
    settings_reader: SettingsReaderManager = ManagerProvider.get_manager(ManagerType.SETTINGS_READER_MANAGER,
                                                                               request_user)

    try:
        db_version = settings_reader.get_all_values_from_section('updater').get('version')
    except Exception as err:
        LOGGER.warning(err)
        db_version = 0

    datagerry_infos = {
        'title': __title__,
        'version': __version__,
        'db_version': db_version,
        'runtime': (time.time() - __runtime__),
        'starting_parameters': sys.argv
    }

    api_response = DefaultResponse(datagerry_infos)

    return api_response.make_response()


@system_blueprint.route('/config/', methods=['GET'])
@insert_request_user
@login_required
@right_required('base.system.view')
def get_config_information(request_user: UserModel):
    """TODO: document"""
    ssc = SystemConfigReader()

    config_dict = {
        'path': ssc.config_file,
        'properties': []
    }

    for section in ssc.get_sections():
        section_values = []

        for key, value in ssc.get_all_values_from_section(section).items():
            section_values.append([key, value])

        config_dict['properties'].append([section, section_values])

    api_response = DefaultResponse(config_dict)

    if len(config_dict) < 1:
        return api_response.make_response(204)

    return api_response.make_response()


@system_blueprint.route('/information/', methods=['GET'])
@system_blueprint.route('/information', methods=['GET'])
@login_required
@right_required('base.system.view')
def get_system_information():
    """TODO: document"""
    system_infos = {
        'platform': sys.platform,
        'python_interpreter': {
            'version': sys.version,
            'path': sys.path
        }
    }

    api_response = DefaultResponse(system_infos)

    return api_response.make_response()
