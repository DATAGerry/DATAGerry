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
import logging

from flask import abort, current_app, jsonify, request

from cmdb.exportd.exportd_job.exportd_job_manager import ExportdJobManagement
from cmdb.exportd.exportd_logs.exportd_log_manager import ExportdLogManager
from cmdb.exportd.managers.exportd_log_manager import ExportDLogManager
from cmdb.framework.cmdb_errors import ObjectManagerGetError
from cmdb.framework.managers.log_manager import LogManagerDeleteError
from cmdb.exportd.exportd_logs.exportd_log import ExportdJobLog, LogAction, ExportdMetaLog
from cmdb.framework.results import IterationResult
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import GetMultiResponse
from cmdb.interface.rest_api.exportd_routes import exportd_blueprint
from cmdb.interface.route_utils import make_response, insert_request_user, login_required, right_required
from cmdb.interface.blueprint import RootBlueprint
from cmdb.manager import ManagerIterationError, ManagerGetError
from cmdb.user_management import UserModel
from cmdb.utils.error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)
exportd_log_blueprint = RootBlueprint('exportd_log_rest', __name__, url_prefix='/exportdlog')

with current_app.app_context():
    exportd_manager = ExportdJobManagement(current_app.database_manager, current_app.event_queue)
    log_manager = ExportdLogManager(current_app.database_manager)


@exportd_blueprint.route('/logs', methods=['GET', 'HEAD'])
@exportd_blueprint.protect(auth=True, right='base.exportd.log.view')
@exportd_blueprint.parse_collection_parameters()
def get_exportd_logs(params: CollectionParameters):
    """Iterate route for exportd logs"""
    body = request.method == 'HEAD'
    log_manager = ExportDLogManager(current_app.database_manager)

    try:
        iteration_result: IterationResult[ExportdJobLog] = log_manager.iterate(
            filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
        types = [ExportdJobLog.to_json(type) for type in iteration_result.results]
        api_response = GetMultiResponse(types, total=iteration_result.total, params=params,
                                        url=request.url, model=ExportdMetaLog.MODEL, body=body)
    except ManagerIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


# DEFAULT ROUTES
@exportd_log_blueprint.route('/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.exportd.log.view')
def get_log_list(request_user: UserModel):
    """
    get all exportd logs in database
    Returns:
        list of exportd logs
    """
    try:
        log_list = log_manager.get_all_logs()
    except ObjectManagerGetError as e:
        return abort(400, e.message)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as err:
        return abort(404, jsonify(message='Not Found', error=err))
    return make_response(log_list)


@exportd_log_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@exportd_log_blueprint.route('/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.exportd.log.delete')
def delete_log(public_id: int, request_user: UserModel):
    """TODO: document"""
    try:
        delete_ack = log_manager.delete_log(public_id=public_id)
    except LogManagerDeleteError as err:
        return abort(500)
    return make_response(delete_ack)


@exportd_log_blueprint.route('/job/<int:public_id>/', methods=['GET'])
@exportd_log_blueprint.route('/job/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.exportd.log.view')
def get_logs_by_jobs(public_id: int, request_user: UserModel):
    """TODO: document"""
    try:
        object_logs = log_manager.get_exportd_job_logs(public_id=public_id)
    except ObjectManagerGetError as err:
        LOGGER.error('Error in get_logs_by_jobs: %s',err)
        return abort(404)
    if len(object_logs) < 1:
        return make_response(object_logs, 204)
    return make_response(object_logs)


# FIND routes
@exportd_log_blueprint.route('/job/exists/', methods=['GET'])
@exportd_log_blueprint.route('/job/exists', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.exportd.log.view')
def get_logs_with_existing_objects(request_user: UserModel):
    """TODO: document"""
    existing_list = []
    deleted_list = []
    passed_objects = []
    try:
        query = {
            'log_type': ExportdJobLog.__name__,
            'action': {
                '$ne': LogAction.DELETE.name
            }
        }
        object_logs = log_manager.get_logs_by(**query)
    except ObjectManagerGetError as err:
        LOGGER.error('Error in get_logs_with_existing_objects: %s', err)
        return abort(404)
    if len(object_logs) < 1:
        return make_response(object_logs, 204)
    for log in object_logs:
        current_object_id: int = log.job_id
        if current_object_id in existing_list:
            passed_objects.append(log)
            continue
        elif current_object_id in deleted_list:
            continue
        else:
            try:
                exportd_manager.get_job(current_object_id)
                existing_list.append(current_object_id)
                passed_objects.append(log)
            except (ObjectManagerGetError, Exception):
                deleted_list.append(current_object_id)
                continue
    if len(passed_objects) < 1:
        return make_response(passed_objects, 204)
    return make_response(passed_objects)


@exportd_log_blueprint.route('/job/notexists/', methods=['GET'])
@exportd_log_blueprint.route('/job/notexists', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.exportd.log.view')
def get_logs_with_deleted_objects(request_user: UserModel):
    """TODO: document"""
    existing_list = []
    deleted_list = []
    passed_objects = []
    try:
        query = {
            'log_type': ExportdJobLog.__name__,
            'action': {
                '$ne': LogAction.DELETE.name
            }
        }
        object_logs = log_manager.get_logs_by(**query)
    except ObjectManagerGetError as err:
        LOGGER.error('Error in get_logs_with_existing_objects: %s',err)
        return abort(404)
    if len(object_logs) < 1:
        return make_response(object_logs, 204)
    for log in object_logs:
        current_object_id: int = log.job_id
        if current_object_id in existing_list:
            continue
        elif current_object_id in deleted_list:
            passed_objects.append(log)
            continue
        else:
            try:
                exportd_manager.get_job(current_object_id)
                existing_list.append(current_object_id)
            except (ObjectManagerGetError, Exception):
                deleted_list.append(current_object_id)
                passed_objects.append(log)
                continue
    if len(passed_objects) < 1:
        return make_response(passed_objects, 204)
    return make_response(passed_objects)


@exportd_log_blueprint.route('/job/deleted/', methods=['GET'])
@exportd_log_blueprint.route('/job/deleted', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.exportd.log.view')
def get_job_delete_logs(request_user: UserModel):
    """TODO: document"""
    try:
        query = {
            'log_type': ExportdJobLog.__name__,
            'action': LogAction.DELETE.name
        }
        object_logs = log_manager.get_logs_by(**query)
    except (ObjectManagerGetError, Exception) as err:
        LOGGER.error('Error in get_object_delete_logs: %s', err)
        return abort(404)
    if len(object_logs) < 1:
        return make_response(object_logs, 204)

    return make_response(object_logs)
