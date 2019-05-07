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

from cmdb.utils.interface_wraps import login_required
from cmdb.interface.route_utils import make_response, RootBlueprint
from cmdb.user_management.user_manager import user_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
right_routes = RootBlueprint('right_rest', __name__, url_prefix='/right')


@login_required
@right_routes.route('/', methods=['GET'])
def get_all_rights():
    right_list = user_manager.get_all_rights()

    resp = make_response(right_list)
    return resp


@login_required
@right_routes.route('/tree', methods=['GET'])
def get_right_tree():
    right_tree = user_manager.get_right_tree()
    resp = make_response(right_tree)
    return resp


@login_required
@right_routes.route('/<string:name>', methods=['GET'])
def get_right(name: str):
    right_instance = user_manager.get_right_by_name(name)
    return make_response(right_instance)


@login_required
@right_routes.route('/level/<int:level>', methods=['GET'])
def get_rights_with_min_level(level: int):
    right_list = user_manager.get_right_names_with_min_level(level)
    return make_response(right_list)


@login_required
@right_routes.route('/levels', methods=['GET'])
def get_security_levels():
    security_levels = user_manager.get_security_levels()
    return make_response(security_levels)

# other crud functions are not required because of static right programming
