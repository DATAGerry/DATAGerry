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

from bson import json_util

from cmdb.utils.wraps import login_required, right_required
from cmdb.interface.route_utils import make_response, RootBlueprint, abort
from cmdb.user_management.user_group import UserGroup
from cmdb.user_management.user_manager import user_manager, UserManagerInsertError, UserManagerGetError

from flask import request

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
group_routes = RootBlueprint('group_rest', __name__, url_prefix='/group')


@group_routes.route('/', methods=['GET'])
@login_required
def get_all_groups():
    try:
        group_list = user_manager.get_all_groups()
    except UserManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    if len(group_list) < 1:
        return make_response(group_list, 204)
    return make_response(group_list)


@group_routes.route('/<int:public_id>', methods=['GET'])
@login_required
def get_group(public_id: int):
    try:
        group_instance = user_manager.get_group(public_id)
    except UserManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    return make_response(group_instance)


@group_routes.route('/', methods=['POST'])
@login_required
def add_group():
    http_post_request_data = json.dumps(request.json)
    new_group_data = json.loads(http_post_request_data, object_hook=json_util.object_hook)
    new_group_data['public_id'] = user_manager.get_new_id(UserGroup.COLLECTION)

    try:
        new_group = UserGroup(**new_group_data)
    except (CMDBError, Exception) as err:
        LOGGER.error(err.message)
        return abort(400)
    try:
        insert_ack = user_manager.insert_group(new_group)
    except UserManagerInsertError as err:
        LOGGER.error(err)
        return abort(400)

    return make_response(insert_ack)


@group_routes.route('/<int:public_id>', methods=['PUT'])
@login_required
def edit_group(public_id: int):
    raise NotImplementedError


@group_routes.route('/<int:public_id>', methods=['DELETE'])
@login_required
def delete_group(public_id: int):
    raise NotImplementedError
