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
import json
import logging
from bson import json_util
from flask import abort, request, Response

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.media_files_manager import MediaFilesManager

from cmdb.user_management.models.user import UserModel
from cmdb.interface.route_utils import make_response,\
                                       insert_request_user,\
                                       login_required,\
                                       right_required
from cmdb.interface.rest_api.routes.media_library_routes.media_file_route_utils import get_element_from_data_request,\
                                                                                       get_file_in_request,\
                                                                                       generate_metadata_filter,\
                                                                                       recursive_delete_filter,\
                                                                                       generate_collection_parameters,\
                                                                                       create_attachment_name
from cmdb.interface.rest_api.responses.helpers.api_parameters import CollectionParameters
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.rest_api.responses import InsertSingleResponse,\
                                              GetMultiResponse

from cmdb.errors.manager.media_file_manager import MediaFileManagerGetError,\
                                                   MediaFileManagerInsertError,\
                                                   MediaFileManagerUpdateError,\
                                                   MediaFileManagerDeleteError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

media_file_blueprint = APIBlueprint('media_file_blueprint', __name__, url_prefix='/media_file')

# -------------------------------------------------------------------------------------------------------------------- #

@media_file_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@media_file_blueprint.protect(auth=True, right='base.framework.object.view')
@media_file_blueprint.parse_collection_parameters()
def get_file_list(params: CollectionParameters, request_user: UserModel):
    """
    Get all objects in database

    Args:
        params (CollectionParameters): Passed parameters over the http query string + optional `view` parameter
    Raises:
        MediaFileManagerGetError: If the files could not be found
    Returns:
        list of files
    """
    media_files_manager: MediaFilesManager = ManagerProvider.get_manager(ManagerType.MEDIA_FILES_MANAGER,
                                                                         request_user)

    try:
        metadata = generate_collection_parameters(params=params)
        response_query = {'limit': params.limit, 'skip': params.skip, 'sort': [(params.sort, params.order)]}
        output = media_files_manager.get_many_media_files(metadata, **response_query)
        api_response = GetMultiResponse(output.result, total=output.total, params=params, url=request.url)
    except MediaFileManagerGetError:
        #ERROR-FIX
        return abort(404, "Could not retrive file list!")

    return api_response.make_response()


@media_file_blueprint.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.framework.object.edit')
def add_new_file(request_user: UserModel):
    """
    This method saves a file to the specified section of the document for storing workflow data.
    Any existing value that matches filename and the metadata is deleted. Before saving a value.
    GridFS document under the specified key is deleted.

    For Example:
        Create a unique media file element:
            - Folders in the same directory are unique.
            - The Folder-Name can exist in different directories

        Create sub-folders:
            - Selected folder is considered as parent

        This also applies for files

    File:
        File is stored under 'request.files.get('files')'

    Metadata:
        Metadata are stored under 'request.form["Metadata"]'

    Raises:
        MediaFileManagerGetError: If the file could not be found.
        MediaFileManagerInsertError: If something went wrong during insert

    Args:
        request_user (UserModel): the instance of the started user

    Returns:
        New MediaFile.
    """
    media_files_manager: MediaFilesManager = ManagerProvider.get_manager(ManagerType.MEDIA_FILES_MANAGER,
                                                                         request_user)

    try:
        file = get_file_in_request('file')
        filter_metadata = generate_metadata_filter('metadata', request)
        filter_metadata.update({'filename': file.filename})
        metadata = get_element_from_data_request('metadata', request)

        # Check if file exists
        file_exists = media_files_manager.file_exists(filter_metadata)
        exist = None

        if file_exists:
            exist = media_files_manager.get_file(filter_metadata)
            media_files_manager.delete_file(exist['public_id'])

        # If file exist overwrite the references from previous file
        if exist:
            metadata['reference'] = exist['metadata']['reference']
            metadata['reference_type'] = exist['metadata']['reference_type']
        metadata['author_id'] = request_user.public_id
        metadata['mime_type'] = file.mimetype

        result = media_files_manager.insert_file(data=file, metadata=metadata)
    except (MediaFileManagerInsertError, MediaFileManagerGetError):
        #ERROR-FIX
        return abort(500)

    api_response = InsertSingleResponse(raw=result, result_id=result['public_id'])

    return api_response.make_response()


