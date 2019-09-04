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

from werkzeug.exceptions import abort

from cmdb.framework.cmdb_errors import ObjectManagerGetError
from cmdb.framework.cmdb_log import log_manager, LogManagerGetError
from cmdb.interface.route_utils import RootBlueprint, make_response

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
log_routes = RootBlueprint('log_rest', __name__, url_prefix='/log')


# CRUD routes
@log_routes.route('/<int:public_id>/', methods=['GET'])
@log_routes.route('/<int:public_id>', methods=['GET'])
def get_log(public_id: int):
    try:
        selected_log = log_manager.get_log(public_id=public_id)
    except LogManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    return make_response(selected_log)


@log_routes.route('/', methods=['POST'])
def insert_log(*args, **kwargs):
    """
    It is not planned to insert a log
    Returns:
        always a 405 Method Not Allowed	error
    """
    return abort(405)


@log_routes.route('/<int:public_id>/', methods=['PUT'])
@log_routes.route('/<int:public_id>', methods=['PUT'])
def update_log(public_id, *args, **kwargs):
    """
    It is not planned to update a log
    Returns:
        always a 405 Method Not Allowed	error
    """
    return abort(405)


@log_routes.route('/<int:public_id>/', methods=['DELETE'])
@log_routes.route('/<int:public_id>', methods=['DELETE'])
def delete_log(public_id: int):
    raise NotImplementedError


# FIND routes
@log_routes.route('/object/<int:public_id>/', methods=['GET'])
@log_routes.route('/object/<int:public_id>', methods=['GET'])
def get_logs_by_objects(public_id: int):
    try:
        object_logs = log_manager.get_object_logs(public_id=public_id)
    except ObjectManagerGetError as err:
        LOGGER.error(f'Error in get_logs_by_objects: {err}')
        return abort(404)
    if len(object_logs) < 1:
        return make_response(object_logs, 204)
    return make_response(object_logs)


@log_routes.route('/<int:public_id>/corresponding/', methods=['GET'])
@log_routes.route('/<int:public_id>/corresponding', methods=['GET'])
def get_corresponding_object_logs(public_id: int):
    try:
        selected_log = log_manager.get_log(public_id=public_id)
        query = {
            'log_type': 'CmdbObjectLog',
            'object_id': selected_log.object_id,
            'render_state': {
                '$ne': None
            },
            '$nor': [{
                'public_id': public_id
            }]
        }
        LOGGER.debug(f'Corresponding query: {query}')
        corresponding_logs = log_manager.get_logs_by(**query)
    except LogManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    LOGGER.debug(f'Corresponding logs: {corresponding_logs}')
    if len(corresponding_logs) < 1:
        return make_response(corresponding_logs, 204)

    return make_response(corresponding_logs)
