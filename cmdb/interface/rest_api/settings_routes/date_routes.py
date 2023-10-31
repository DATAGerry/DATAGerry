# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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

import logging

from flask import request, current_app, abort

from cmdb.interface.route_utils import make_response
from cmdb.interface.blueprint import APIBlueprint

from cmdb.settings.date.date_settings import DateSettingsDAO
from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils.system_writer import SystemSettingsWriter

date_blueprint = APIBlueprint('date', __name__)
LOGGER = logging.getLogger(__name__)

with current_app.app_context():
    system_settings_reader: SystemSettingsReader = SystemSettingsReader(current_app.database_manager)
    system_setting_writer: SystemSettingsWriter = SystemSettingsWriter(current_app.database_manager)


@date_blueprint.route('/', methods=['GET'])
def get_date_settings():
    date_settings = system_settings_reader.get_all_values_from_section('date',
                                                                       default=DateSettingsDAO.__DEFAULT_SETTINGS__)
    date_settings = DateSettingsDAO(**date_settings)
    return make_response(date_settings)


@date_blueprint.route('/', methods=['POST', 'PUT'])
@date_blueprint.protect(auth=True, right='base.system.edit')
def update_date_settings():
    new_auth_settings_values = request.get_json()
    if not new_auth_settings_values:
        return abort(400, 'No new data was provided')
    try:
        new_auth_setting_instance = DateSettingsDAO(**new_auth_settings_values)
    except Exception as err:
        return abort(400, err)
    update_result = system_setting_writer.write(_id='date', data=new_auth_setting_instance.__dict__)
    if update_result.acknowledged:
        return make_response(system_settings_reader.get_section('date'))
    return abort(400, 'Could not update date settings')
