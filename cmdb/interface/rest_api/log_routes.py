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

from werkzeug.exceptions import abort
from flask import current_app

from cmdb.security.acl.errors import AccessDeniedError
from cmdb.framework.cmdb_errors import ObjectManagerGetError
from cmdb.framework.cmdb_log import CmdbObjectLog, LogAction
from cmdb.framework.cmdb_log_manager import LogManagerGetError, LogManagerDeleteError
from cmdb.interface.route_utils import make_response, login_required, right_required, insert_request_user
from cmdb.interface.blueprint import RootBlueprint
from cmdb.user_management import UserModel

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
log_blueprint = RootBlueprint('log_rest', __name__, url_prefix='/log')

with current_app.app_context():
    object_manager = current_app.object_manager
    log_manager = current_app.log_manager

# CRUD routes
@log_blueprint.route('/<int:public_id>/', methods=['GET'])
@log_blueprint.route('/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.log.view')
def get_log(public_id: int, request_user: UserModel):
    try:
        selected_log = log_manager.get_log(public_id=public_id, group_id=request_user.group_id)
    except LogManagerGetError:
        return abort(404)
    except AccessDeniedError as err:
        return abort(403, err.message)
    return make_response(selected_log)


@log_blueprint.route('/', methods=['POST'])
def insert_log(*args, **kwargs):
    """
    It is not planned to insert a log
    Returns:
        always a 405 Method Not Allowed	error
    """
    return abort(405)


@log_blueprint.route('/<int:public_id>/', methods=['PUT'])
@log_blueprint.route('/<int:public_id>', methods=['PUT'])
def update_log(public_id, *args, **kwargs):
    """
    It is not planned to update a log
    Returns:
        always a 405 Method Not Allowed	error
    """
    return abort(405)


@log_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@log_blueprint.route('/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.framework.log.delete')
def delete_log(public_id: int, request_user: UserModel):
    try:
        delete_ack = log_manager.delete_log(public_id=public_id)
    except LogManagerDeleteError as err:
        return abort(500)
    return make_response(delete_ack)


