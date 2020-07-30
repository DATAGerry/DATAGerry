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

from flask import abort, request, jsonify, current_app

from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.search.query.query_builder import QueryBuilder
from cmdb.user_management import User
from cmdb.interface.route_utils import make_response, login_required, insert_request_user, right_required
from cmdb.interface.blueprint import RootBlueprint
from cmdb.framework.cmdb_errors import TypeNotFoundError, TypeInsertError, ObjectDeleteError, ObjectManagerGetError, \
    ObjectManagerInitError
from cmdb.framework.cmdb_type import CmdbType

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
type_blueprint = RootBlueprint('type_blueprint', __name__, url_prefix='/type')

with current_app.app_context():
    object_manager: CmdbObjectManager = current_app.object_manager


@type_blueprint.route('/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.type.view')
def get_types(request_user: User):
    """Get all types as a list"""
    try:
        type_list = object_manager.get_all_types()
    except (ObjectManagerInitError, ObjectManagerGetError) as err:
        return abort(500, err.message)
    if len(type_list) == 0:
        return make_response(type_list, 204)
    return make_response(type_list)


@type_blueprint.route('/find/<path:regex>/', defaults={'regex_options': 'imsx'}, methods=['GET'])
@type_blueprint.route('/find/<path:regex>', defaults={'regex_options': 'imsx'}, methods=['GET'])
@type_blueprint.route('/find/<path:regex>/<path:regex_options>/', methods=['GET'])
@type_blueprint.route('/find/<path:regex>/<path:regex_options>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.type.view')
def find_types_by_name(regex: str, regex_options: str, request_user: User):
    query_builder = QueryBuilder()

    if not regex or (regex == '') or regex is None or len(regex) == 0:
        return abort(400, 'No valid selection parameter was passed!')

    if any(ro not in 'imsx' for ro in regex_options):
        return abort(400, 'No valid regex options!')

    query_name = query_builder.regex_('name', f'{regex}', regex_options)
    query_label = query_builder.regex_('label', f'{regex}', regex_options)
    query = query_builder.or_([query_name, query_label])

    try:
        type_list = object_manager.get_types_by(**query)
    except ObjectManagerInitError as err:
        return abort(500, err.message)
    except ObjectManagerGetError as err:
        return abort(400, err.message)

    if len(type_list) == 0:
        return make_response(type_list, 204)
    return make_response(type_list)


@type_blueprint.route('/<int:public_id>/', methods=['GET'])
@type_blueprint.route('/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.type.view')
def get_type(public_id: int, request_user: User):
    try:
        type_instance = object_manager.get_type(public_id)
    except ObjectManagerGetError as err:
        return abort(404, err.message)
    return make_response(type_instance)


@type_blueprint.route('/<string:name>/', methods=['GET'])
@type_blueprint.route('/<string:name>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.type.view')
def get_type_by_name(name: str, request_user: User):
    try:
        type_instance = object_manager.get_type_by(name=name)
    except ObjectManagerGetError as err:
        return abort(404, err.message)
    return make_response(type_instance)


@type_blueprint.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.framework.type.add')
def add_type(request_user: User):
    from bson import json_util
    from datetime import datetime
    add_data_dump = json.dumps(request.json)
    try:
        new_type_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
        new_type_data['public_id'] = object_manager.get_new_id(CmdbType.COLLECTION)
        new_type_data['creation_time'] = datetime.utcnow()
    except TypeError as e:
        LOGGER.warning(e)
        return abort(400)
    try:
        type_instance = CmdbType(**new_type_data)
    except CMDBError as e:
        LOGGER.debug(e)
        return abort(400)
    try:
        ack = object_manager.insert_type(type_instance)
    except TypeInsertError:
        return abort(500)

    resp = make_response(ack)
    return resp


@type_blueprint.route('/', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.framework.type.edit')
def update_type(request_user: User):
    from bson import json_util
    add_data_dump = json.dumps(request.json)
    try:
        new_type_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)
    try:
        update_type_instance = CmdbType(**new_type_data)
    except CMDBError:
        return abort(400)
    try:
        old_fields = object_manager.get_type(update_type_instance.get_public_id()).get_fields()
        new_fields = update_type_instance.get_fields()
        if [item for item in old_fields if item not in new_fields]:
            update_type_instance.clean_db = False
        if [item for item in new_fields if item not in old_fields]:
            update_type_instance.clean_db = False
    except CMDBError:
        return abort(500)
    try:
        object_manager.update_type(update_type_instance)
    except CMDBError:
        return abort(500)

    resp = make_response(update_type_instance)
    return resp


@type_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@type_blueprint.route('/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.framework.type.delete')
def delete_type(public_id: int, request_user: User):
    try:
        # delete all objects by typeID
        obj_ids = []
        objs_by_type = object_manager.get_objects_by_type(public_id)
        for objID in objs_by_type:
            obj_ids.append(objID.get_public_id())
        object_manager.delete_many_objects({'type_id': public_id}, obj_ids, request_user)

        ack = object_manager.delete_type(public_id=public_id)
    except User as e:
        return abort(400, f'Type with Public ID: {public_id} was not found!: {e}')
    return make_response(ack)


@type_blueprint.route('/delete/<string:public_ids>/', methods=['GET'])
@type_blueprint.route('/delete/<string:public_ids>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.type.delete')
def delete_many_types(public_ids, request_user: User):
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

        ack = object_manager.delete_many_types(filter_public_ids, ids)
        return make_response(ack.raw_result)
    except TypeNotFoundError as e:
        return jsonify(message='Delete Error', error=e.message)
    except ObjectDeleteError as e:
        return jsonify(message='Delete Error', error=e.message)
    except CMDBError:
        return abort(500)


@type_blueprint.route('/count/', methods=['GET'])
@type_blueprint.route('/count', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.type.view')
def count_types(request_user: User):
    try:
        count = object_manager.count_types()
        resp = make_response(count)
    except CMDBError:
        return abort(400)
    return resp


@type_blueprint.route('/category/<int:public_id>/', methods=['GET'])
@type_blueprint.route('/category/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.type.view')
def get_types_by_category(public_id, request_user: User):
    try:
        category = object_manager.get_category(public_id=public_id)
    except ObjectManagerGetError as err:
        return abort(404, err.message)
    if category.get_number_of_types() == 0:
        return make_response([], 204)

    type_ids = category.get_types()
    try:
        type_list = object_manager.get_types_by(public_id={'$in': type_ids})
    except ObjectManagerGetError as err:
        return abort(404, err.message)
    return make_response(type_list)


@type_blueprint.route('/uncategorized/', methods=['GET'])
@type_blueprint.route('/uncategorized', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.type.view')
def get_uncategorized_types(request_user: User):
    categories = object_manager.get_all_categories()
    types = object_manager.get_all_types()

    categorized_types = []
    for category in categories:
        categorized_types += category.types

    uncategorized_types = [type_ for type_ in types if type_.get_public_id() not in categorized_types]

    return make_response(uncategorized_types)


@type_blueprint.route('/cleanup/remove/<int:public_id>/', methods=['GET'])
@type_blueprint.route('/cleanup/remove/<int:public_id>', methods=['GET'])
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


@type_blueprint.route('/cleanup/update/<int:public_id>/', methods=['GET'])
@type_blueprint.route('/cleanup/update/<int:public_id>', methods=['GET'])
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
