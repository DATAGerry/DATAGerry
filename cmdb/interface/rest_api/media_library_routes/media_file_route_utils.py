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
from typing import Union

from flask import request, abort
from werkzeug.datastructures import FileStorage
from werkzeug.wrappers import Request

from cmdb.manager.query_builder.builder import Builder
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.manager.media_file_manager import MediaFileManager
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #

def get_file_in_request(file_name: str) -> FileStorage:
    """TODO: document"""
    try:
        return request.files.get(file_name)
    except (KeyError, Exception):
        LOGGER.error('File with name: %s was not provided', file_name)
        return abort(400)


def get_element_from_data_request(element, _request: Request) -> Union[dict, None]:
    """TODO: document"""
    try:
        metadata = json.loads(_request.form.to_dict()[element])
        return metadata
    except (KeyError, Exception):
        return None


def generate_metadata_filter(element, _request=None, params=None):
    """TODO: document"""
    filter_metadata = {}

    try:
        data = params
        if _request:
            if _request.args.get(element):
                data = json.loads(_request.args.get(element))
            if not data:
                data = get_element_from_data_request(element, _request)

        for key, value in data.items():
            if 'reference' == key and value:
                if isinstance(value, list):
                    filter_metadata.update({f"metadata.{key}": {'$in': value}})
                else:
                    filter_metadata.update({f"metadata.{key}": {'$in': [int(value)]}})
            else:
                filter_metadata.update({f"metadata.{key}": value})

    except (IndexError, KeyError, TypeError, Exception) as ex:
        LOGGER.error('Metadata was not provided - Exception: %s', ex)
        return abort(400)
    return filter_metadata


def generate_collection_parameters(params: CollectionParameters):
    """TODO: document"""
    builder = Builder()
    search = params.optional.get('searchTerm')
    param = json.loads(params.optional['metadata'])

    if search:
        _ = [
            builder.regex_('filename', search)
            , builder.regex_('metadata.reference_type', search)
            , builder.regex_('metadata.mime_type', search)
        ]

        if search.isdigit():
            _.append({'public_id': int(search)})
            _.append({'metadata.reference': int(search)})
            _.append(builder.in_('metadata.reference', [int(search)]))
            _.append({'metadata.parent': int(search)})

        return builder.and_([{'metadata.folder': False}, builder.or_(_)])

    return generate_metadata_filter('metadata', params=param)


def create_attachment_name(name, index, metadata, media_file_manager):
    """ This method checks whether the current file name already exists in the directory.
        If this is the case, 'copy_(index)_' is appended as a prefix. method is executed recursively.

        Args:
            name (str): filename of the File
            index (int): counter
            metadata (dict): Metadata for filtering Files from Database
            media_file_manager (MediaFileManager): Manager
        Returns:
         New Filename with 'copy_(index)_' - prefix.
    """
    try:
        if media_file_manager.exist_file(metadata):
            index += 1  
            name = name.replace(f'copy_({index-1})_', '')
            name = f'copy_({index})_{name}'
            metadata['filename'] = name

            return create_attachment_name(name, index, metadata, media_file_manager)

        return name
    except Exception as err:
        raise Exception(err) from err


def recursive_delete_filter(public_id: int, media_file_manager: MediaFileManager, _ids=None) -> list:
    """ This method deletes a file in the specified section of the document for storing workflow data.
        Any existing value that matches the file name and metadata is deleted. Before saving a value.
        GridFS document under the specified key is deleted.

        Args:
            public_id (int): Public ID of the File
            media_file_manager (MediaFileManager): Manager
            _ids (list(int): List of IDs of the Files
        Returns:
         List of deleted public_id.
    """
    if not _ids:
        _ids = []

    root = media_file_manager.get_many(metadata={'public_id': public_id}).result[0]
    output = media_file_manager.get_many(metadata={'metadata.parent': root['public_id']})
    _ids.append(root['public_id'])

    for item in output.result:
        recursive_delete_filter(item['public_id'], media_file_manager, _ids)

    return _ids
