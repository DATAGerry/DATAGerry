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
import sys
import time

from flask import current_app

from cmdb.interface.rest_api.setting_routes import settings_blueprint
from cmdb.interface.route_utils import make_response, login_required, right_required, \
    insert_request_user
from cmdb.interface.blueprint import NestedBlueprint
from cmdb.user_management import UserModel
from cmdb.utils.system_config import SystemConfigReader
from cmdb.utils.system_reader import SystemSettingsReader

LOGGER = logging.getLogger(__name__)
try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

system_blueprint = NestedBlueprint(settings_blueprint, url_prefix='/system')

with current_app.app_context():
    system_settings_reader: SystemSettingsReader = SystemSettingsReader(current_app.database_manager)


@system_blueprint.route('/', methods=['GET'])
@login_required
@insert_request_user
def get_datagerry_information(request_user: UserModel):
    from cmdb import __title__, __version__, __runtime__

    try:
        db_version = system_settings_reader.get_all_values_from_section('updater').get('version')
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
    return make_response(datagerry_infos)


@system_blueprint.route('/config/', methods=['GET'])
@system_blueprint.route('/config', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.system.view')
def get_config_information(request_user: UserModel):

    ssc = SystemConfigReader()
    config_dict = {
        'path': ssc.config_file,
        'properties': []
    }
    ssc = SystemConfigReader()
    for section in ssc.get_sections():
        section_values = []
        for key, value in ssc.get_all_values_from_section(section).items():
            section_values.append([key, value])
        config_dict['properties'].append([
            section, section_values
        ])
    if len(config_dict) < 1:
        return make_response(config_dict, 204)
    return make_response(config_dict)


@system_blueprint.route('/information/', methods=['GET'])
@system_blueprint.route('/information', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.system.view')
def get_system_information(request_user: UserModel):
    system_infos = {
        'platform': sys.platform,
        'python_interpreter': {
            'version': sys.version,
            'path': sys.path
        }
    }
    return make_response(system_infos)
