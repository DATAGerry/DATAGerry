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

from flask import abort, request, current_app, Response
from cmdb.framework.cmdb_errors import ObjectDeleteError, ObjectInsertError, ObjectManagerGetError
from cmdb.interface.route_utils import make_response, RootBlueprint


with current_app.app_context():
    media_file_manager = current_app.media_file_manager
    log_manager = current_app.exportd_log_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
media_file_blueprint = RootBlueprint('media_file_blueprint', __name__, url_prefix='/media_file')

# DEFAULT ROUTES


@media_file_blueprint.route('/', methods=['GET'])
# @login_required
# @insert_request_user
# @right_required('base.framework.object.view')
def get_object_list():
    """
    get all objects in database
    Args:
        request_user: auto inserted user who made the request.
    Returns:
        list of media_files
    """
    try:
        media_file_list = media_file_manager.get_all_media_files()
    except ObjectManagerGetError as err:
        LOGGER.error(err.message)
        return abort(404)
    if len(media_file_list) < 1:
        return make_response(media_file_list, 204)

    return make_response(media_file_list)


@media_file_blueprint.route('/', methods=['POST'])
def add_new_file():
    try:
        ack = media_file_manager.insert_media_file(request.files['file'], request.files['metadata'])
    except ObjectInsertError:
        return abort(500)

    resp = make_response(ack)
    return resp


@media_file_blueprint.route('/download/<path:filename>', methods=['POST'])
def download_media_file(filename: str):
    try:
        grid_fs_file = media_file_manager.get_media_file(filename)
    except ObjectInsertError:
        return abort(500)

    return Response(
        grid_fs_file,
        mimetype="application/octet-stream",
        headers={
            "Content-Disposition":
                "attachment; filename=%s" % filename
        }
    )


@media_file_blueprint.route('/<path:filename>', methods=['DELETE'])
def delete_media_file(filename: str):
    try:
        ack = media_file_manager.delete_media_file(file_name=filename)
    except ObjectDeleteError:
        return abort(500)

    resp = make_response(ack)
    return resp
