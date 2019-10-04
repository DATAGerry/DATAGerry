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
import json

from flask import request, current_app
from werkzeug.exceptions import abort
from bson import json_util

from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerInsertError, ObjectManagerUpdateError
from cmdb.framework.cmdb_status import CmdbStatus
from cmdb.interface.route_utils import RootBlueprint, make_response

with current_app.app_context():
    object_manager = current_app.object_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
status_blueprint = RootBlueprint('status_rest', __name__, url_prefix='/status')


@status_blueprint.route('/', methods=['GET'])
def get_statuses():
    try:
        status = object_manager.get_statuses()
    except ObjectManagerGetError:
        return abort(404)
    if len(status) < 1:
        return make_response(status, 204)
    return make_response(status)


@status_blueprint.route('/<int:public_id>/', methods=['GET'])
@status_blueprint.route('/<int:public_id>', methods=['GET'])
def get_status(public_id: int):
    try:
        status = object_manager.get_status(public_id)
    except ObjectManagerGetError:
        return abort(404)
    return make_response(status)


@status_blueprint.route('/', methods=['POST'])
def add_status():
    new_status_params = {**request.json, **{'public_id': int(object_manager.get_new_id(CmdbStatus.COLLECTION) + 1)}}
    try:
        ack = object_manager.insert_status(new_status_params)
    except ObjectManagerInsertError:
        return abort(400)
    return make_response(ack)


@status_blueprint.route('/', methods=['PUT'])
def update_status():
    updated_status_params = json.dumps(request.json)
    try:
        ack = object_manager.update_status(json.loads(updated_status_params, object_hook=json_util.object_hook))
    except ObjectManagerUpdateError:
        return abort(400)
    return make_response(ack)


@status_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@status_blueprint.route('/<int:public_id>', methods=['DELETE'])
def delete_status(public_id: int):
    raise NotImplementedError
