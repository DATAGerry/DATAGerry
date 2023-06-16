# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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

import logging

from werkzeug.exceptions import abort
from flask import current_app, request

from cmdb.framework.cmdb_errors import ObjectManagerGetError
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.managers.object_manager import ObjectManager
from cmdb.framework.models.log import CmdbObjectLog, CmdbMetaLog, LogAction
from cmdb.framework.managers.log_manager import CmdbLogManager
from cmdb.manager.errors import ManagerIterationError, ManagerGetError, ManagerDeleteError
from cmdb.interface.route_utils import make_response, insert_request_user

from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetMultiResponse
from cmdb.security.acl.errors import AccessDeniedError
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel

LOGGER = logging.getLogger(__name__)
log_blueprint = APIBlueprint('log', __name__)

with current_app.app_context():
    database_manager = current_app.database_manager
    object_manager = CmdbObjectManager(current_app.database_manager, current_app.event_queue)
    log_manager = CmdbLogManager(current_app.database_manager)


# CRUD routes
@log_blueprint.route('/<int:public_id>', methods=['GET'])
@log_blueprint.protect(auth=True, right='base.framework.log.view')
@insert_request_user
def get_log(public_id: int, request_user: UserModel):
    manager = CmdbLogManager(database_manager=database_manager)
    try:
        selected_log: CmdbObjectLog = manager.get(public_id=public_id)
        ObjectManager(database_manager=database_manager).get(selected_log.object_id, user=request_user,
                                                             permission=AccessControlPermission.READ)
    except ManagerGetError as err:
        return abort(404, err.message)
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


