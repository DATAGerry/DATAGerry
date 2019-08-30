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

from flask import request
from werkzeug.exceptions import abort
from bson import json_util

from cmdb.framework.cmdb_object_manager import object_manager
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerInsertError, ObjectManagerUpdateError
from cmdb.framework.cmdb_status import CmdbStatus
from cmdb.interface.route_utils import RootBlueprint, make_response

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
log_routes = RootBlueprint('status_rest', __name__, url_prefix='/log')


@log_routes.route('/<int:public_id>', methods=['GET'])
@log_routes.route('/<int:public_id>/', methods=['GET'])
def get_log(public_id: int):
    try:
        status = object_manager.get_status(public_id)
    except ObjectManagerGetError:
        return abort(404)
    return make_response(status)