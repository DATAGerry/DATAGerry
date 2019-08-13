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

from cmdb.framework.cmdb_object_manager import object_manager
from cmdb.interface.route_utils import RootBlueprint, make_response

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
status_routes = RootBlueprint('status_rest', __name__, url_prefix='/status')


@status_routes.route('/', methods=['GET'])
def get_status_list():
    return make_response(object_manager.get_all_status())


@status_routes.route('/<int:public_id>/', methods=['GET'])
@status_routes.route('/<int:public_id>', methods=['GET'])
def get_status(public_id: int):
    return make_response(public_id)


@status_routes.route('/', methods=['POST'])
def add_status():
    raise NotImplementedError


@status_routes.route('/', methods=['PUT'])
def update_status():
    raise NotImplementedError


@status_routes.route('/<int:public_id>/', methods=['DELETE'])
@status_routes.route('/<int:public_id>', methods=['DELETE'])
def delete_status(public_id: int):
    return make_response(public_id)
