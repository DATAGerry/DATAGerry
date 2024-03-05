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
"""Definition of all routes for Logs"""
import logging

from flask import current_app, request

from cmdb.framework.managers.object_manager import ObjectManager
from cmdb.manager.logs_manager import LogsManager

from cmdb.framework.models.log import CmdbObjectLog, CmdbMetaLog, LogAction
from cmdb.interface.route_utils import make_response
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetMultiResponse, ErrorBody

from cmdb.errors.manager import ManagerIterationError, ManagerGetError, ManagerDeleteError

from cmdb.manager.query_builder.builder_parameters import BuilderParameters
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)
logs_blueprint = APIBlueprint('logs', __name__)

with current_app.app_context():
    logs_manager = LogsManager(current_app.database_manager, current_app.event_queue)
    object_manager = ObjectManager(current_app.database_manager, current_app.event_queue)

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@logs_blueprint.route('/<int:public_id>', methods=['GET'])
@logs_blueprint.protect(auth=True, right='base.framework.log.view')
def get_log(public_id: int):
    """
    Retrives a single log from the database

    Args:
        public_id (int): public_id of the requested log
    Returns:
        CmdbObjectLog: The log with the given public_id
    """
    try:
        requested_log: CmdbObjectLog = logs_manager.get_one(public_id)
    except ManagerGetError:
        return ErrorBody(404, "Could not retrieve the requested log from database!").response()

    return make_response(requested_log)


@logs_blueprint.route('/object/exists', methods=['GET', 'HEAD'])
@logs_blueprint.protect(auth=True, right='base.framework.log.view')
@logs_blueprint.parse_collection_parameters()
def get_logs_with_existing_objects(params: CollectionParameters):
    """
    Retrieves all logs of objects which still exist

    Args:
        params (CollectionParameters): parameters for query
    Returns:
        GetMultiResponse: with all logs of exisiting objects
    """
    try:
        query = logs_manager.query_builder.prepare_log_query()

        builder_params = BuilderParameters(query, params.limit, params.skip, params.sort, params.order)

        object_logs = logs_manager.iterate(builder_params)

        logs = [CmdbObjectLog.to_json(_) for _ in object_logs.results]

        api_response = GetMultiResponse(logs,
                                        object_logs.total,
                                        params,
                                        request.url,
                                        CmdbMetaLog.MODEL,
                                        request.method == 'HEAD')

    except ManagerIterationError as err:
        LOGGER.debug("ManagerIterationError: %s", err)
        return ErrorBody(400, "Could not retrieve existing object logs from database!").response()

    return api_response.make_response()


@logs_blueprint.route('/object/notexists', methods=['GET', 'HEAD'])
@logs_blueprint.protect(auth=True, right='base.framework.log.view')
@logs_blueprint.parse_collection_parameters()
def get_logs_with_deleted_objects(params: CollectionParameters):
    """
    Retrieves all logs of objects which are deleted

    Args:
        params (CollectionParameters): parameters for query
    Returns:
        GetMultiResponse: with all logs of deleted objects
    """
    try:
        query = logs_manager.query_builder.prepare_log_query(False)

        builder_params = BuilderParameters(query, params.limit, params.skip, params.sort, params.order)

        object_logs = logs_manager.iterate(builder_params)

        logs = [CmdbObjectLog.to_json(_) for _ in object_logs.results]

        api_response = GetMultiResponse(logs,
                                        object_logs.total,
                                        params,
                                        request.url,
                                        CmdbMetaLog.MODEL,
                                        request.method == 'HEAD')

    except ManagerIterationError as err:
        LOGGER.debug("ManagerIterationError: %s", err)
        return ErrorBody(400, "Could not retrieve deleted objects logs from database!").response()

    return api_response.make_response()


