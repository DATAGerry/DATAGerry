# Net|CMDB - OpenSource Enterprise CMDB
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

from cmdb.utils.interface_wraps import login_required, right_required
from cmdb.interface.route_utils import make_response, RootBlueprint
from cmdb.user_management.user_manager import user_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
group_routes = RootBlueprint('group_rest', __name__, url_prefix='/group')


@group_routes.route('/', methods=['GET'])
@login_required
def get_all_groups():
    group_list = user_manager.get_all_groups()
    resp = make_response(group_list)
    return resp


@group_routes.route('/<int:public_id>', methods=['GET'])
@login_required
def get_group(public_id: int):
    group_instance = user_manager.get_group(public_id)
    resp = make_response(group_instance)
    return resp


@group_routes.route('/', methods=['POST'])
@login_required
@right_required('base.system.user.manage_groups')
def add_group():
    raise NotImplementedError


@group_routes.route('/<int:public_id>', methods=['PUT'])
@login_required
@right_required('base.system.user.manage_groups')
def edit_group(public_id: int):
    raise NotImplementedError


@group_routes.route('/<int:public_id>', methods=['DELETE'])
@login_required
@right_required('base.system.user.manage_groups')
def delete_group(public_id: int):
    raise NotImplementedError
