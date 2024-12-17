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
from flask import current_app
from werkzeug.exceptions import abort

from cmdb.database.mongo_database_manager import MongoDatabaseManager

from cmdb.interface.route_utils import verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses import DefaultResponse
from cmdb.interface.blueprints import RootBlueprint
# -------------------------------------------------------------------------------------------------------------------- #

debug_blueprint = RootBlueprint('debug_rest', __name__, url_prefix='/debug')

with current_app.app_context():
    dbm: MongoDatabaseManager = current_app.database_manager

# -------------------------------------------------------------------------------------------------------------------- #

@debug_blueprint.route('/indexes/<string:collection>/', methods=['GET'])
@debug_blueprint.route('/indexes/<string:collection>', methods=['GET'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_index(collection: str):
    """TODO: document"""
    return DefaultResponse(dbm.get_index_info(collection)).make_response()


@debug_blueprint.route('/error/<int:status_code>/', methods=['GET', 'POST'])
@debug_blueprint.route('/error/<int:status_code>', methods=['GET', 'POST'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def trigger_error_handler(status_code: int):
    """TODO: document"""
    return abort(status_code)


@debug_blueprint.route('/error/<int:status_code>/<string:description>/', methods=['GET', 'POST'])
@debug_blueprint.route('/error/<int:status_code>/<string:description>', methods=['GET', 'POST'])
def trigger_error_handler_with_description(status_code: int, description: str):
    """TODO: document"""
    return abort(status_code, description=description)
