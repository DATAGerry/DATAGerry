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

import json
import logging

from flask import abort, jsonify, request, current_app

from cmdb.framework import CmdbObject
from cmdb.framework.cmdb_errors import ObjectDeleteError, ObjectInsertError, ObjectNotFoundError
from cmdb.framework.cmdb_log import LogAction, log_manager, CmdbMetaLog, CmdbObjectLog, LogManagerInsertError
from cmdb.framework.cmdb_object_manager import object_manager
from cmdb.framework.cmdb_render import CmdbRender
from cmdb.interface.route_utils import make_response, RootBlueprint, insert_request_user
from cmdb.user_management import User
from cmdb.utils.interface_wraps import login_required

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
object_rest = RootBlueprint('object_rest', __name__, url_prefix='/object')
with current_app.app_context():
    from cmdb.interface.rest_api.object_link_routes import link_rest

    object_rest.register_nested_blueprint(link_rest)


# DEFAULT ROUTES

@object_rest.route('/', methods=['GET'])
@login_required
def get_object_list():
    try:
        all_objects_list = object_manager.get_all_objects()

    except CMDBError:
        return abort(400)

    resp = make_response(all_objects_list)
    return resp


@object_rest.route('/type/<string:type_ids>', methods=['GET'])
@login_required
def get_object_by_type(type_ids):
    """Return all objects by type_id"""
    try:
        query = _build_query({'type_id': type_ids}, q_operator='$or')
        all_objects_list = object_manager.get_objects_by(sort="type_id", **query)

    except CMDBError:
        return abort(400)

    resp = make_response(all_objects_list)
    return resp


@object_rest.route('/many/<string:public_ids>', methods=['GET'])
@login_required
def get_objects_by_public_id(public_ids):
    """Return all objects by public_ids"""

    try:
        query = _build_query({'public_id': public_ids}, q_operator='$or')
        all_objects_list = object_manager.get_objects_by(sort="public_id", **query)

    except CMDBError:
        return abort(400)

    resp = make_response(all_objects_list)
    return resp


@object_rest.route('/count/<int:type_id>', methods=['GET'])
@login_required
def count_object_by_type(type_id):
    try:
        count = object_manager.count_objects_by_type(type_id)
        resp = make_response(count)
    except CMDBError:
        return abort(400)
    return resp


@object_rest.route('/count/', methods=['GET'])
@login_required
def count_objects():
    try:
        count = object_manager.count_objects()
        resp = make_response(count)
    except CMDBError:
        return abort(400)
    return resp


def _build_query(args, q_operator='$and'):
    query_list = []
    try:
        for key, value in args.items():
            for v in value.split(","):
                try:
                    query_list.append({key: int(v)})
                except (ValueError, TypeError):
                    return abort(400)
        return {q_operator: query_list}

    except CMDBError:
        pass


@object_rest.route('/native', methods=['GET'])
@login_required
def get_native_object_list():
    try:
        object_list = object_manager.get_all_objects()
    except CMDBError:
        return abort(404)
    resp = make_response(object_list)
    return resp


@object_rest.route('/<int:public_id>', methods=['GET'])
@login_required
def get_object(public_id):
    try:
        object_instance = object_manager.get_object(public_id)
    except ObjectNotFoundError as e:
        return jsonify(message='Not Found', error=e.message)
    except CMDBError:
        return abort(404)

    try:
        type_instance = object_manager.get_type(object_instance.get_type_id())
    except CMDBError:
        return abort(404)

    try:
        render = CmdbRender(object_instance=object_instance, type_instance=type_instance)
        render_result = render.result()
    except CMDBError:
        return abort(404)

    resp = make_response(render_result)
    return resp


@object_rest.route('<int:public_id>/native/', methods=['GET'])
@login_required
def get_native_object(public_id: int):
    try:
        object_instance = object_manager.get_object(public_id)
    except CMDBError:
        return abort(404)
    resp = make_response(object_instance)
    return resp


@object_rest.route('/', methods=['POST'])
@login_required
def add_object():
    from bson import json_util
    from datetime import datetime
    add_data_dump = json.dumps(request.json)

    try:
        new_object_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
        new_object_data['public_id'] = object_manager.get_highest_id(CmdbObject.COLLECTION) + 1
        new_object_data['creation_time'] = datetime.utcnow()
        new_object_data['last_edit_time'] = datetime.utcnow()
        new_object_data['views'] = 0
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)
    try:
        object_instance = CmdbObject(**new_object_data)
    except CMDBError as e:
        LOGGER.debug(e.message)
        return abort(400)
    try:
        ack = object_manager.insert_object(object_instance)
    except ObjectInsertError:
        return abort(500)

    resp = make_response(ack)
    return resp


@object_rest.route('/', methods=['PUT'])
@login_required
@insert_request_user
def update_object(request_user: User):
    from bson import json_util
    from datetime import datetime
    add_data_dump = json.dumps(request.json)
    try:
        up_object_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
        up_object_data['last_edit_time'] = datetime.utcnow()
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)

    try:
        update_object_instance = CmdbObject(**up_object_data)
    except CMDBError as e:
        LOGGER.warning(e)
        return abort(400)
    old_object = object_manager.get_object(update_object_instance.get_public_id())
    changes = old_object / update_object_instance
    # Generate log
    try:
        update_log = {
            'public_id': object_manager.get_highest_id(CmdbMetaLog.COLLECTION) + 1,
            'object_id': old_object.get_public_id(),
            'log_type': CmdbObjectLog.__name__,
            'log_time': datetime.utcnow(),
            'version': old_object.get_version(),
            'user_id': request_user.get_public_id(),
            'user_name': request_user.get_name(),
            'changes': changes,
            'action': LogAction.EDIT.value,
        }
    except CMDBError as err:
        LOGGER.error(err.message)

    try:
        ack = object_manager.update_object(update_object_instance)
    except CMDBError as e:
        LOGGER.warning(e)
        return abort(500)

    try:
        log_manager.insert_log(update_log)
    except LogManagerInsertError as err:
        LOGGER.error(err.message)

    resp = make_response(ack)
    return resp


@object_rest.route('/<int:public_id>', methods=['DELETE'])
@login_required
def delete_object(public_id: int):
    try:
        ack = object_manager.delete_object(public_id=public_id)
    except ObjectDeleteError:
        return abort(400)
    except CMDBError:
        return abort(500)
    resp = make_response(ack)
    return resp


@object_rest.route('/delete/<string:public_ids>', methods=['GET'])
@login_required
def delete_many_objects(public_ids):
    try:
        ids = []
        operator_in = {'$in': []}
        filter_public_ids = {'public_id': {}}

        for v in public_ids.split(","):
            try:
                ids.append(int(v))
            except (ValueError, TypeError):
                return abort(400)

        operator_in.update({'$in': ids})
        filter_public_ids.update({'public_id': operator_in})

        ack = object_manager.delete_many_objects(filter_public_ids)
        return make_response(ack.raw_result)
    except ObjectDeleteError as e:
        return jsonify(message='Delete Error', error=e.message)
    except CMDBError:
        return abort(500)
