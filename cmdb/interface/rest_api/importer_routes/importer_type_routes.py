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

from cmdb.manager.type_manager import TypeManager

from cmdb.framework import TypeModel
from cmdb.interface.rest_api.import_routes import importer_blueprint
from cmdb.interface.route_utils import login_required, make_response, insert_request_user
from cmdb.interface.blueprint import NestedBlueprint
from cmdb.user_management.models.user import UserModel
from cmdb.manager.manager_provider import ManagerType, ManagerProvider

from cmdb.errors.manager import ManagerGetError, ManagerInsertError
# -------------------------------------------------------------------------------------------------------------------- #

importer_type_blueprint = NestedBlueprint(importer_blueprint, url_prefix='/type')

LOGGER = logging.getLogger(__name__)

@importer_type_blueprint.route('/create/', methods=['POST'])
@insert_request_user
@login_required
def add_type(request_user: UserModel):
    """TODO: document"""
    type_manager: TypeManager = ManagerProvider.get_manager(ManagerType.TYPE_MANAGER, request_user)

    error_collection = {}
    upload = request.form.get('uploadFile')
    new_type_list = json.loads(upload, object_hook=json_util.object_hook)

    for new_type_data in new_type_list:
        try:
            new_type_data['public_id'] = type_manager.get_new_id()
            new_type_data['creation_time'] = datetime.now(timezone.utc)
        except TypeError as e:
            LOGGER.error(e)
            return abort(400)
        try:
            type_instance = TypeModel.from_data(new_type_data)
            type_manager.insert(type_instance)
        except (ManagerInsertError, Exception) as err:
            #TODO: ERROR-FIX
            error_collection.update({"public_id": new_type_data['public_id'], "message": err})

    return make_response(error_collection)


@importer_type_blueprint.route('/update/', methods=['POST'])
@insert_request_user
@login_required
def update_type(request_user: UserModel):
    """TODO: document"""
    type_manager: TypeManager = ManagerProvider.get_manager(ManagerType.TYPE_MANAGER, request_user)

    error_collection = {}
    upload = request.form.get('uploadFile')
    data_dump = json.loads(upload, object_hook=json_util.object_hook)

    for add_data_dump in data_dump:
        try:
            update_type_instance = TypeModel.from_data(add_data_dump)
        except Exception:
            #TODO: ERROR-FIX
            return abort(400)
        try:
            type_manager.get(update_type_instance.public_id)
            type_manager.update(update_type_instance.public_id, update_type_instance)
        except (ManagerGetError, Exception) as err:
            #TODO: ERROR-FIX
            error_collection.update({"public_id": add_data_dump['public_id'], "message": err})

    return make_response(error_collection)
