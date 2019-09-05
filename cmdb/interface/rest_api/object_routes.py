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
from datetime import datetime

from flask import abort, jsonify, request, current_app

from cmdb.framework import CmdbObject
from cmdb.framework.cmdb_errors import ObjectDeleteError, ObjectInsertError, ObjectManagerGetError, \
    ObjectManagerUpdateError
from cmdb.framework.cmdb_log import LogAction, log_manager, CmdbObjectLog, LogManagerInsertError
from cmdb.framework.cmdb_object_manager import object_manager
from cmdb.framework.cmdb_render import CmdbRender, RenderList, RenderError
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
@insert_request_user
def get_object(public_id, request_user: User):
    try:
        object_instance = object_manager.get_object(public_id)
    except ObjectManagerGetError as err:
        LOGGER.error(err)
        return abort(404)

    try:
        type_instance = object_manager.get_type(object_instance.get_type_id())
    except ObjectManagerGetError as err:
        LOGGER.error(err)
        return abort(404)

    try:
        render = CmdbRender(object_instance=object_instance, type_instance=type_instance, render_user=request_user)
        render_result = render.result()
    except RenderError as err:
        LOGGER.error(err)
        return abort(500)

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


@object_rest.route('/reference/<int:public_id>/', methods=['GET'])
@object_rest.route('/reference/<int:public_id>', methods=['GET'])
@insert_request_user
def get_objects_by_reference(public_id: int, request_user: User):
    try:
        reference_list: list = object_manager.get_object_references(public_id=public_id)
        rendered_reference_list = RenderList(reference_list, request_user).render_result_list()
    except ObjectManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    if len(reference_list) < 1:
        return make_response(rendered_reference_list, 204)
    return make_response(rendered_reference_list)


# CRUD routes

@object_rest.route('/', methods=['POST'])
@login_required
@insert_request_user
def insert_object(request_user):
    from bson import json_util
    from datetime import datetime
    add_data_dump = json.dumps(request.json)

    try:
        new_object_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
        new_object_data['public_id'] = object_manager.get_highest_id(CmdbObject.COLLECTION) + 1
        new_object_data['active'] = True
        new_object_data['creation_time'] = datetime.utcnow()
        new_object_data['last_edit_time'] = datetime.utcnow()
        new_object_data['views'] = 0
        new_object_data['version'] = '1.0.0'  # default init version
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)
    try:
        object_instance = CmdbObject(**new_object_data)
    except CMDBError as e:
        LOGGER.debug(e.message)
        return abort(400)
    try:
        new_object_id = object_manager.insert_object(object_instance)
    except ObjectInsertError:
        return abort(500)

    # Generate new insert log
    try:
        log_params = {
            'object_id': new_object_id,
            'user_id': request_user.get_public_id(),
            'user_name': request_user.get_name(),
            'comment': 'Object was created',
            'version': object_instance.version
        }
        log_ack = log_manager.insert_log(action=LogAction.CREATE, log_type=CmdbObjectLog.__name__, **log_params)
        LOGGER.debug(log_ack)
    except LogManagerInsertError as err:
        LOGGER.error(err)

    resp = make_response(new_object_id)
    return resp


@object_rest.route('/<int:public_id>/', methods=['PUT'])
@object_rest.route('/<int:public_id>', methods=['PUT'])
@login_required
@insert_request_user
def update_object(public_id: int, request_user: User):
    from cmdb.data_storage.database_utils import object_hook, default

    # get current object state
    try:
        current_object_instance = object_manager.get_object(public_id)
        current_type_instance = object_manager.get_type(current_object_instance.get_type_id())
        current_object_render_result = CmdbRender(object_instance=current_object_instance,
                                                  type_instance=current_type_instance,
                                                  render_user=request_user).result()
    except ObjectManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    except RenderError as err:
        LOGGER.error(err)
        return abort(500)

    update_comment = ''
    # load put data
    try:
        # get data as str
        add_data_dump = json.dumps(request.json)

        # convert into python dict
        put_data = json.loads(add_data_dump, object_hook=object_hook)
        # check for comment
        try:
            update_comment = put_data['comment']
            del put_data['comment']
        except (KeyError, IndexError, ValueError):
            update_comment = ''
    except TypeError as e:
        LOGGER.warning(e)
        return abort(400)

    # update edit time
    put_data['last_edit_time'] = datetime.utcnow()

    try:
        update_object_instance = CmdbObject(**put_data)
    except ObjectManagerUpdateError as err:
        LOGGER.error(err)
        return abort(400)

    # calc version

    changes = current_object_instance / update_object_instance

    if len(changes['new']) == 1:
        update_object_instance.update_version(update_object_instance.VERSIONING_PATCH)
    elif len(changes['new']) == len(update_object_instance.fields):
        update_object_instance.update_version(update_object_instance.VERSIONING_MAJOR)
    elif len(changes['new']) > (len(update_object_instance.fields) / 2):
        update_object_instance.update_version(update_object_instance.VERSIONING_MINOR)
    else:
        update_object_instance.update_version(update_object_instance.VERSIONING_PATCH)

    # insert object
    try:
        update_ack = object_manager.update_object(update_object_instance)
    except CMDBError as e:
        LOGGER.warning(e)
        return abort(500)

    try:
        # generate log
        log_data = {
            'object_id': public_id,
            'version': current_object_render_result.object_information['version'],
            'user_id': request_user.get_public_id(),
            'user_name': request_user.get_name(),
            'comment': update_comment,
            'changes': changes,
            'render_state': json.dumps(current_object_render_result, default=default).encode('UTF-8')
        }
        log_manager.insert_log(action=LogAction.EDIT, log_type=CmdbObjectLog.__name__, **log_data)
    except (CMDBError, LogManagerInsertError) as err:
        LOGGER.error(err)

    return make_response(update_ack)


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


# Special routes
@object_rest.route('/<int:public_id>/state/', methods=['GET'])
@object_rest.route('/<int:public_id>/state', methods=['GET'])
def get_object_state(public_id: int):
    try:
        founded_object = object_manager.get_object(public_id=public_id)
    except ObjectManagerGetError as err:
        LOGGER.debug(err)
        return abort(404)
    return make_response(founded_object.active)


@object_rest.route('/<int:public_id>/state/', methods=['PUT'])
@object_rest.route('/<int:public_id>/state', methods=['PUT'])
@insert_request_user
def update_object_state(public_id: int, request_user: User):
    if isinstance(request.json, bool):
        state = request.json
    else:
        return abort(400)
    try:
        founded_object = object_manager.get_object(public_id=public_id)
    except ObjectManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    if founded_object.active == state:
        return make_response(False, 204)
    try:
        founded_object.active = state
        update_ack = object_manager.update_object(founded_object)
    except ObjectManagerUpdateError as err:
        LOGGER.error(err)
        return abort(500)

    try:
        # generate log
        change = {
            'old': not state,
            'new': state
        }
        log_data = {
            'object_id': public_id,
            'version': founded_object.version,
            'user_id': request_user.get_public_id(),
            'user_name': request_user.get_name(),
            'comment': 'Active status has changed',
            'changes': change,
        }
        log_manager.insert_log(action=LogAction.ACTIVE_CHANGE, log_type=CmdbObjectLog.__name__, **log_data)
    except (CMDBError, LogManagerInsertError) as err:
        LOGGER.error(err)

    return make_response(update_ack)
