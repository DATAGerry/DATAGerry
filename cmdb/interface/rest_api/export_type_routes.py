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
import datetime
import time

from flask import abort, jsonify, current_app, Response
from cmdb.interface.route_utils import RootBlueprint, login_required
from cmdb.framework.cmdb_errors import TypeNotFoundError
from cmdb.utils import json_encoding

with current_app.app_context():
    object_manager = current_app.object_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
type_export_blueprint = RootBlueprint('type_export_rest', __name__, url_prefix='/export/type')


@type_export_blueprint.route('/', methods=['POST'])
# @login_required
def export_type():
    try:
        type_list = object_manager.get_all_types()
        resp = json.dumps(type_list, default=json_encoding.default, indent=2)
    except TypeNotFoundError as e:
        return abort(400, e.message)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as e:
        return abort(404, jsonify(message='Not Found', error=e.message))
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H_%M_%S')

    return Response(
            resp,
            mimetype="text/json",
            headers={
                "Content-Disposition":
                    "attachment; filename=%s.%s" % (timestamp, 'json')
            }
        )


@type_export_blueprint.route('/<string:public_ids>', methods=['POST'])
@login_required
def export_type_by_ids(public_ids):
    try:
        type_list = []
        try:
            query_list = []
            for key, value in {'public_id': public_ids}.items():
                for v in value.split(","):
                    try:
                        query_list.append({key: int(v)})
                    except (ValueError, TypeError):
                        return abort(400)
            type_list = object_manager.get_types_by(sort="public_id", **{'$or': query_list})
        except CMDBError as e:
            abort(400, e)

        for obj in type_list:
            type_obj = obj.__dict__
            del type_obj['_id']

        resp = json.dumps(type_list, default=json_encoding.default, indent=2)

    except TypeNotFoundError as e:
        return abort(400, e.message)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as e:
        return abort(404, jsonify(message='Not Found', error=e.message))
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H_%M_%S')

    return Response(
        resp,
        mimetype="text/json",
        headers={
            "Content-Disposition":
                "attachment; filename=%s.%s" % (timestamp, 'json')
        }
    )
