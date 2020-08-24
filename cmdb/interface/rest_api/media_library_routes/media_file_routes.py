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
from cmdb.interface.route_utils import make_response, RootBlueprint, insert_request_user, login_required, right_required
from cmdb.user_management import User
from cmdb.interface.rest_api.media_library_routes.media_file_route_utils import get_element_from_data_request, \
    get_file_in_request, generate_metadata_filter, recursive_delete_filter


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
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_file_list(request_user: User):
    """
    get all objects in database

    Returns:
        list of media_files
    """
    try:
        media_file_list = media_file_manager.get_all_media_files(generate_metadata_filter('metadata', request))
    except ObjectManagerGetError as err:
        LOGGER.error(err.message)
        return abort(404)
    if len(media_file_list) < 1:
        return make_response(media_file_list, 204)

    return make_response(media_file_list)


@media_file_blueprint.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.framework.object.edit')
def add_new_file(request_user: User):
    """ This method saves a file to the specified section of the document for storing workflow data.
        Any existing value that matches filename and the metadata is deleted. Before saving a value.
        GridFS document under the specified key is deleted.

        File:
            File is stored under 'request.files["file"]'

        Metadata:
            Metadata are stored under 'request.form["Metadata"]'

        Args:
            request_user (User): the instance of the started user
        Returns:
            int: ObjectId of GridFS File.
        """
    try:
        file = get_file_in_request('file')
        filter_metadata = generate_metadata_filter('metadata', request)

        # Check if file exists
        is_exist_file = media_file_manager.exist_media_file(file.filename, filter_metadata)
        if is_exist_file:
            grid_fs_file = media_file_manager.get_media_file(file.filename, filter_metadata)
            media_file_manager.delete_media_file(grid_fs_file._file['public_id'])

        metadata = get_element_from_data_request('metadata', request)
        metadata['author_id'] = request_user.public_id
        metadata['mime_type'] = file.mimetype
        ack = media_file_manager.insert_media_file(data=file, metadata=metadata)
    except ObjectInsertError:
        return abort(500)

    resp = make_response(ack)
    return resp


@media_file_blueprint.route('/', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.framework.object.edit')
def update_file(request_user: User):
    try:

        import json
        from bson import json_util
        add_data_dump = json.dumps(request.json)

        new_file_data = json.loads(add_data_dump, object_hook=json_util.object_hook)

        # Check if file exists
        curr_file = media_file_manager.get_media_file_by_public_id(new_file_data['public_id'])._file
        curr_file['public_id'] = new_file_data['public_id']
        curr_file['filename'] = new_file_data['filename']
        curr_file['metadata'] = new_file_data['metadata']
        curr_file['metadata']['author_id'] = new_file_data['metadata']['author_id'] = request_user.get_public_id()

        ack = media_file_manager.updata_media_file(curr_file)
    except ObjectInsertError:
        return abort(500)

    resp = make_response(ack)
    return resp


@media_file_blueprint.route('/<string:name>/', methods=['GET'])
@media_file_blueprint.route('/<string:name>', methods=['GET'])
@login_required
def get_file_by_name(name: str):
    """ Validation: Check folder name for uniqueness
        Create a unique directory:
         - Folders in the same directory are unique.
         - The same Folder-Name can exist in different directories

        Create subfolders:
         - Selected folder is considered as parent

        This also applies for files

        Args:
            name: folderName must be unique

        Returns: True if exist else False

        """
    try:
        filter_metadata = generate_metadata_filter('metadata', request)
        media_file = media_file_manager.exist_media_file(name, filter_metadata)
    except ObjectManagerGetError as err:
        return abort(404, err.message)
    return make_response(media_file)


@media_file_blueprint.route('/download/<path:filename>', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def download_media_file(request_user: User, filename: str):
    try:
        filter_metadata = generate_metadata_filter('metadata', request)
        grid_fs_file = media_file_manager.get_media_file(filename, filter_metadata).read()
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


@media_file_blueprint.route('<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.framework.object.edit')
def delete_file(request_user: User, public_id: int):
    try:
        for _id in recursive_delete_filter(public_id, media_file_manager):
            media_file_manager.delete_media_file(_id)
    except ObjectDeleteError:
        return abort(500)

    return make_response(True)
