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
from cmdb.interface.route_utils import NestedBlueprint, make_response, login_required, right_required, \
    insert_request_user
from cmdb.user_management import User
from cmdb.utils.system_reader import SystemConfigReader

LOGGER = logging.getLogger(__name__)
try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

system_blueprint = NestedBlueprint(settings_blueprint, url_prefix='/system')


@system_blueprint.route('/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.system.view')
@current_app.cache.cached(timeout=50)
def get_datagerry_information(request_user: User):
    from cmdb import __title__, __version__, __runtime__
    datagerry_infos = {
        'title': __title__,
        'version': __version__,
        'runtime': (time.time() - __runtime__),
        'starting_parameters': sys.argv
    }
    return make_response(datagerry_infos)


@system_blueprint.route('/config/', methods=['GET'])
@system_blueprint.route('/config', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.system.view')
@current_app.cache.cached(timeout=1200)
def get_config_information(request_user: User):
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


@system_blueprint.route('/config/', methods=['POST'])
@system_blueprint.route('/config', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.system.reload')
def reload_config_reader(request_user: User):
    ssc = SystemConfigReader()
    ssc.setup()
    LOGGER.warning('Reload config file!')
    status = ssc.status()
    if status:
        current_app.cache.clear()
    return make_response(status)


@system_blueprint.route('/information/', methods=['GET'])
@system_blueprint.route('/information', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.system.view')
@current_app.cache.cached(timeout=50)
def get_system_information(request_user: User):
    system_infos = {
        'platform': sys.platform,
        'python_interpreter': {
            'version': sys.version,
            'path': sys.path
        }
    }
    return make_response(system_infos)
