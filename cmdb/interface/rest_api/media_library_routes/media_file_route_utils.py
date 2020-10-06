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

import json
import logging

from flask import request, abort
from werkzeug.datastructures import FileStorage
from werkzeug.wrappers import Request
from cmdb.search.query.builder import Builder
from cmdb.interface.api_parameters import CollectionParameters

LOGGER = logging.getLogger(__name__)


def get_file_in_request(file_name: str) -> FileStorage:
    try:
        return request.files.get(file_name)
    except (KeyError, Exception):
        LOGGER.error(f'File with name: {file_name} was not provided')
        return abort(400)


def get_element_from_data_request(element, _request: Request) -> (dict, None):
    try:
        metadata = json.loads(_request.form.to_dict()[element])
        return metadata
    except (KeyError, Exception):
        return None


def generate_metadata_filter(element, _request=None, params=None):
    filter_metadata = {}
    try:
        data = params
        if _request:
            if _request.args.get(element):
                data = json.loads(_request.args.get(element))
            if not data:
                data = get_element_from_data_request(element, _request)
        for key, value in data.items():
            filter_metadata.update({"metadata.%s" % key: value})
    except (IndexError, KeyError, TypeError, Exception) as ex:
        LOGGER.error(f'Metadata was not provided - Exception: {ex}')
        return abort(400)
    return filter_metadata


def generate_metadata(params: CollectionParameters):

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


def recursive_delete_filter(public_id, media_file_manager, _ids=None) -> []:
    if not _ids:
        _ids = []

    root = media_file_manager.get_many(metadata={'public_id': public_id}).result[0]
    output = media_file_manager.get_many(metadata={'metadata.parent': root.public_id})
    _ids.append(root.public_id)

    for item in output.result:
        recursive_delete_filter(item.public_id, media_file_manager, _ids)

    return _ids
