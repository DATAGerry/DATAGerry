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
import json
import logging
from datetime import datetime, timezone
from bson import json_util
from flask import request, abort

from cmdb.manager.types_manager import TypesManager

from cmdb.framework.models.type_model.type import TypeModel
from cmdb.interface.rest_api.routes.importer_routes.import_routes import importer_blueprint
from cmdb.interface.route_utils import login_required, insert_request_user
from cmdb.interface.blueprint import NestedBlueprint
from cmdb.interface.rest_api.responses import GetSingleValueResponse
from cmdb.user_management.models.user import UserModel
from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType

from cmdb.errors.manager import ManagerGetError, ManagerInsertError
# -------------------------------------------------------------------------------------------------------------------- #

importer_type_blueprint = NestedBlueprint(importer_blueprint, url_prefix='/type')

LOGGER = logging.getLogger(__name__)

@importer_type_blueprint.route('/create/', methods=['POST'])
@insert_request_user
@login_required
def add_type(request_user: UserModel):
    """TODO: document"""
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)

    error_collection = {}
    upload = request.form.get('uploadFile')
    new_type_list = json.loads(upload, object_hook=json_util.object_hook)

    for new_type_data in new_type_list:
        try:
            new_type_data['public_id'] = types_manager.get_new_type_public_id()
            new_type_data['creation_time'] = datetime.now(timezone.utc)
        except TypeError as e:
            LOGGER.error(e)
            return abort(400)
        try:
            type_instance = TypeModel.from_data(new_type_data)
            types_manager.insert_type(type_instance)
        except (ManagerInsertError, Exception) as err:
            #ERROR-FIX
            error_collection.update({"public_id": new_type_data['public_id'], "message": err})

    api_response = GetSingleValueResponse(error_collection)

    return api_response.make_response()


@importer_type_blueprint.route('/update/', methods=['POST'])
@insert_request_user
@login_required
def update_type(request_user: UserModel):
    """TODO: document"""
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)

    error_collection = {}
    upload = request.form.get('uploadFile')
    data_dump = json.loads(upload, object_hook=json_util.object_hook)

    for add_data_dump in data_dump:
        try:
            update_type_instance = TypeModel.from_data(add_data_dump)
        except Exception:
            #ERROR-FIX
            return abort(400)
        try:
            types_manager.get_type(update_type_instance.public_id)
            types_manager.update_type(update_type_instance.public_id, update_type_instance)
        except (ManagerGetError, Exception) as err:
            #ERROR-FIX
            error_collection.update({"public_id": add_data_dump['public_id'], "message": err})

    api_response = GetSingleValueResponse(error_collection)

    return api_response.make_response()