@media_file_blueprint.route('/', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.framework.object.edit')
def update_file(request_user: UserModel):
    """
    This method updates a file to the specified section in the document.
    Any existing value that matches the file name and metadata is taken into account.
    Furthermore, it is checked whether the current file name already exists in the directory.
    If this is the case, 'copy_(index)_' is appended as prefix. The method is executed recursively.
    Exception, if the parameter 'attachment' is passed with the value '{reference':true}', the name is not checked.

    Note:
        Create a unique media file element:
            - Folders in the same directory are unique.
            - The folder name can exist in different directories

        Create sub-folders:
            - Selected folder is considered as parent folder

        This also applies to files

    Changes:
        Is stored under 'request.json'

    Raises:
        MediaFileManagerUpdateError: If something went wrong during update.

    Args:
        Args:
        request_user (User): the instance of the started user (last modifier)

    Returns: MediaFile as JSON

    """
    media_files_manager: MediaFilesManager = ManagerProvider.get_manager(ManagerType.MEDIA_FILES_MANAGER,
                                                                         request_user)

    try:
        add_data_dump = json.dumps(request.json)
        new_file_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
        reference_attachment = json.loads(request.args.get('attachment'))

        data = media_files_manager.get_file(metadata={'public_id': new_file_data['public_id']})
        data['public_id'] = new_file_data['public_id']
        data['filename'] = new_file_data['filename']
        data['metadata'] = new_file_data['metadata']
        data['metadata']['author_id'] = new_file_data['metadata']['author_id'] = request_user.get_public_id()

        # Check if file / folder exist in folder
        if not reference_attachment['reference']:
            checker = {'filename': new_file_data['filename'], 'metadata.parent': new_file_data['metadata']['parent']}
            copied_name = create_attachment_name(new_file_data['filename'], 0, checker, media_files_manager)
            data['filename'] = copied_name

        media_files_manager.update_file(data)
    except MediaFileManagerUpdateError:
        #ERROR-FIX
        return abort(500)

    return make_response(data)


@media_file_blueprint.route('/<string:filename>/', methods=['GET'])
@media_file_blueprint.route('/<string:filename>', methods=['GET'])
@insert_request_user
@media_file_blueprint.protect(auth=True, right='base.framework.object.view')
def get_file(filename: str, request_user: UserModel):
    """
    This method fetch a file to the specified section of the document.
    Any existing value that matches the file name and metadata will be considered.

    Raises:
        MediaFileManagerGetError: If the file could not be found.

    Args:
        filename: name must be unique

    Returns: MediaFile as JSON
    """
    media_files_manager: MediaFilesManager = ManagerProvider.get_manager(ManagerType.MEDIA_FILES_MANAGER,
                                                                         request_user)

    try:
        filter_metadata = generate_metadata_filter('metadata', request)
        filter_metadata.update({'filename': filename})

        if media_files_manager.file_exists(filter_metadata):
            result = media_files_manager.get_file(metadata=filter_metadata)
        else:
            result = None
    except MediaFileManagerGetError:
        #ERROR-FIX
        return abort(404, f"Could not retrieve file with filename: {filename}")

    return make_response(result)


@media_file_blueprint.route('/download/<path:filename>', methods=['GET'])
@insert_request_user
@media_file_blueprint.protect(auth=True, right='base.framework.object.view')
def download_file(filename: str, request_user: UserModel):
    """
    This method download a file to the specified section of the document.
    Any existing value that matches the file name and metadata will be considered.

    Raises:
        MediaFileManagerGetError: If the file could not be found.

    Args:
        filename (str): name must be unique

    Returns: File
    """
    media_files_manager: MediaFilesManager = ManagerProvider.get_manager(ManagerType.MEDIA_FILES_MANAGER,
                                                                         request_user)

    try:
        filter_metadata = generate_metadata_filter('metadata', request)
        filter_metadata.update({'filename': filename})
        result = media_files_manager.get_file(metadata=filter_metadata, blob=True)
    except MediaFileManagerGetError:
        #ERROR-FIX
        return abort(500)

    return Response(
        result,
        mimetype="application/octet-stream",
        headers={
            "Content-Disposition":
                f"attachment; filename={filename}"
        }
    )

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@media_file_blueprint.route('<int:public_id>', methods=['DELETE'])
@insert_request_user
@media_file_blueprint.protect(auth=True, right='base.framework.object.edit')
def delete_file(public_id: int, request_user: UserModel):
    """
    This method deletes a file in the specified section of the document for storing workflow data.
    Any existing value that matches the file name and metadata is deleted. Before saving a value.
    GridFS document under the specified key is deleted.

    Raises:
        MediaFileManagerDeleteError: When something went wrong during the deletion

    Args:
        public_id (int): Public ID of the File

    Returns:
         Delete result with the deleted File as JSON.
    """
    media_files_manager: MediaFilesManager = ManagerProvider.get_manager(ManagerType.MEDIA_FILES_MANAGER,
                                                                         request_user)

    try:
        file_to_delete = media_files_manager.get_file(metadata={'public_id': public_id})

        if file_to_delete:
            for _id in recursive_delete_filter(public_id, media_files_manager):
                media_files_manager.delete_file(_id)
    except MediaFileManagerDeleteError as err:
        #ERROR-FIX
        LOGGER.debug("[delete_file] MediaFileManagerDeleteError: %s", err)
        return abort(404)

    return make_response(file_to_delete)
