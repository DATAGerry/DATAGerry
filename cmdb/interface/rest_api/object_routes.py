# dataGerry - OpenSource Enterprise CMDB
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

from flask import abort
from cmdb.object_framework.cmdb_render import CmdbRender
from cmdb.object_framework.cmdb_object_manager import object_manager
from cmdb.utils.interface_wraps import login_required
from cmdb.interface.route_utils import make_response, RootBlueprint
from cmdb.user_management.user_manager import get_user_manager
usm = get_user_manager()

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
object_rest = RootBlueprint('object_rest', __name__, url_prefix='/object')


# DEFAULT ROUTES

@login_required
@object_rest.route('/', methods=['GET'])
def get_object_list():
    all_objects = []
    try:
        type_buffer_list = {}
        all_objects_list = object_manager.get_all_objects()
        for passed_object in all_objects_list:
            current_type = None
            passed_object_type_id = passed_object.get_type_id()
            if passed_object_type_id in type_buffer_list:
                current_type = type_buffer_list[passed_object_type_id]
            else:
                try:
                    current_type = object_manager.get_type(passed_object_type_id)
                    type_buffer_list.update({passed_object_type_id: current_type})
                except CMDBError as e:
                    continue
            tmp_render = CmdbRender(type_instance=current_type, object_instance=passed_object)
            all_objects.append(tmp_render)

    except CMDBError:
        return abort(400)

    resp = make_response(CmdbRender.result_loop_render(all_objects))
    return resp


@login_required
@object_rest.route('/native', methods=['GET'])
def get_native_object_list():
    try:
        object_list = object_manager.get_all_objects()
    except CMDBError:
        return abort(404)
    resp = make_response(object_list)
    return resp


@login_required
@object_rest.route('/<int:public_id>', methods=['GET'])
def get_object(public_id):
    try:
        object_instance = object_manager.get_object(public_id)
    except CMDBError:
        return make_response("error object", 404)

    try:
        type_instance = object_manager.get_type(object_instance.get_type_id())
    except CMDBError:
        return make_response("error type", 404)

    try:
        render = CmdbRender(object_instance=object_instance, type_instance=type_instance)
        render_result = render.result()
    except CMDBError:
        return make_response("render type", 404)

    resp = make_response(render_result)
    return resp


@login_required
@object_rest.route('<int:public_id>/native/', methods=['GET'])
def get_navtive_object(public_id: int):
    try:
        object_instance = object_manager.get_object(public_id)
    except CMDBError:
        return abort(404)
    resp = make_response(object_instance)
    return resp


@login_required
@object_rest.route('/by/<dict:requirements>', methods=['GET'])
def get_object_by(requirements):
    """TODO Implement"""
    requirements_dict = None
    try:
        pass  # requirements_dict = dict(requirements)
    except ValueError:
        return abort(400)
    resp = make_response(requirements_dict)
    return resp


@login_required
@object_rest.route('/', methods=['POST'])
def add_object():
    pass


@login_required
@object_rest.route('/<int:public_id>', methods=['PUT'])
def update_object(public_id):
    try:
        object_instance = object_manager.get_object(public_id)
    except CMDBError:
        return abort(404)
    resp = make_response(object_instance)
    return resp


@login_required
@object_rest.route('/<int:public_id>', methods=['DELETE'])
def delete_object(public_id):
    try:
        object_instance_ack = object_manager.delete_object(public_id)
    except CMDBError:
        return abort(400)
    resp = make_response(object_instance_ack)
    return resp


# SPECIAL ROUTES
@login_required
@object_rest.route('/newest/')
def get_newest_objects():
    type_buffer_list = {}
    newest_objects_list = object_manager.get_objects_by(sort='creation_time',
                                                        limit=25,
                                                        active={"$eq": True})
    newest_objects = []
    for passed_object in newest_objects_list:
        global current_type
        current_type = None
        passed_object_type_id = passed_object.get_type_id()
        if passed_object_type_id in type_buffer_list:
            current_type = type_buffer_list[passed_object_type_id]
        else:
            try:
                current_type = object_manager.get_type(passed_object_type_id)
                type_buffer_list.update({passed_object_type_id: current_type})
            except CMDBError as e:
                LOGGER.warning("Newest object type - error: {}".format(e.message))
                continue
        tmp_render = CmdbRender(type_instance=current_type, object_instance=passed_object)
        newest_objects.append(tmp_render)

    resp = make_response(CmdbRender.result_loop_render(newest_objects))
    return resp
