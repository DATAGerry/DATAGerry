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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from typing import List

from flask import current_app, abort, request

from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetListResponse
from cmdb.manager import ManagerGetError
from cmdb.user_management import UserSettingModel
from cmdb.user_management.managers.setting_manager import UserSettingsManager

user_settings_blueprint = APIBlueprint('user_settings', __name__)


@user_settings_blueprint.route('/', methods=['GET'])
def get_user_settings(user_id: int):
    settings_manager = UserSettingsManager(database_manager=current_app.database_manager)
    try:
        settings: List[UserSettingModel] = settings_manager.get_user_settings(user_id=user_id)
        raw_settings = [UserSettingModel.to_dict(setting) for setting in settings]
        api_response = GetListResponse(results=raw_settings, url=request.url, model=UserSettingModel.MODEL,
                                       body=request.method == 'HEAD')
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()
