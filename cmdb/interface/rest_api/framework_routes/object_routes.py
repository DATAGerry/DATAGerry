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

import copy
import json
import logging
import pytz

from datetime import datetime
from bson import json_util

from flask import abort, jsonify, request, current_app

from cmdb.data_storage.database_utils import object_hook, default
from cmdb.framework import CmdbObject
from cmdb.framework.cmdb_errors import ObjectDeleteError, ObjectInsertError, ObjectManagerGetError, \
    ObjectManagerUpdateError
from cmdb.framework.cmdb_log import LogAction, CmdbObjectLog
from cmdb.framework.cmdb_log_manager import LogManagerInsertError
from cmdb.framework.cmdb_render import CmdbRender, RenderList, RenderError
from cmdb.interface.route_utils import make_response, insert_request_user, login_required, right_required
from cmdb.interface.blueprint import RootBlueprint
from cmdb.user_management import User

with current_app.app_context():
    object_manager = current_app.object_manager
    log_manager = current_app.log_manager
    user_manager = current_app.user_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
object_blueprint = RootBlueprint('object_blueprint', __name__, url_prefix='/object')
with current_app.app_context():
    from cmdb.interface.rest_api.framework_routes.object_link_routes import link_rest

    object_blueprint.register_nested_blueprint(link_rest)


# DEFAULT ROUTES