@logs_blueprint.route('/object/deleted', methods=['GET', 'HEAD'])
@logs_blueprint.protect(auth=True, right='base.framework.log.view')
@logs_blueprint.parse_collection_parameters()
def get_object_delete_logs(params: CollectionParameters):
    """
    Retrives all logs of objects being deleted

    Args:
        params (CollectionParameters): filter for documents
    Returns:
        GetMultiResponse: with all object deleted logs
    """
    try:
        query = {
            'log_type': CmdbObjectLog.__name__,
            'action': LogAction.DELETE.value
        }
        builder_params = BuilderParameters(query, params.limit, params.skip, params.sort, params.order)
        object_logs = logs_manager.iterate(builder_params)

        logs = [CmdbObjectLog.to_json(_) for _ in object_logs.results]

        api_response = GetMultiResponse(logs,
                                        object_logs.total,
                                        params,
                                        request.url,
                                        CmdbMetaLog.MODEL,
                                        request.method == 'HEAD')

    except ManagerIterationError as err:
        LOGGER.debug("ManagerIterationError: %s", err)
        return ErrorBody(400, "Could not retrieve the deleted object logs from database!").response()

    return api_response.make_response()


@logs_blueprint.route('/object/<int:object_id>', methods=['GET', 'HEAD'])
@logs_blueprint.protect(auth=True, right='base.framework.log.view')
@logs_blueprint.parse_collection_parameters()
def get_logs_by_object(object_id: int, params: CollectionParameters):
    """
    Retrieves logs for an object with the given public_id

    Args:
        object_id (int): public_id of the object
        params (CollectionParameters): Filter for documents
    Returns:
        GetMultiResponse: with all logs of the object
    """
    try:
        builder_params = BuilderParameters({'object_id':object_id},
                                           params.limit,
                                           params.skip,
                                           params.sort,
                                           params.order)

        iteration_result = logs_manager.iterate(builder_params)

        logs = [CmdbObjectLog.to_json(_) for _ in iteration_result.results]

        api_response = GetMultiResponse(logs,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        CmdbMetaLog.MODEL,
                                        request.method == 'HEAD')
    except ManagerIterationError as err:
        LOGGER.debug("ManagerIterationError: %s", err)
        return ErrorBody(400, f"Could not retrieve logs for object with ID:{object_id}!").response()

    return api_response.make_response()


@logs_blueprint.route('/<int:public_id>/corresponding', methods=['GET', 'HEAD'])
@logs_blueprint.protect(auth=True, right='base.framework.log.view')
def get_corresponding_object_logs(public_id: int):
    """
    Get the corresponding log

    Args:
        public_id (int): public_id of log
    Returns:
        dict: object log
    """
    try:
        selected_log: CmdbObjectLog = logs_manager.get_one(public_id)
        query = {
            'log_type': CmdbObjectLog.__name__,
            'object_id': selected_log['object_id'],
            'action': LogAction.EDIT.value,
            '$nor': [{
                'public_id': public_id
            }]
        }

        builder_params = BuilderParameters(query)

        logs = logs_manager.iterate(builder_params)
        corresponding_logs = [CmdbObjectLog.to_json(log) for log in logs.results]
    except ManagerIterationError as err:
        LOGGER.debug("ManagerIterationError: %s", err)
        return ErrorBody(400, f"Could not retrieve corresponding logs for ID:{public_id}!").response()

    return make_response(corresponding_logs)

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@logs_blueprint.route('/<int:public_id>', methods=['DELETE'])
@logs_blueprint.protect(auth=True, right='base.framework.log.delete')
def delete_log(public_id: int):
    """
    Deletes a single log with the given public_id

    Args:
        public_id (int): public_id of the log which need to be deleted
    Returns:
        bool: deletion success
    """
    try:
        deleted = logs_manager.delete({'public_id':public_id})
    except ManagerDeleteError as err:
        LOGGER.debug("ManagerDeleteError: %s", err)
        return ErrorBody(400, f"Could not delete the log with the ID:{public_id}!").response()

    return make_response(deleted)
