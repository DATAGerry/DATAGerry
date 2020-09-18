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
from flask import request, current_app

from cmdb.interface.route_utils import make_response, abort, login_required, insert_request_user, \
    right_required
from cmdb.interface.blueprint import RootBlueprint
from cmdb.user_management import UserModel
from cmdb.user_management.models.group import UserGroupModel
from cmdb.user_management.user_manager import UserManager, UserManagerInsertError, UserManagerGetError, \
    UserManagerUpdateError, UserManagerDeleteError

with current_app.app_context():
    user_manager: UserManager = current_app.user_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
group_blueprint = RootBlueprint('group_rest', __name__, url_prefix='/group')


@group_blueprint.route('/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.user-management.group.view')
def get_all_groups(request_user: UserModel):
    try:
        group_list = user_manager.get_groups()
    except UserManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    if len(group_list) < 1:
        return make_response(group_list, 204)
    return make_response(group_list)


@group_blueprint.route('/<int:public_id>/', methods=['GET'])
@group_blueprint.route('/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.user-management.group.view', {'group_id': 'public_id'})
def get_group(public_id: int, request_user: UserModel):
    try:
        group_instance = user_manager.get_group(public_id)
    except UserManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    return make_response(group_instance)


@group_blueprint.route('/<string:group_name>/', methods=['GET'])
@group_blueprint.route('/<string:group_name>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.user-management.group.view')
def get_group_by_name(group_name: str, request_user: UserModel):
    try:
        group = user_manager.get_group_by(name=group_name)
    except UserManagerGetError:
        return abort(404)
    return make_response(group)


@group_blueprint.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.user-management.group.add')
def add_group(request_user: UserModel):
    http_post_request_data = json.dumps(request.json)
    new_group_data = json.loads(http_post_request_data, object_hook=json_util.object_hook)
    new_group_data['public_id'] = user_manager.get_new_id(UserGroupModel.COLLECTION)

    try:
        new_group = UserGroupModel(**new_group_data)
    except (CMDBError, Exception) as err:
        LOGGER.error(err.message)
        return abort(400)
    try:
        insert_ack = user_manager.insert_group(new_group)
    except UserManagerInsertError as err:
        LOGGER.error(err)
        return abort(400)

    return make_response(insert_ack)


@group_blueprint.route('/<int:public_id>/', methods=['PUT'])
@group_blueprint.route('/<int:public_id>', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.user-management.group.edit')
def edit_group(public_id: int, request_user: UserModel):
    updated_group_params = json.dumps(request.json)
    try:
        response = user_manager.update_group(public_id,
                                             json.loads(updated_group_params, object_hook=json_util.object_hook))
    except UserManagerUpdateError as umue:
        LOGGER.error(umue)
        return abort(400)
    return make_response(response.acknowledged)


@group_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@group_blueprint.route('/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.user-management.group.delete')
def delete_group(public_id: int, request_user: UserModel):
    action = request.args.get('action')
    options = None
    if request.args.get('options'):
        options = json.loads(request.args.get('options'))
    if action is None:
        return abort(400)
    try:
        ack = user_manager.delete_group(public_id, action, options=options)
    except UserManagerDeleteError as err:
        LOGGER.error(err)
        return abort(500)
    return make_response(ack)
