# dataGerry - OpenSource Enterprise CMDB
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

from flask import abort, request
from cmdb.utils.interface_wraps import login_required, json_required
from cmdb.object_framework.cmdb_object_manager import object_manager as obm
from cmdb.interface.route_utils import make_response, RootBlueprint
from cmdb.object_framework.cmdb_errors import TypeNotFoundError, TypeInsertError
from cmdb.object_framework.cmdb_object_type import CmdbType

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
type_routes = RootBlueprint('type_routes', __name__, url_prefix='/type')

object_manager = obm


@type_routes.route('/', methods=['GET'])
@login_required
def get_type_list():
    try:
        type_list = object_manager.get_all_types()
    except CMDBError:
        return abort(500)
    resp = make_response(type_list)
    return resp


@type_routes.route('/<int:public_id>', methods=['GET'])

def get_type(public_id: int):
    try:
        type_instance = object_manager.get_type(public_id)
    except TypeNotFoundError:
        return abort(404)
    except CMDBError:
        return abort(500)
    resp = make_response(type_instance)
    return resp


@type_routes.route('/', methods=['POST'])
@login_required
@json_required
def add_type():
    from bson import json_util
    add_data_dump = json.dumps(request.json)
    try:
        new_type_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)
    try:
        type_instance = CmdbType(**new_type_data)
    except CMDBError:
        return abort(400)
    try:
        ack = object_manager.insert_type(type_instance)
    except TypeInsertError:
        return abort(500)

    resp = make_response(ack)
    return resp


@type_routes.route('/', methods=['PUT'])
@login_required
@json_required
def update_type():
    """TODO: Generate update log"""
    from bson import json_util
    add_data_dump = json.dumps(request.json)
    try:
        new_type_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)
    try:
        update_type_instance = CmdbType(**new_type_data)
    except CMDBError:
        return abort(400)

    try:
        object_manager.update_type(update_type_instance)
    except CMDBError:
        return abort(500)

    resp = make_response(update_type_instance)
    return resp


@type_routes.route('/<int:public_id>', methods=['DELETE'])
@login_required
def delete_type(public_id: int):
    try:
        ack = object_manager.delete_type(public_id=public_id)
    except TypeNotFoundError:
        return abort(400)
    except CMDBError:
        return abort(500)
    resp = make_response(ack)
    return resp