@object_blueprint.route('/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_object_list(request_user: User):
    """
    get all objects in database
    Args:
        request_user: auto inserted user who made the request.
    Returns:
        list of rendered objects
    """
    try:
        filter_state = {'sort': 'public_id'}
        if _fetch_only_active_objs():
            filter_state['active'] = {"$eq": True}

        object_list = object_manager.get_objects_by(**filter_state)

        if request.args.get('start') is not None:
            start = int(request.args.get('start'))
            length = int(request.args.get('length'))
            object_list = object_list[start:start + length]

    except ObjectManagerGetError as err:
        LOGGER.error(err.message)
        return abort(404)
    if len(object_list) < 1:
        return make_response(object_list, 204)

    rendered_list = RenderList(object_list, request_user).render_result_list()

    return make_response(rendered_list)


@object_blueprint.route('/native', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_native_object_list(request_user: User):
    try:
        object_list = object_manager.get_all_objects()
    except CMDBError:
        return abort(404)
    resp = make_response(object_list)
    return resp


@object_blueprint.route('/dt/type/<int:type_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_dt_objects_by_type(type_id, request_user: User):
    """Return all objects by type_id"""
    try:
        table_config = request.args
        filter_state = {'type_id': type_id}

        if _fetch_only_active_objs():
            filter_state['active'] = {"$eq": True}

        start_at = int(table_config.get('start'))
        site_length = int(table_config.get('length'))
        order_column = table_config.get('order') if table_config.get('order') else 'type_id'
        order_direction = 1 if table_config.get('direction') == 'asc' else -1

        if order_column in ['active', 'public_id', 'type_id', 'author_id', 'creation_time']:
            object_list = object_manager.get_objects_by(sort=order_column, direction=order_direction, **filter_state)
        else:
            object_list = object_manager.sort_objects_by_field_value(value=order_column, order=order_direction,
                                                                     match=filter_state)
        totals = len(object_list)
        object_list = object_list[start_at:start_at + site_length]

    except CMDBError:
        return abort(400)

    rendered_list = RenderList(object_list, request_user, dt_render=True).render_result_list()

    table_response = {
        'data': rendered_list,
        'recordsTotal': totals,
        'recordsFiltered': totals
    }
    return make_response(table_response)


@object_blueprint.route('/dt/filter/type/<int:type_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_dt_filter_objects_by_type(type_id, request_user: User):
    """Return all objects by type_id"""
    try:
        table_config = request.args

        filter_ids = table_config.getlist('idList')
        start_at = int(table_config.get('start', 0, int))
        site_length = int(table_config.get('length', 10, int))
        search_for = table_config.get('search', '', str)
        order_column = table_config.get('order', 'type_id', str)
        order_direction = 1 if table_config.get('direction') == 'asc' else -1
        dt_render = False if table_config.get('dtRender') == 'false' else True

        # Prepare search term
        if search_for in ['true', 'True']:
            search_for = True
        elif search_for in ['false', 'False']:
            search_for = False
        elif search_for.isdigit():
            search_for = int(search_for)

        # Filter Objects by IDS
        filter_arg = []
        if filter_ids:
            filter_arg.append({'public_id': {'$in': list(map(int, filter_ids))}})

        # Search default values
        filter_arg.append({'type_id': type_id})
        if _fetch_only_active_objs():
            filter_arg.append({'active': {"$eq": True}})

        # Search search term over entire object
        or_conditions = []
        if not isinstance(search_for, bool):
            search_term = {'$regex': str(search_for), '$options': 'i'}
        else:
            search_term = search_for

        or_conditions.append({'fields': {'$elemMatch': {'value': search_term}}})
        # ToDo: Find - convert string to date
        # or_conditions.append({'creation_time': {'$toDate': str(search_for)}})

        if isinstance(search_for, int) and not isinstance(search_for, bool):
            if order_column in ['public_id', 'author_id']:
                or_conditions.append({'$where': "this.public_id.toString().includes(%s)" % search_for})
                or_conditions.append({'$where': "this.author_id.toString().includes(%s)" % search_for})
            else:
                or_conditions.append({'public_id': search_for})
                or_conditions.append({'author_id': search_for})

        # Linking queries
        filter_arg.append({'$or': or_conditions})
        filter_state = {'$and': filter_arg}

        if order_column in ['active', 'public_id', 'type_id', 'author_id', 'creation_time']:
            object_list = object_manager.get_objects_by(sort=order_column, direction=order_direction, **filter_state)
        else:
            object_list = object_manager.sort_objects_by_field_value(value=order_column, order=order_direction,
                                                                     match=filter_state)
        totals = len(object_list)
        object_list = object_list[start_at:start_at + site_length]

    except CMDBError:
        return abort(400)

    rendered_list = RenderList(object_list, request_user, dt_render=dt_render).render_result_list()

    table_response = {
        'data': rendered_list,
        'recordsTotal': totals,
        'recordsFiltered': totals
    }
    return make_response(table_response)


@object_blueprint.route('/type/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_objects_by_type(public_id, request_user: User):
    """Return all objects by type_id"""
    try:
        filter_state = {'type_id': public_id}
        if _fetch_only_active_objs():
            filter_state['active'] = {"$eq": True}

        object_list = object_manager.get_objects_by(sort="type_id", **filter_state)
    except CMDBError:
        return abort(400)

    if request.args.get('start') is not None:
        start = int(request.args.get('start'))
        length = int(request.args.get('length'))
        object_list = object_list[start:start + length]

    if len(object_list) < 1:
        return make_response(object_list, 204)

    rendered_list = RenderList(object_list, request_user).render_result_list()
    resp = make_response(rendered_list)
    return resp


@object_blueprint.route('/type/<string:type_ids>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_objects_by_types(type_ids, request_user: User):
    """Return all objects by type_id"""
    try:
        in_types = {'type_id': {'$in': list(map(int, type_ids.split(',')))}}
        is_active = {'active': {"$eq": False}}
        if _fetch_only_active_objs:
            is_active = {'active': {"$eq": True}}
        query = {'$and': [in_types, is_active]}

        all_objects_list = object_manager.get_objects_by(sort="type_id", **query)
        rendered_list = RenderList(all_objects_list, request_user).render_result_list()

    except CMDBError:
        return abort(400)

    resp = make_response(rendered_list)
    return resp


@object_blueprint.route('/many/<string:public_ids>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_objects_by_public_id(public_ids, request_user: User):
    """Return all objects by public_ids"""

    try:
        filter_state = {'public_id': public_ids}
        query = _build_query(filter_state, q_operator='$or')
        all_objects_list = object_manager.get_objects_by(sort="public_id", **query)
        rendered_list = RenderList(all_objects_list, request_user).render_result_list()

    except CMDBError:
        return abort(400)

    resp = make_response(rendered_list)
    return resp


@object_blueprint.route('/count/<int:type_id>', methods=['GET'])
@login_required
def count_object_by_type(type_id):
    try:
        count = object_manager.count_objects_by_type(type_id)
        if _fetch_only_active_objs():
            filter_state = {'type_id': type_id, 'active': {'$eq': True}}
            result = []
            cursor = object_manager.group_objects_by_value('active', filter_state)
            for document in cursor:
                result.append(document)
            count = result[0]['count'] if result else 0

        resp = make_response(count)
    except CMDBError:
        return abort(400)
    return resp


@object_blueprint.route('/count/', methods=['GET'])
@login_required
def count_objects():
    try:
        count = object_manager.count_objects()
        if _fetch_only_active_objs():
            result = []
            cursor = object_manager.group_objects_by_value('active', {'active': {"$eq": True}})
            for document in cursor:
                result.append(document)
            count = result[0]['count'] if result else 0
        resp = make_response(count)
    except CMDBError:
        return abort(400)
    return resp


@object_blueprint.route('/group/<string:value>', methods=['GET'])
@login_required
def group_objects_by_type_id(value):
    try:
        filter_state = None
        if _fetch_only_active_objs():
            filter_state = {'active': {"$eq": True}}
        result = []
        cursor = object_manager.group_objects_by_value(value, filter_state)
        max_length = 0
        for document in cursor:
            document['label'] = object_manager.get_type(document['_id']).label
            result.append(document)
            max_length += 1
            if max_length == 5:
                break
        resp = make_response(result)
    except CMDBError:
        return abort(400)
    return resp


@object_blueprint.route('/<int:public_id>/', methods=['GET'])
@object_blueprint.route('/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
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
        render = CmdbRender(object_instance=object_instance, type_instance=type_instance, render_user=request_user,
                            user_list=user_manager.get_users())
        render_result = render.result()
    except RenderError as err:
        LOGGER.error(err)
        return abort(500)

    resp = make_response(render_result)
    return resp


@object_blueprint.route('<int:public_id>/native/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_native_object(public_id: int, request_user: User):
    try:
        object_instance = object_manager.get_object(public_id)
    except CMDBError:
        return abort(404)
    resp = make_response(object_instance)
    return resp


@object_blueprint.route('/reference/<int:public_id>/', methods=['GET'])
@object_blueprint.route('/reference/<int:public_id>', methods=['GET'])
@insert_request_user
def get_objects_by_reference(public_id: int, request_user: User):
    try:
        active_flag = None
        if _fetch_only_active_objs():
            active_flag = True

        reference_list: list = object_manager.get_object_references(public_id=public_id, active_flag=active_flag)
        rendered_reference_list = RenderList(reference_list, request_user).render_result_list()
    except ObjectManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    if len(reference_list) < 1:
        return make_response(rendered_reference_list, 204)
    return make_response(rendered_reference_list)


@object_blueprint.route('/user/<int:public_id>/', methods=['GET'])
@object_blueprint.route('/user/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_objects_by_user(public_id: int, request_user: User):
    try:
        object_list = object_manager.get_objects_by(sort="type_id", author_id=public_id)
    except ObjectManagerGetError as err:
        LOGGER.error(err)
        return abort(400)

    if len(object_list) < 1:
        return make_response(object_list, 204)

    rendered_list = RenderList(object_list, request_user).render_result_list()
    return make_response(rendered_list)


@object_blueprint.route('/user/new/<int:timestamp>/', methods=['GET'])
@object_blueprint.route('/user/new/<int:timestamp>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_new_objects_since(timestamp: int, request_user: User):
    request_date = datetime.fromtimestamp(timestamp, pytz.utc)
    query = {
        'creation_time': {
            '$gt': request_date
        }
    }
    try:
        object_list = object_manager.get_objects_by(sort="creation_time", **query)
    except ObjectManagerGetError as err:
        LOGGER.error(err)
        return abort(400)

    if len(object_list) < 1:
        return make_response(object_list, 204)

    rendered_list = RenderList(object_list, request_user).render_result_list()
    return make_response(rendered_list)


@object_blueprint.route('/user/changed/<int:timestamp>/', methods=['GET'])
@object_blueprint.route('/user/changed/<int:timestamp>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_changed_objects_since(timestamp: int, request_user: User):
    request_date = datetime.fromtimestamp(timestamp, pytz.utc)
    query = {
        'last_edit_time': {
            '$gt': request_date,
            '$ne': None
        }
    }
    try:
        object_list = object_manager.get_objects_by(sort="creation_time", **query)
    except ObjectManagerGetError as err:
        LOGGER.error(err)
        return abort(400)

    if len(object_list) < 1:
        return make_response(object_list, 204)

    rendered_list = RenderList(object_list, request_user).render_result_list()
    return make_response(rendered_list)


# CRUD routes

@object_blueprint.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.framework.object.add')
def insert_object(request_user: User):
    from bson import json_util
    from datetime import datetime
    add_data_dump = json.dumps(request.json)

    try:
        new_object_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
        if not 'public_id' in new_object_data:
            new_object_data['public_id'] = object_manager.get_new_id(CmdbObject.COLLECTION)
        if not 'active' in new_object_data:
            new_object_data['active'] = True
        new_object_data['creation_time'] = datetime.utcnow()
        new_object_data['views'] = 0
        new_object_data['version'] = '1.0.0'  # default init version
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)

    try:
        new_object_id = object_manager.insert_object(new_object_data)
    except ObjectInsertError as oie:
        LOGGER.error(oie)
        return abort(500)

    # get current object state
    try:
        current_type_instance = object_manager.get_type(new_object_data['type_id'])
        current_object = object_manager.get_object(new_object_id)
        current_object_render_result = CmdbRender(object_instance=current_object,
                                                  type_instance=current_type_instance,
                                                  render_user=request_user,
                                                  user_list=user_manager.get_users()).result()
    except ObjectManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    except RenderError as err:
        LOGGER.error(err)
        return abort(500)

    # Generate new insert log
    try:
        log_params = {
            'object_id': new_object_id,
            'user_id': request_user.get_public_id(),
            'user_name': request_user.get_name(),
            'comment': 'Object was created',
            'render_state': json.dumps(current_object_render_result, default=default).encode('UTF-8'),
            'version': current_object.version
        }
        log_ack = log_manager.insert_log(action=LogAction.CREATE, log_type=CmdbObjectLog.__name__, **log_params)
    except LogManagerInsertError as err:
        LOGGER.error(err)

    resp = make_response(new_object_id)
    return resp


@object_blueprint.route('/<int:public_id>/', methods=['PUT'])
@object_blueprint.route('/<int:public_id>', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.framework.object.edit')
def update_object(public_id: int, request_user: User):
    object_ids = request.args.getlist('objectIDs')

    if len(object_ids) > 0:
        object_ids = list(map(int, object_ids))
    else:
        object_ids = [public_id]

    update_ack = None

    for obj_id in object_ids:
        # get current object state
        try:
            current_object_instance = object_manager.get_object(obj_id)
            current_type_instance = object_manager.get_type(current_object_instance.get_type_id())
            current_object_render_result = CmdbRender(object_instance=current_object_instance,
                                                      type_instance=current_type_instance,
                                                      render_user=request_user,
                                                      user_list=user_manager.get_users()).result()
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
                put_data['public_id'] = obj_id
                put_data['creation_time'] = current_object_instance.creation_time
                put_data['author_id'] = current_object_instance.author_id

                old_fields = list(map(lambda x: {k: v for k, v in x.items() if k in ['name', 'value']},
                                      current_type_instance.get_fields()))
                new_fields = put_data['fields']
                for item in new_fields:
                    for old in old_fields:
                        if item['name'] == old['name']:
                            old['value'] = item['value']
                put_data['fields'] = old_fields

                if 'active' not in put_data:
                    put_data['active'] = current_object_instance.active
                if 'version' not in put_data:
                    put_data['version'] = current_object_instance.version

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
            update_ack = object_manager.update_object(update_object_instance, request_user)
        except CMDBError as e:
            LOGGER.warning(e)
            return abort(500)

        try:
            # generate log
            log_data = {
                'object_id': obj_id,
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


@object_blueprint.route('/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.framework.object.delete')
def delete_object(public_id: int, request_user: User):
    try:
        current_object_instance = object_manager.get_object(public_id)
        current_type_instance = object_manager.get_type(current_object_instance.get_type_id())
        current_object_render_result = CmdbRender(object_instance=current_object_instance,
                                                  type_instance=current_type_instance,
                                                  render_user=request_user,
                                                  user_list=user_manager.get_users()).result()
    except ObjectManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    except RenderError as err:
        LOGGER.error(err)
        return abort(500)

    try:
        ack = object_manager.delete_object(public_id=public_id, request_user=request_user)
    except ObjectDeleteError:
        return abort(400)
    except CMDBError:
        return abort(500)

    try:
        # generate log
        log_data = {
            'object_id': public_id,
            'version': current_object_render_result.object_information['version'],
            'user_id': request_user.get_public_id(),
            'user_name': request_user.get_name(),
            'comment': 'Object was deleted',
            'render_state': json.dumps(current_object_render_result, default=default).encode('UTF-8')
        }
        log_manager.insert_log(action=LogAction.DELETE, log_type=CmdbObjectLog.__name__, **log_data)
    except (CMDBError, LogManagerInsertError) as err:
        LOGGER.error(err)

    resp = make_response(ack)
    return resp


@object_blueprint.route('/delete/<string:public_ids>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.delete')
def delete_many_objects(public_ids, request_user: User):
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

        ack = []
        objects = object_manager.get_objects_by(**filter_public_ids)

        for current_object_instance in objects:
            try:
                current_type_instance = object_manager.get_type(current_object_instance.get_type_id())
                current_object_render_result = CmdbRender(object_instance=current_object_instance,
                                                          type_instance=current_type_instance,
                                                          render_user=request_user,
                                                          user_list=user_manager.get_users()).result()
            except ObjectManagerGetError as err:
                LOGGER.error(err)
                return abort(404)
            except RenderError as err:
                LOGGER.error(err)
                return abort(500)

            try:
                ack.append(object_manager.delete_object(public_id=current_object_instance.get_public_id(),
                                                        request_user=request_user))
            except ObjectDeleteError:
                return abort(400)
            except CMDBError:
                return abort(500)

            try:
                # generate log
                log_data = {
                    'object_id': current_object_instance.get_public_id(),
                    'version': current_object_render_result.object_information['version'],
                    'user_id': request_user.get_public_id(),
                    'user_name': request_user.get_name(),
                    'comment': 'Object was deleted',
                    'render_state': json.dumps(current_object_render_result, default=default).encode('UTF-8')
                }
                log_manager.insert_log(action=LogAction.DELETE, log_type=CmdbObjectLog.__name__, **log_data)
            except (CMDBError, LogManagerInsertError) as err:
                LOGGER.error(err)

        resp = make_response({'successfully': ack})
        return resp

    except ObjectDeleteError as e:
        return jsonify(message='Delete Error', error=e.message)
    except CMDBError:
        return abort(500)


# Special routes
@object_blueprint.route('/<int:public_id>/state/', methods=['GET'])
@object_blueprint.route('/<int:public_id>/state', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.activation')
def get_object_state(public_id: int, request_user: User):
    try:
        founded_object = object_manager.get_object(public_id=public_id)
    except ObjectManagerGetError as err:
        LOGGER.debug(err)
        return abort(404)
    return make_response(founded_object.active)


@object_blueprint.route('/<int:public_id>/state/', methods=['PUT'])
@object_blueprint.route('/<int:public_id>/state', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.framework.object.activation')
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
        update_ack = object_manager.update_object(founded_object, request_user)
    except ObjectManagerUpdateError as err:
        LOGGER.error(err)
        return abort(500)

        # get current object state
    try:
        current_type_instance = object_manager.get_type(founded_object.get_type_id())
        current_object_render_result = CmdbRender(object_instance=founded_object,
                                                  type_instance=current_type_instance,
                                                  render_user=request_user,
                                                  user_list=user_manager.get_users()).result()
    except ObjectManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    except RenderError as err:
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
            'render_state': json.dumps(current_object_render_result, default=default).encode('UTF-8'),
            'comment': 'Active status has changed',
            'changes': change,
        }
        log_manager.insert_log(action=LogAction.ACTIVE_CHANGE, log_type=CmdbObjectLog.__name__, **log_data)
    except (CMDBError, LogManagerInsertError) as err:
        LOGGER.error(err)

    return make_response(update_ack)


# SPECIAL ROUTES
@object_blueprint.route('/newest', methods=['GET'])
@object_blueprint.route('/newest/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_newest(request_user: User):
    """
    get object with newest creation time
    Args:
        request_user: auto inserted user who made the request.
    Returns:
        list of rendered objects
    """
    newest_objects_list = object_manager.get_objects_by(sort='creation_time',
                                                        limit=25,
                                                        active={"$eq": True},
                                                        creation_time={'$ne': None})
    rendered_list = RenderList(newest_objects_list, request_user).render_result_list()
    if len(rendered_list) < 1:
        return make_response(rendered_list, 204)
    return make_response(rendered_list)


@object_blueprint.route('/latest', methods=['GET'])
@object_blueprint.route('/latest/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_latest(request_user: User):
    """
    get object with newest last edit time
    Args:
        request_user: auto inserted user who made the request.
    Returns:
        list of rendered objects
    """
    last_objects_list = object_manager.get_objects_by(sort='last_edit_time',
                                                      limit=25,
                                                      active={"$eq": True},
                                                      last_edit_time={'$ne': None})
    rendered_list = RenderList(last_objects_list, request_user).render_result_list()
    if len(rendered_list) < 1:
        return make_response(rendered_list, 204)
    return make_response(rendered_list)


@object_blueprint.route('/cleanup/remove/<int:public_id>/', methods=['GET'])
@object_blueprint.route('/cleanup/remove/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.type.clean')
def cleanup_removed_fields(public_id, request_user: User):
    # REMOVE fields from CmdbObject
    try:
        update_type_instance = object_manager.get_type(public_id)
        type_fields = update_type_instance.get_fields()
        objects_by_type = object_manager.get_objects_by_type(public_id)

        for obj in objects_by_type:
            incorrect = []
            correct = []
            obj_fields = obj.get_all_fields()
            for t_field in type_fields:
                name = t_field["name"]
                for field in obj_fields:
                    if name == field["name"]:
                        correct.append(field["name"])
                    else:
                        incorrect.append(field["name"])
            removed_type_fields = [item for item in incorrect if not item in correct]
            for field in removed_type_fields:
                object_manager.remove_object_fields(filter_query={'public_id': obj.public_id},
                                                    update={'$pull': {'fields': {"name": field}}})

    except Exception as error:
        return abort(500)

    return make_response(update_type_instance)


@object_blueprint.route('/cleanup/update/<int:public_id>/', methods=['GET'])
@object_blueprint.route('/cleanup/update/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.type.clean')
def cleanup_updated_push_fields(public_id, request_user: User):
    # Update/Push fields to CmdbObject
    try:
        update_type_instance = object_manager.get_type(public_id)
        type_fields = update_type_instance.get_fields()
        objects_by_type = object_manager.get_objects_by_type(public_id)

        for obj in objects_by_type:
            for t_field in type_fields:
                name = t_field["name"]
                value = None
                if [item for item in obj.get_all_fields() if item["name"] == name]:
                    continue
                if "value" in t_field:
                    value = t_field["value"]
                object_manager.update_object_fields(filter={'public_id': obj.public_id},
                                                    update={
                                                        '$addToSet': {'fields': {"name": name, "value": value}}})
    except CMDBError:
        return abort(500)

    return make_response(update_type_instance)


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


def _fetch_only_active_objs() -> bool:
    """
        Checking if request have cookie parameter for object active state
        Returns:
            True if cookie is set or value is true else false
        """
    if request.args.get('onlyActiveObjCookie') is not None:
        value = request.args.get('onlyActiveObjCookie')
        if value in ['True', 'true']:
            return True
    return False
