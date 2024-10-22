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
from flask import abort, jsonify, request

from cmdb.manager.exportd_logs_manager import ExportdLogsManager
from cmdb.manager.exportd_jobs_manager import ExportdJobsManager

from cmdb.exportd.exportd_logs.exportd_log import ExportdJobLog, LogAction, ExportdMetaLog
from cmdb.framework.results import IterationResult
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import GetMultiResponse
from cmdb.interface.rest_api.exportd_routes import exportd_blueprint
from cmdb.interface.route_utils import make_response, login_required, right_required, insert_request_user
from cmdb.interface.blueprint import RootBlueprint
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.user_management.models.user import UserModel
from cmdb.manager.manager_provider import ManagerType, ManagerProvider

from cmdb.errors.manager import ManagerGetError, ManagerIterationError
from cmdb.errors.manager.object_manager import ObjectManagerGetError
from cmdb.errors.manager.exportd_log_manager import ExportdLogManagerDeleteError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

exportd_log_blueprint = RootBlueprint('exportd_log_rest', __name__, url_prefix='/exportdlog')

# -------------------------------------------------------------------------------------------------------------------- #

@exportd_blueprint.route('/logs', methods=['GET', 'HEAD'])
@insert_request_user
@exportd_blueprint.protect(auth=True, right='base.exportd.log.view')
@exportd_blueprint.parse_collection_parameters()
def get_exportd_logs(params: CollectionParameters, request_user: UserModel):
    """Iterate route for exportd logs"""
    body = request.method == 'HEAD'

    exportd_logs_manager: ExportdLogsManager = ManagerProvider.get_manager(ManagerType.EXPORTD_LOGS_MANAGER,
                                                                           request_user)

    builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

    try:
        iteration_result: IterationResult[ExportdJobLog] = exportd_logs_manager.iterate(builder_params)

        types = [ExportdJobLog.to_json(type) for type in iteration_result.results]
        api_response = GetMultiResponse(types, total=iteration_result.total, params=params,
                                        url=request.url, model=ExportdMetaLog.MODEL, body=body)
    except ManagerIterationError:
        #ERROR-FIX
        return abort(400)
    except ManagerGetError:
        #ERROR-FIX
        return abort(404, "Could not retrieve exportd logs!")

    return api_response.make_response()


@exportd_log_blueprint.route('/', methods=['GET'])
@insert_request_user
@login_required
@right_required('base.exportd.log.view')
def get_log_list(request_user: UserModel):
    """
    get all exportd logs in database
    Returns:
        list of exportd logs
    """
    exportd_logs_manager: ExportdLogsManager = ManagerProvider.get_manager(ManagerType.EXPORTD_LOGS_MANAGER,
                                                                           request_user)

    try:
        log_list = exportd_logs_manager.get_all_logs()
    except ObjectManagerGetError as err:
        #ERROR-FIX
        LOGGER.debug("[get_log_list] ObjectManagerGetError: %s", err.message)
        return abort(400, "Could not retrieve the log list!")
    except ModuleNotFoundError:
        #ERROR-FIX
        return abort(400)
    except Exception as err:
        #ERROR-FIX
        LOGGER.info("Error occured in get_log_list(): %s", err)
        return abort(404, jsonify(message='Not Found'))

    return make_response(log_list)


@exportd_log_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@exportd_log_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@login_required
@right_required('base.exportd.log.delete')
def delete_log(public_id: int, request_user: UserModel):
    """TODO: document"""
    exportd_logs_manager: ExportdLogsManager = ManagerProvider.get_manager(ManagerType.EXPORTD_LOGS_MANAGER,
                                                                           request_user)

    try:
        delete_ack = exportd_logs_manager.delete_log(public_id)
    except ExportdLogManagerDeleteError:
        #ERROR-FIX
        return abort(500)

    return make_response(delete_ack)


@exportd_log_blueprint.route('/job/<int:public_id>/', methods=['GET'])
@exportd_log_blueprint.route('/job/<int:public_id>', methods=['GET'])
@insert_request_user
@login_required
@right_required('base.exportd.log.view')
def get_logs_by_jobs(public_id: int, request_user: UserModel):
    """TODO: document"""
    exportd_logs_manager: ExportdLogsManager = ManagerProvider.get_manager(ManagerType.EXPORTD_LOGS_MANAGER,
                                                                           request_user)

    try:
        object_logs = exportd_logs_manager.get_exportd_job_logs(public_id=public_id)
    except ObjectManagerGetError as err:
        LOGGER.debug("[get_logs_by_jobs] ObjectManagerGetError: %s", err.message)
        return abort(404)
    if len(object_logs) < 1:
        return make_response(object_logs, 204)

    return make_response(object_logs)


# FIND routes
@exportd_log_blueprint.route('/job/exists/', methods=['GET'])
@exportd_log_blueprint.route('/job/exists', methods=['GET'])
@insert_request_user
@login_required
@right_required('base.exportd.log.view')
def get_logs_with_existing_objects(request_user: UserModel):
    """TODO: document"""
    exportd_logs_manager: ExportdLogsManager = ManagerProvider.get_manager(ManagerType.EXPORTD_LOGS_MANAGER,
                                                                           request_user)
    exportd_jobs_manager: ExportdJobsManager = ManagerProvider.get_manager(ManagerType.EXPORTD_JOBS_MANAGER,
                                                                            request_user)

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
        object_logs = exportd_logs_manager.get_logs_by(**query)
    except ObjectManagerGetError as err:
        LOGGER.debug("[get_logs_with_existing_objects] ObjectManagerGetError: %s", err.message)
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
                exportd_jobs_manager.get_job(current_object_id)
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
@insert_request_user
@login_required
@right_required('base.exportd.log.view')
def get_logs_with_deleted_objects(request_user: UserModel):
    """TODO: document"""
    exportd_logs_manager: ExportdLogsManager = ManagerProvider.get_manager(ManagerType.EXPORTD_LOGS_MANAGER,
                                                                           request_user)
    exportd_jobs_manager: ExportdJobsManager = ManagerProvider.get_manager(ManagerType.EXPORTD_JOBS_MANAGER,
                                                                            request_user)

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
        object_logs = exportd_logs_manager.get_logs_by(**query)
    except ObjectManagerGetError as err:
        LOGGER.debug("[get_logs_with_deleted_objects] ObjectManagerGetError: %s", err.message)
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
                exportd_jobs_manager.get_job(current_object_id)
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
@insert_request_user
@login_required
@right_required('base.exportd.log.view')
def get_job_delete_logs(request_user: UserModel):
    """TODO: document"""
    exportd_logs_manager: ExportdLogsManager = ManagerProvider.get_manager(ManagerType.EXPORTD_LOGS_MANAGER,
                                                                           request_user)

    try:
        query = {
            'log_type': ExportdJobLog.__name__,
            'action': LogAction.DELETE.name
        }
        object_logs = exportd_logs_manager.get_logs_by(**query)
    except (ObjectManagerGetError, Exception) as err:
        LOGGER.debug("[get_job_delete_logs] ObjectManagerGetError: %s", err.message)
        return abort(404)

    if len(object_logs) < 1:
        return make_response(object_logs, 204)

    return make_response(object_logs)
