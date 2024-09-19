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
import json
import datetime
import time
import logging

from flask import abort, jsonify, Response

from cmdb.framework import TypeModel
from cmdb.interface.route_utils import login_required, insert_request_user
from cmdb.interface.blueprint import RootBlueprint
from cmdb.errors.type import TypeNotFoundError
from cmdb.utils import json_encoding
from cmdb.utils.error import CMDBError
from cmdb.user_management import UserModel
from cmdb.manager.manager_provider import ManagerType, ManagerProvider
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

type_export_blueprint = RootBlueprint('type_export_rest', __name__, url_prefix='/export/type')

# -------------------------------------------------------------------------------------------------------------------- #

@type_export_blueprint.route('/', methods=['POST'])
@insert_request_user
@login_required
def export_type(request_user: UserModel):
    """TODO: document"""
    object_manager = ManagerProvider.get_manager(ManagerType.CMDB_OBJECT_MANAGER, request_user)

    try:
        type_list = [TypeModel.to_json(type) for type in object_manager.get_all_types()]
        resp = json.dumps(type_list, default=json_encoding.default, indent=2)
    except TypeNotFoundError as e:
        return abort(400, e)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as err:
        LOGGER.info("Error occured in export_type(): %s", err)
        return abort(404, jsonify(message='Not Found'))

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H_%M_%S')

    return Response(
        resp,
        mimetype="text/json",
        headers={
            "Content-Disposition":
                f"attachment; filename={timestamp}.json"
        }
    )


@type_export_blueprint.route('/<string:public_ids>', methods=['POST'])
@insert_request_user
@login_required
def export_type_by_ids(public_ids, request_user: UserModel):
    """TODO: document"""
    object_manager = ManagerProvider.get_manager(ManagerType.CMDB_OBJECT_MANAGER, request_user)

    try:
        query_list = []
        for key, value in {'public_id': public_ids}.items():
            for v in value.split(","):
                try:
                    query_list.append({key: int(v)})
                except (ValueError, TypeError):
                    return abort(400)
        type_list_data = json.dumps([TypeModel.to_json(type_) for type_ in
                                     object_manager.get_types_by(sort="public_id", **{'$or': query_list})],
                                    default=json_encoding.default, indent=2)
    except TypeNotFoundError as e:
        return abort(400, e)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as err:
        LOGGER.info("Error occured in export_type_by_ids(): %s", err)
        return abort(404, jsonify(message='Not Found'))

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H_%M_%S')

    return Response(
        type_list_data,
        mimetype="text/json",
        headers={
            "Content-Disposition":
                f"attachment; filename={timestamp}.json"
        }
    )
