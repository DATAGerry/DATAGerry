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
import json

from datetime import datetime, timezone

from flask import abort, request, jsonify, current_app
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.exportd.exportd_job.exportd_job_manager import ExportdJobManagerGetError, \
    ExportdJobManagerInsertError, ExportdJobManagerUpdateError, ExportdJobManagerDeleteError, ExportdJobManagement
from cmdb.exportd.exportd_logs.exportd_log_manager import LogManagerInsertError, LogAction, ExportdJobLog, \
    ExportdLogManager
from cmdb.exportd.exportd_job.exportd_job import ExportdJob, ExecuteState
from cmdb.exportd.managers.exportd_job_manager import ExportDJobManager
from cmdb.framework.results import IterationResult
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import GetMultiResponse
from cmdb.interface.rest_api.exportd_routes import exportd_blueprint
from cmdb.interface.route_utils import make_response, login_required, insert_request_user, right_required
from cmdb.interface.blueprint import RootBlueprint
from cmdb.framework.cmdb_errors import ObjectManagerGetError
from cmdb.manager import ManagerIterationError, ManagerGetError
from cmdb.user_management import UserModel
from cmdb.utils.error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

with current_app.app_context():
    object_manager = CmdbObjectManager(current_app.database_manager)
    exportd_manager = ExportdJobManagement(current_app.database_manager, current_app.event_queue)
    log_manager = ExportdLogManager(current_app.database_manager)

LOGGER = logging.getLogger(__name__)
exportd_job_blueprint = RootBlueprint('exportd_job_blueprint', __name__, url_prefix='/exportdjob')


# DEFAULT ROUTES
@exportd_blueprint.route('/jobs', methods=['GET', 'HEAD'])
@exportd_blueprint.protect(auth=True, right='base.exportd.job.view')
@exportd_blueprint.parse_collection_parameters()
def get_exportd_jobs(params: CollectionParameters):
    """Iterate route for exportd jobs"""

    job_manager = ExportDJobManager(current_app.database_manager)
    body = request.method == 'HEAD'

    try:
        iteration_result: IterationResult[ExportdJob] = job_manager.iterate(
            filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
        types = [ExportdJob.to_json(type) for type in iteration_result.results]
        api_response = GetMultiResponse(types, total=iteration_result.total, params=params,
                                        url=request.url, model=ExportdJob.MODEL, body=body)
    except ManagerIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


# DEFAULT ROUTES
@exportd_job_blueprint.route('/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.exportd.job.view')
def get_exportd_job_list(request_user: UserModel):
    """
    get all objects in database
    Returns:
        list of exportd jobs
    """
    try:
        job_list = exportd_manager.get_all_jobs()
    except ExportdJobManagerGetError as e:
        return abort(400, e.message)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as err:
        LOGGER.info("Error occured in get_exportd_job_list(): %s", err)
        return abort(404, jsonify(message='Not Found'))
    return make_response(job_list)


@exportd_job_blueprint.route('/<int:public_id>/', methods=['GET'])
@exportd_job_blueprint.route('/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.exportd.job.view')
def get_exportd_job(public_id, request_user: UserModel):
    """
        get job in database
        Returns:
            exportd job
        """
    try:
        job = exportd_manager.get_job(public_id)
    except ExportdJobManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    resp = make_response(job)
    return resp


@exportd_job_blueprint.route('/name/<string:name>/', methods=['GET'])
@exportd_job_blueprint.route('/name/<string:name>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.exportd.job.view')
def get_type_by_name(name: str, request_user: UserModel):
    """TODO: document"""
    try:
        job_instance = exportd_manager.get_job_by_name(name=name)
    except ObjectManagerGetError as err:
        return abort(404, err.message)
    return make_response(job_instance)


@exportd_job_blueprint.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.exportd.job.add')
def add_job(request_user: UserModel):
    """TODO: document"""
    from bson import json_util
    add_data_dump = json.dumps(request.json)
    try:
        new_job_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
        new_job_data['public_id'] = exportd_manager.get_new_id(ExportdJob.COLLECTION)
        new_job_data['last_execute_date'] = datetime.now(timezone.utc)
        new_job_data['author_id'] = request_user.get_public_id()
        new_job_data['author_name'] = request_user.get_display_name()
        new_job_data['state'] = ExecuteState.SUCCESSFUL.name
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)
    try:
        job_instance = ExportdJob(**new_job_data)
    except CMDBError as e:
        LOGGER.debug(e)
        return abort(400)
    try:
        ack = exportd_manager.insert_job(job_instance)
    except ExportdJobManagerInsertError:
        return abort(500)

    # Generate new insert log
    try:
        log_params = {
            'job_id': job_instance.get_public_id(),
            'state': True,
            'user_id': request_user.get_public_id(),
            'user_name': request_user.get_display_name(),
            'event': LogAction.CREATE.name,
            'message': '',
        }
        log_manager.insert_log(action=LogAction.CREATE, log_type=ExportdJobLog.__name__, **log_params)
    except LogManagerInsertError as err:
        LOGGER.error(err)

    return make_response(ExportdJob.to_json(job_instance))


