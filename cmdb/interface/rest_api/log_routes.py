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
from flask import current_app, request

from cmdb.framework.cmdb_errors import ObjectManagerGetError
from cmdb.framework.cmdb_log import CmdbObjectLog, CmdbMetaLog, LogAction
from cmdb.framework.cmdb_log_manager import LogManagerGetError, LogManagerDeleteError
from cmdb.manager.errors import ManagerIterationError
from cmdb.interface.route_utils import make_response


from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetMultiResponse

LOGGER = logging.getLogger(__name__)
log_blueprint = APIBlueprint('log', __name__)

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

with current_app.app_context():
    object_manager = current_app.object_manager
    log_manager = current_app.log_manager

# CRUD routes
@log_blueprint.route('/<int:public_id>/', methods=['GET'])
@log_blueprint.route('/<int:public_id>', methods=['GET'])
@log_blueprint.protect(auth=True, right='base.framework.log.view')
def get_log(public_id: int):
    try:
        selected_log = log_manager.get_log(public_id=public_id)
    except LogManagerGetError:
        return abort(404)
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
@log_blueprint.protect(auth=True, right='base.framework.log.delete')
def delete_log(public_id: int):
    try:
        delete_ack = log_manager.delete_log(public_id=public_id)
    except LogManagerDeleteError as err:
        return abort(500, err.message)
    return make_response(delete_ack)


# FIND routes
@log_blueprint.route('/object/exists/', methods=['GET'])
@log_blueprint.route('/object/exists', methods=['GET'])
@log_blueprint.protect(auth=True, right='base.framework.log.view')
@log_blueprint.parse_collection_parameters()
def get_logs_with_existing_objects(params: CollectionParameters):

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
                          "as": "logs"
                        }})
        query.append({'$unwind': {'path': '$logs', 'preserveNullAndEmptyArrays': True}})
        query.append({'$match': {'logs': {'$exists': True}}})

        body = request.method == 'HEAD'
        object_logs = log_manager.get_logs(filter=query, limit=params.limit,
                                           skip=params.skip, sort=params.sort, order=params.order)
        logs = [CmdbObjectLog.to_json(_) for _ in object_logs.results]
        api_response = GetMultiResponse(logs, total=object_logs.total, params=params,
                                        url=request.url, model=CmdbMetaLog.MODEL, body=body)

    except ManagerIterationError as err:
        return abort(400, err.message)
    except ObjectManagerGetError as err:
        LOGGER.error(f'Error in get_logs_with_existing_objects: {err}')
        return abort(404)
    return api_response.make_response()


@log_blueprint.route('/object/notexists/', methods=['GET'])
@log_blueprint.route('/object/notexists', methods=['GET'])
@log_blueprint.protect(auth=True, right='base.framework.log.view')
@log_blueprint.parse_collection_parameters()
def get_logs_with_deleted_objects(params: CollectionParameters):

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
            "as": "logs"
        }})
        query.append({'$unwind': {'path': '$logs', 'preserveNullAndEmptyArrays': True}})
        query.append({'$match': {'logs': {'$exists': False}}})

        body = request.method == 'HEAD'
        object_logs = log_manager.get_logs(filter=query, limit=params.limit,
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


@log_blueprint.route('/object/deleted/', methods=['GET'])
@log_blueprint.route('/object/deleted', methods=['GET'])
@log_blueprint.protect(auth=True, right='base.framework.log.view')
@log_blueprint.parse_collection_parameters()
def get_object_delete_logs(params: CollectionParameters):
    try:
        query = {
            'log_type': CmdbObjectLog.__name__,
            'action': LogAction.DELETE.value
        }
        body = request.method == 'HEAD'
        object_logs = log_manager.get_logs(filter=query, limit=params.limit, skip=params.skip,
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


@log_blueprint.route('/object/<int:public_id>/', methods=['GET'])
@log_blueprint.route('/object/<int:public_id>', methods=['GET'])
@log_blueprint.protect(auth=True, right='base.framework.log.view')
@log_blueprint.parse_collection_parameters()
def get_logs_by_objects(public_id: int, params: CollectionParameters):
    try:
        body = request.method == 'HEAD'
        iteration_result = log_manager.get_logs(public_id=public_id, filter=params.filter, limit=params.limit,
                                                skip=params.skip, sort=params.sort, order=params.order)
        logs = [CmdbObjectLog.to_json(_) for _ in iteration_result.results]
        api_response = GetMultiResponse(logs, total=iteration_result.total, params=params,
                                        url=request.url, model=CmdbMetaLog.MODEL, body=body)
    except ManagerIterationError as err:
        return abort(400, err.message)
    except ObjectManagerGetError as err:
        LOGGER.error(f'Error in get_logs_by_objects: {err}')
        return abort(404)
    return api_response.make_response()


@log_blueprint.route('/<int:public_id>/corresponding/', methods=['GET'])
@log_blueprint.route('/<int:public_id>/corresponding', methods=['GET'])
@log_blueprint.protect(auth=True, right='base.framework.log.view')
def get_corresponding_object_logs(public_id: int):
    try:
        selected_log = log_manager.get_log(public_id=public_id)
        query = {
            'log_type': CmdbObjectLog.__name__,
            'object_id': selected_log.object_id,
            'action': LogAction.EDIT.value,
            '$nor': [{
                'public_id': public_id
            }]
        }
        LOGGER.debug(f'Corresponding query: {query}')
        corresponding_logs = log_manager.get_logs(filter=query, limit=10, skip=0, order=1, sort='public_id')
    except LogManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    LOGGER.debug(f'Corresponding logs: {corresponding_logs}')
    if len(corresponding_logs.results) < 1:
        return make_response(corresponding_logs.results, 204)

    return make_response(corresponding_logs.results)
