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
from flask import Blueprint, make_response, jsonify
from cmdb.data_storage import get_pre_init_database
try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

connection_routes = Blueprint('connection_routes', __name__)
LOGGER = logging.getLogger(__name__)


@connection_routes.route('/')
def connection_response():
    from cmdb import __title__, __version__

    resp = make_response(jsonify({
        'title': __title__,
        'version': __version__,
        'connected': get_pre_init_database().status()
    }))
    resp.mimetype = "application/json"
    return resp