@exportd_job_blueprint.route('/', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.exportd.job.edit')
def update_job(request_user: UserModel):
    """TODO: document"""
    from bson import json_util
    add_data_dump = json.dumps(request.json)
    new_job_data = None
    try:
        new_job_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)
    try:
        state = new_job_data["state"]
        update_job_instance = ExportdJob(**new_job_data)
    except CMDBError:
        return abort(400)
    try:
        exportd_manager.update_job(update_job_instance, request_user, False)
    except ExportdJobManagerUpdateError:
        return abort(500)

    # Generate new insert log
    if state not in ExecuteState.RUNNING.name:
        try:
            log_params = {
                'job_id': update_job_instance.get_public_id(),
                'state': True,
                'user_id': request_user.get_public_id(),
                'user_name': request_user.get_display_name(),
                'event': LogAction.EDIT.name,
                'message': '',
            }
            log_manager.insert_log(action=LogAction.EDIT, log_type=ExportdJobLog.__name__, **log_params)
        except LogManagerInsertError as err:
            LOGGER.error(err)

    resp = make_response(update_job_instance)
    return resp


@exportd_job_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@exportd_job_blueprint.route('/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.exportd.job.delete')
def delete_job(public_id: int, request_user: UserModel):
    """TODO: document"""
    try:
        try:
            job_instance = exportd_manager.get_job(public_id)
            log_params = {
                'job_id': job_instance.get_public_id(),
                'state': True,
                'user_id': request_user.get_public_id(),
                'user_name': request_user.get_display_name(),
                'event': LogAction.DELETE.name,
                'message': '',
            }
            log_manager.insert_log(action=LogAction.DELETE, log_type=ExportdJobLog.__name__, **log_params)
        except (ExportdJobManagerGetError, LogManagerInsertError) as err:
            LOGGER.error(err)
            return abort(404)

        ack = exportd_manager.delete_job(public_id=public_id, request_user=request_user)
    except ExportdJobManagerDeleteError:
        return abort(400)
    except CMDBError:
        return abort(500)
    resp = make_response(ack)
    return resp


@exportd_job_blueprint.route('/manual/<int:public_id>/', methods=['GET'])
@exportd_job_blueprint.route('/manual/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.exportd.job.run')
def get_run_job_manual(public_id, request_user: UserModel):
    """
     run job manual
    """
    try:
        exportd_manager.get_job(public_id=public_id)
        ack = exportd_manager.run_job_manual(public_id, request_user)
    except Exception as err:
        LOGGER.error(err)
        return abort(404)

    resp = make_response(ack)
    return resp


@exportd_job_blueprint.route('/pull/<int:public_id>/', methods=['GET'])
@exportd_job_blueprint.route('/pull/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.exportd.job.run')
def get_job_output_by_id(public_id, request_user: UserModel):
    """TODO: document"""
    try:
        job = exportd_manager.get_job_by_args(public_id=public_id, exportd_type='PULL')
        resp = worker(job, request_user)
    except ObjectManagerGetError as err:
        return abort(404, err.message)
    return resp


@exportd_job_blueprint.route('/pull/<string:name>/', methods=['GET'])
@exportd_job_blueprint.route('/pull/<string:name>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.exportd.job.run')
def get_job_output_by_name(name, request_user: UserModel):
    """TODO: document"""
    try:
        job = exportd_manager.get_job_by_args(name=name, exportd_type='PULL')
        resp = worker(job, request_user)
    except ObjectManagerGetError as err:
        return abort(404, err.message)
    return resp


def worker(job: ExportdJob, request_user: UserModel):
    """TODO: document"""
    from flask import make_response as make_res
    from cmdb.exportd.exporter_base import ExportdManagerBase
    from cmdb.event_management.event import Event

    try:
        event = Event("cmdb.exportd.run_manual", {"id": job.get_public_id(),
                                                  "user_id": request_user.get_public_id(),
                                                  "event": 'manuel'})

        content = ExportdManagerBase(job, object_manager, log_manager, event).execute(request_user.public_id,
                                                                                      request_user.get_display_name(),
                                                                                      False)
        response = make_res(content.data, content.status)
        response.headers['Content-Type'] = f'{content.mimetype}; charset={content.charset}'
        return response
    except Exception as err:
        LOGGER.error(err)
        return abort(404)
