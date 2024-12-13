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
from flask import request, abort

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.settings_reader_manager import SettingsReaderManager
from cmdb.manager.settings_writer_manager import SettingsWriterManager

from cmdb.settings.date_settings import DateSettingsDAO
from cmdb.models.user_model.user import UserModel
from cmdb.interface.rest_api.responses import DefaultResponse
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.blueprints import APIBlueprint
# -------------------------------------------------------------------------------------------------------------------- #

date_blueprint = APIBlueprint('date', __name__)

LOGGER = logging.getLogger(__name__)

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@date_blueprint.route('/', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_date_settings(request_user: UserModel):
    """TODO: document"""
    settings_reader: SettingsReaderManager = ManagerProvider.get_manager(ManagerType.SETTINGS_READER_MANAGER,
                                                                        request_user)

    try:
        date_settings = settings_reader.get_all_values_from_section('date', DateSettingsDAO.__DEFAULT_SETTINGS__)

        date_settings = DateSettingsDAO(**date_settings)

        api_response = DefaultResponse(date_settings)

        return api_response.make_response()
    except Exception as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_date_settings] Exception: %s, Type: %s", err, type(err))
        return abort(500)

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@date_blueprint.route('/', methods=['POST', 'PUT'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@date_blueprint.protect(auth=True, right='base.system.edit')
def update_date_settings(request_user: UserModel):
    """TODO: document"""
    new_auth_settings_values = request.get_json()

    settings_reader: SettingsReaderManager = ManagerProvider.get_manager(ManagerType.SETTINGS_READER_MANAGER,
                                                                               request_user)
    settings_writer: SettingsWriterManager = ManagerProvider.get_manager(ManagerType.SETTINGS_WRITER_MANAGER,
                                                                               request_user)

    if not new_auth_settings_values:
        return abort(400, 'No new data was provided')
    try:
        new_auth_setting_instance = DateSettingsDAO(**new_auth_settings_values)
    except Exception as err:
        return abort(400, err)

    update_result = settings_writer.write(_id='date', data=new_auth_setting_instance.__dict__)

    if update_result.acknowledged:
        api_response = DefaultResponse(settings_reader.get_section('date'))

        return api_response.make_response()

    return abort(400, 'Could not update date settings')
