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

from datetime import datetime

from flask import abort, request, jsonify, current_app
from cmdb.utils.wraps import json_required
from cmdb.exportd.exportd_job.exportd_job_manager import ExportdJobManagerGetError,\
    ExportdJobManagerInsertError, ExportdJobManagerUpdateError, ExportdJobManagerDeleteError
from cmdb.exportd.exportd_logs.exportd_log_manager import LogManagerInsertError, LogAction, ExportdJobLog
from cmdb.exportd.exportd_job.exportd_job import ExportdJob, ExecuteState
from cmdb.interface.route_utils import make_response, RootBlueprint, insert_request_user, login_required
from cmdb.user_management import User

with current_app.app_context():
    exportd_manager = current_app.exportd_manager
    log_manager = current_app.exportd_log_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
exportd_job_blueprint = RootBlueprint('exportd_job_blueprint', __name__, url_prefix='/exportdjob')


# DEFAULT ROUTES
@exportd_job_blueprint.route('/', methods=['GET'])
@login_required
def get_exportd_job_list():
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
    except CMDBError as e:
        return abort(404, jsonify(message='Not Found', error=e.message))
    return make_response(job_list)


@exportd_job_blueprint.route('/<int:public_id>/', methods=['GET'])
@exportd_job_blueprint.route('/<int:public_id>', methods=['GET'])
@login_required
def get_exportd_job(public_id):
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


@exportd_job_blueprint.route('/', methods=['POST'])
@login_required
@insert_request_user
def add_job(request_user: User):
    from bson import json_util
    add_data_dump = json.dumps(request.json)
    try:
        new_job_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
        new_job_data['public_id'] = exportd_manager.get_new_id(ExportdJob.COLLECTION)
        new_job_data['last_execute_date'] = datetime.utcnow()
        new_job_data['author_id'] = request_user.get_public_id()
        new_job_data['author_name'] = request_user.get_name()
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
            'user_id': request_user.get_public_id(),
            'user_name': request_user.get_name(),
            'event': LogAction.CREATE.name,
            'message': '',
        }
        log_manager.insert_log(action=LogAction.CREATE, log_type=ExportdJobLog.__name__, **log_params)
    except LogManagerInsertError as err:
        LOGGER.error(err)

    resp = make_response(ack)
    return resp


@exportd_job_blueprint.route('/', methods=['PUT'])
@login_required
@json_required
@insert_request_user
def update_job(request_user: User):
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
                'user_name': request_user.get_name(),
                'event': LogAction.EDIT.name,
                'message': '',
            }
            log_manager.insert_log(action=LogAction.EDIT, log_type=ExportdJobLog.__name__, **log_params)
        except LogManagerInsertError as err:
            LOGGER.error(err)

    resp = make_response(update_job_instance)
    return resp


@exportd_job_blueprint.route('/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
def delete_job(public_id: int, request_user: User):
    try:
        try:
            job_instance = exportd_manager.get_job(public_id)
            log_params = {
                'job_id': job_instance.get_public_id(),
                'user_id': request_user.get_public_id(),
                'user_name': request_user.get_name(),
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
def get_run_job_manual(public_id, request_user: User):
    """
     run job manual
    """
    try:
        ack = exportd_manager.run_job_manual(public_id, request_user)
    except Exception as err:
        LOGGER.error(err)
        return abort(404)

    resp = make_response(ack)
    return resp
