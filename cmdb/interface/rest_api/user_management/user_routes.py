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

from flask import abort
from cmdb.utils.interface_wraps import login_required
from cmdb.interface.route_utils import RootBlueprint, make_response
from cmdb.user_management.user_manager import user_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
user_routes = RootBlueprint('user_rest', __name__, url_prefix='/user')


@login_required
@user_routes.route('/', methods=['GET'])
def get_users():
    try:
        users = user_manager.get_all_users()
    except CMDBError:
        return abort(404)

    resp = make_response(users)
    return resp


@login_required
@user_routes.route('/<int:public_id>', methods=['GET'])
def get_user(public_id):
    try:
        user = user_manager.get_user(public_id=public_id)
    except CMDBError:
        return abort(404)

    resp = make_response(user)
    return resp


@login_required
@user_routes.route('/', methods=['POST'])
def add_user():
    raise NotImplementedError


@login_required
@user_routes.route('/<int:public_id>', methods=['PUT'])
def update_user(public_id: int):
    raise NotImplementedError


@login_required
@user_routes.route('/<int:public_id>', methods=['DELETE'])
def delete_user(public_id: int):
    raise NotImplementedError
