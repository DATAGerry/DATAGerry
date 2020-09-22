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
from bson import json_util

from flask import abort, request, current_app, Response, jsonify
from cmdb.media_library.media_file_manager import MediaFileManagerGetError, \
    MediaFileManagerDeleteError, MediaFileManagerUpdateError, MediaFileManagerInsertError
from cmdb.interface.route_utils import make_response, insert_request_user, login_required, right_required
from cmdb.user_management import User
from cmdb.interface.rest_api.media_library_routes.media_file_route_utils import get_element_from_data_request, \
    get_file_in_request, generate_metadata_filter, recursive_delete_filter


from cmdb.interface.response import GetMultiResponse, InsertSingleResponse
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.blueprint import APIBlueprint


with current_app.app_context():
    media_file_manager = current_app.media_file_manager
    log_manager = current_app.exportd_log_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
media_file_blueprint = APIBlueprint('media_file_blueprint', __name__, url_prefix='/media_file')


@media_file_blueprint.route('/', methods=['GET', 'HEAD'])
@media_file_blueprint.protect(auth=True, right='base.framework.object.view')
@media_file_blueprint.parse_collection_parameters()
def get_file_list(params: CollectionParameters):
    """
    get all objects in database

    Returns:
        list of media_files
    """
    try:
        param = json.loads(params.optional['metadata'])
        metadata = generate_metadata_filter('metadata', params=param)
        query = {'limit': params.limit, 'skip': params.skip}
        output = media_file_manager.get_all_media_files(metadata, **query)
        api_response = GetMultiResponse(output.result, total=output.total, params=params, url=request.url)
    except MediaFileManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


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
            New MediaFile.
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

        result = media_file_manager.insert_media_file(data=file, metadata=metadata)
    except (MediaFileManagerInsertError, MediaFileManagerGetError):
        return abort(500)

    api_response = InsertSingleResponse(result['public_id'], raw=result, url=request.url)
    return api_response.make_response(prefix='library')


@media_file_blueprint.route('/', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.framework.object.edit')
def update_file(request_user: User):
    try:
        add_data_dump = json.dumps(request.json)
        new_file_data = json.loads(add_data_dump, object_hook=json_util.object_hook)

        # Check if file exists
        data = media_file_manager.get_media_file_by_public_id(new_file_data['public_id'])._file
        data['public_id'] = new_file_data['public_id']
        data['filename'] = new_file_data['filename']
        data['metadata'] = new_file_data['metadata']
        data['metadata']['author_id'] = new_file_data['metadata']['author_id'] = request_user.get_public_id()
        media_file_manager.updata_media_file(data)
    except MediaFileManagerUpdateError:
        return abort(500)

    resp = make_response(data)
    return resp


@media_file_blueprint.route('/<string:name>/', methods=['GET'])
@media_file_blueprint.route('/<string:name>', methods=['GET'])
@media_file_blueprint.protect(auth=True, right='base.framework.object.view')
def get_file(name: str):
    """ Validation: Check folder name for uniqueness

        For Example

        Create a unique media file element:
         - Folders in the same directory are unique.
         - The same Folder-Name can exist in different directories

        Create subfolders:
         - Selected folder is considered as parent

        This also applies for files

        Args:
            name: name must be unique

        Returns: MediaFile

        """
    try:
        filter_metadata = generate_metadata_filter('metadata', request)
        result = media_file_manager.get_media_file(name, filter_metadata)._file
    except MediaFileManagerGetError as err:
        return abort(404, err.message)
    return make_response(result)


@media_file_blueprint.route('/download/<path:filename>', methods=['POST'])
@media_file_blueprint.protect(auth=True, right='base.framework.object.view')
def download_file(filename: str):
    try:
        filter_metadata = generate_metadata_filter('metadata', request)
        grid_fs_file = media_file_manager.get_media_file(filename, filter_metadata).read()
    except MediaFileManagerInsertError:
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
@media_file_blueprint.protect(auth=True, right='base.framework.object.edit')
def delete_file(public_id: int):
    try:
        deleted = media_file_manager.get_media_file_by_public_id(public_id)
        for _id in recursive_delete_filter(public_id, media_file_manager):
            media_file_manager.delete_media_file(_id)
    except MediaFileManagerDeleteError:
        return abort(500)

    return make_response(deleted._file)