# FIND routes
@log_blueprint.route('/object/exists/', methods=['GET'])
@log_blueprint.route('/object/exists', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.log.view')
def get_logs_with_existing_objects(request_user: UserModel):
    existing_list = []
    deleted_list = []
    passed_objects = []
    location = 'type.acl.groups.includes.' + str(request_user.group_id)

    try:
        query = [
            {
                '$lookup':
                    {
                        'from': 'framework.objects',
                        'localField': 'object_id',
                        'foreignField': 'public_id',
                        'as': 'object'
                    }
            },
            {'$lookup':
                {
                    'from': 'framework.types',
                    'localField': 'object.0.type_id',
                    'foreignField': 'public_id',
                    'as': 'type'
                }
            },
            {'$unwind': {'path': '$type'}},
            {
                '$match':
                    {'$and': [
                        {'$or': [
                            {'$or': [{'type.acl': {'$exists': False}}, {'type.acl.activated': False}]},
                            {'$and': [
                                {'type.acl.activated': True},
                                {'$and': [
                                    {location: {'$exists': True}},
                                    {location: {'$in': ['READ']}}
                                ]},
                            ]}]
                        },
                        {
                            'log_type': CmdbObjectLog.__name__,
                            'action': {
                                '$ne': LogAction.DELETE.value
                            }
                        }]
                    }
            },
            {'$project': {'object': 0, 'type': 0}}
        ]
        object_logs = log_manager.get_logs_by(query)
    except ObjectManagerGetError as err:
        LOGGER.error(f'Error in get_logs_with_existing_objects: {err}')
        return abort(404)
    if len(object_logs) < 1:
        return make_response(object_logs, 204)
    for log in object_logs:
        current_object_id: int = log.object_id
        if current_object_id in existing_list:
            passed_objects.append(log)
            continue
        elif current_object_id in deleted_list:
            continue
        else:
            try:
                object_manager.get_object(current_object_id)
                existing_list.append(current_object_id)
                passed_objects.append(log)
            except ObjectManagerGetError:
                deleted_list.append(current_object_id)
                continue
    if len(passed_objects) < 1:
        return make_response(passed_objects, 204)
    return make_response(passed_objects)


@log_blueprint.route('/object/notexists/', methods=['GET'])
@log_blueprint.route('/object/notexists', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.log.view')
def get_logs_with_deleted_objects(request_user: UserModel):
    existing_list = []
    deleted_list = []
    passed_objects = []
    location = 'type.acl.groups.includes.' + str(request_user.group_id)
    try:
        query = [
            {
                '$lookup':
                    {
                        'from': 'framework.objects',
                        'localField': 'object_id',
                        'foreignField': 'public_id',
                        'as': 'object'
                    }
            },
            {'$lookup':
                {
                    'from': 'framework.types',
                    'localField': 'object.0.type_id',
                    'foreignField': 'public_id',
                    'as': 'type'
                }
            },
            {'$unwind': {'path': '$type'}},
            {
                '$match':
                    {'$and': [
                        {'$or': [
                            {'$or': [{'type.acl': {'$exists': False}}, {'type.acl.activated': False}]},
                            {'$and': [
                                {'type.acl.activated': True},
                                {'$and': [
                                    {location: {'$exists': True}},
                                    {location: {'$in': ['READ']}}
                                ]},
                            ]}]
                        },
                        {
                            'log_type': CmdbObjectLog.__name__,
                            'action': {
                                '$ne': LogAction.DELETE.value
                            }
                        }]
                    }
            },
            {'$project': {'object': 0, 'type': 0}}
        ]
        object_logs = log_manager.get_logs_by(query)
    except ObjectManagerGetError as err:
        LOGGER.error(f'Error in get_logs_with_existing_objects: {err}')
        return abort(404)
    if len(object_logs) < 1:
        return make_response(object_logs, 204)
    for log in object_logs:
        current_object_id: int = log.object_id
        if current_object_id in existing_list:
            continue
        elif current_object_id in deleted_list:
            passed_objects.append(log)
            continue
        else:
            try:
                object_manager.get_object(current_object_id)
                existing_list.append(current_object_id)
            except ObjectManagerGetError:
                deleted_list.append(current_object_id)
                passed_objects.append(log)
                continue
    if len(passed_objects) < 1:
        return make_response(passed_objects, 204)
    return make_response(passed_objects)


@log_blueprint.route('/object/deleted/', methods=['GET'])
@log_blueprint.route('/object/deleted', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.log.view')
def get_object_delete_logs(request_user: UserModel):
    try:
        location = 'type.acl.groups.includes.' + str(request_user.group_id)
        query = [
            {
                '$lookup':
                    {
                        'from': 'framework.objects',
                        'localField': 'object_id',
                        'foreignField': 'public_id',
                        'as': 'object'
                    }
            },
            {'$lookup':
                {
                    'from': 'framework.types',
                    'localField': 'object.0.type_id',
                    'foreignField': 'public_id',
                    'as': 'type'
                }
            },
            {'$unwind': {'path': '$type'}},
            {
                '$match':
                    {'$and': [
                        {'$or': [
                            {'$or': [{'type.acl': {'$exists': False}}, {'type.acl.activated': False}]},
                            {'$and': [
                                {'type.acl.activated': True},
                                {'$and': [
                                    {location: {'$exists': True}},
                                    {location: {'$in': ['READ']}}
                                ]},
                            ]}]
                        },
                        {
                            'log_type': CmdbObjectLog.__name__,
                            'action': LogAction.DELETE.value
                        }]
                    }
            },
            {'$project': {'object': 0, 'type': 0}}
        ]

        object_logs = log_manager.get_logs_by(query)
    except ObjectManagerGetError as err:
        LOGGER.error(f'Error in get_object_delete_logs: {err}')
        return abort(404)
    if len(object_logs) < 1:
        return make_response(object_logs, 204)

    return make_response(object_logs)


@log_blueprint.route('/object/<int:public_id>/', methods=['GET'])
@log_blueprint.route('/object/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.log.view')
def get_logs_by_objects(public_id: int, request_user: UserModel):
    try:
        object_logs = log_manager.get_object_logs(public_id=public_id)
    except ObjectManagerGetError as err:
        LOGGER.error(f'Error in get_logs_by_objects: {err}')
        return abort(404)
    if len(object_logs) < 1:
        return make_response(object_logs, 204)
    return make_response(object_logs)


@log_blueprint.route('/<int:public_id>/corresponding/', methods=['GET'])
@log_blueprint.route('/<int:public_id>/corresponding', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.log.view')
def get_corresponding_object_logs(public_id: int, request_user: UserModel):
    try:
        selected_log = log_manager.get_log(public_id=public_id, group_id=request_user.group_id)
        location = 'type.acl.groups.includes.' + str(request_user.group_id)
        query = [
            {
                '$lookup':
                    {
                        'from': 'framework.objects',
                        'localField': 'object_id',
                        'foreignField': 'public_id',
                        'as': 'object'
                    }
            },
            {'$lookup':
                {
                    'from': 'framework.types',
                    'localField': 'object.0.type_id',
                    'foreignField': 'public_id',
                    'as': 'type'
                }
            },
            {'$unwind': {'path': '$type'}},
            {
                '$match':
                    {'$and': [
                        {'$or': [
                            {'$or': [{'type.acl': {'$exists': False}}, {'type.acl.activated': False}]},
                            {'$and': [
                                {'type.acl.activated': True},
                                {'$and': [
                                    {location: {'$exists': True}},
                                    {location: {'$in': ['READ']}}
                                ]},
                            ]}]
                        },
                        {
                            'log_type': CmdbObjectLog.__name__,
                            'object_id': selected_log.object_id,
                            'action': LogAction.EDIT.value,
                            '$nor': [{
                                'public_id': public_id
                            }]
                        }]
                    }
            },
            {'$project': {'object': 0, 'type': 0}}
        ]

        LOGGER.debug(f'Corresponding query: {query}')
        corresponding_logs = log_manager.get_logs_by(query)
    except LogManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    LOGGER.debug(f'Corresponding logs: {corresponding_logs}')
    if len(corresponding_logs) < 1:
        return make_response(corresponding_logs, 204)

    return make_response(corresponding_logs)