@log_blueprint.route('/<int:public_id>', methods=['DELETE'])
@log_blueprint.protect(auth=True, right='base.framework.log.delete')
@insert_request_user
def delete_log(public_id: int, request_user: UserModel):
    manager = CmdbLogManager(database_manager=database_manager)
    try:
        selected_log: CmdbObjectLog = manager.get(public_id=public_id)
        ObjectManager(database_manager=database_manager).get(selected_log.object_id, user=request_user,
                                                             permission=AccessControlPermission.DELETE)
        deleted_object = log_manager.delete(public_id=public_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    except AccessDeniedError as err:
        return abort(403, err.message)
    except ManagerDeleteError as err:
        return abort(500, err.message)
    return make_response(deleted_object, 202)


# FIND routes
@log_blueprint.route('/object/exists', methods=['GET', 'HEAD'])
@log_blueprint.protect(auth=True, right='base.framework.log.view')
@log_blueprint.parse_collection_parameters()
@insert_request_user
def get_logs_with_existing_objects(params: CollectionParameters, request_user: UserModel):
    try:
        query = []

        if isinstance(params.filter, dict):
            query.append({'$match': params.filter})
        elif isinstance(params.filter, list):
            for pipe in params.filter:
                query.append(pipe)

        query.append({'$match': {
            'log_type': CmdbObjectLog.__name__,
            'action': {
                '$ne': LogAction.DELETE.value
            }
        }})

        query.append({"$lookup": {
            "from": "framework.objects",
            "let": {"ref_id": "$object_id"},
            "pipeline": [{'$match': {'$expr': {'$eq': ["$public_id", '$$ref_id']}}}],
            "as": "object"
        }})
        query.append({'$unwind': {'path': '$object', 'preserveNullAndEmptyArrays': True}})
        query.append({'$match': {'object': {'$exists': True}}})

        body = request.method == 'HEAD'
        object_logs = log_manager.iterate(filter=query, limit=params.limit,
                                          skip=params.skip, sort=params.sort, order=params.order, user=request_user,
                                          permission=AccessControlPermission.READ)
        logs = [CmdbObjectLog.to_json(_) for _ in object_logs.results]
        api_response = GetMultiResponse(logs, total=object_logs.total, params=params,
                                        url=request.url, model=CmdbMetaLog.MODEL, body=body)

    except ManagerIterationError as err:
        return abort(400, err.message)
    except ObjectManagerGetError as err:
        LOGGER.error(f'Error in get_logs_with_existing_objects: {err}')
        return abort(404)
    return api_response.make_response()


@log_blueprint.route('/object/notexists', methods=['GET', 'HEAD'])
@log_blueprint.protect(auth=True, right='base.framework.log.view')
@log_blueprint.parse_collection_parameters()
def get_logs_with_deleted_objects(params: CollectionParameters):
    manager = CmdbLogManager(database_manager=database_manager)
    try:
        query = []

        if isinstance(params.filter, dict):
            query.append({'$match': params.filter})
        elif isinstance(params.filter, list):
            for pipe in params.filter:
                query.append(pipe)

        query.append({'$match': {
            'log_type': CmdbObjectLog.__name__,
            'action': {
                '$ne': LogAction.DELETE.value
            }
        }})

        query.append({"$lookup": {
            "from": "framework.objects",
            "let": {"ref_id": "$object_id"},
            "pipeline": [{'$match': {'$expr': {'$eq': ["$public_id", '$$ref_id']}}}],
            "as": "object"
        }})
        query.append({'$unwind': {'path': '$object', 'preserveNullAndEmptyArrays': True}})
        query.append({'$match': {'object': {'$exists': False}}})

        body = request.method == 'HEAD'
        object_logs = manager.iterate(filter=query, limit=params.limit,
                                          skip=params.skip, sort=params.sort, order=params.order)

        logs = [CmdbObjectLog.to_json(_) for _ in object_logs.results]
        api_response = GetMultiResponse(logs, total=object_logs.total, params=params,
                                        url=request.url, model=CmdbMetaLog.MODEL, body=body)

    except ManagerIterationError as err:
        return abort(400, err.message)
    except ObjectManagerGetError as err:
        LOGGER.error(f'Error in get_logs_with_deleted_objects: {err}')
        return abort(404)
    return api_response.make_response()


@log_blueprint.route('/object/deleted', methods=['GET', 'HEAD'])
@log_blueprint.protect(auth=True, right='base.framework.log.view')
@log_blueprint.parse_collection_parameters()
def get_object_delete_logs(params: CollectionParameters):
    manager = CmdbLogManager(database_manager=database_manager)
    try:
        query = {
            'log_type': CmdbObjectLog.__name__,
            'action': LogAction.DELETE.value
        }
        body = request.method == 'HEAD'
        object_logs = manager.iterate(filter=query, limit=params.limit, skip=params.skip,
                                          sort=params.sort, order=params.order)
        logs = [CmdbObjectLog.to_json(_) for _ in object_logs.results]
        api_response = GetMultiResponse(logs, total=object_logs.total, params=params,
                                        url=request.url, model=CmdbMetaLog.MODEL, body=body)

    except ManagerIterationError as err:
        return abort(400, err.message)
    except ObjectManagerGetError as err:
        LOGGER.error(f'Error in get_object_delete_logs: {err}')
        return abort(404)
    return api_response.make_response()


@log_blueprint.route('/object/<int:object_id>', methods=['GET', 'HEAD'])
@log_blueprint.protect(auth=True, right='base.framework.log.view')
@log_blueprint.parse_collection_parameters()
@insert_request_user
def get_logs_by_object(object_id: int, params: CollectionParameters, request_user: UserModel):
    manager = CmdbLogManager(database_manager=database_manager)
    try:
        ObjectManager(database_manager=database_manager).get(object_id, user=request_user,
                                                             permission=AccessControlPermission.READ)
        body = request.method == 'HEAD'
        iteration_result = manager.iterate(public_id=object_id, filter=params.filter, limit=params.limit,
                                           skip=params.skip, sort=params.sort, order=params.order)
        logs = [CmdbObjectLog.to_json(_) for _ in iteration_result.results]
        api_response = GetMultiResponse(logs, total=iteration_result.total, params=params,
                                        url=request.url, model=CmdbMetaLog.MODEL, body=body)
    except ManagerGetError as err:
        return abort(404, err.message)
    except AccessDeniedError as err:
        return abort(403, err.message)
    except ManagerIterationError as err:
        return abort(400, err.message)

    return api_response.make_response()


@log_blueprint.route('/<int:public_id>/corresponding', methods=['GET', 'HEAD'])
@log_blueprint.protect(auth=True, right='base.framework.log.view')
@insert_request_user
def get_corresponding_object_logs(public_id: int, request_user: UserModel):
    try:
        selected_log = log_manager.get(public_id=public_id)
        ObjectManager(database_manager=database_manager).get(selected_log.object_id, user=request_user,
                                                             permission=AccessControlPermission.READ)
        query = {
            'log_type': CmdbObjectLog.__name__,
            'object_id': selected_log.object_id,
            'action': LogAction.EDIT.value,
            '$nor': [{
                'public_id': public_id
            }]
        }
        logs = log_manager.iterate(filter=query, limit=0, skip=0, order=1, sort='public_id')
        corresponding_logs = [CmdbObjectLog.to_json(_) for _ in logs.results]
    except ManagerGetError as err:
        return abort(404, err.message)
    except AccessDeniedError as err:
        return abort(403, err.message)
    except ManagerIterationError as err:
        return abort(400, err.message)

    if len(corresponding_logs) < 1:
        return make_response(corresponding_logs, 204)

    return make_response(corresponding_logs)
