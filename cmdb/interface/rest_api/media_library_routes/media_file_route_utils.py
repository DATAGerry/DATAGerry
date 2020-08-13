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


def generate_metadata_filter(element, _request):
    filter_metadata = {}
    try:
        if _request.args.get(element):
            data = json.loads(_request.args.get(element))
        else:
            data = json.loads(_request.form.to_dict()[element])

        for key, value in data.items():
            filter_metadata.update({"metadata.%s" % key: value})
    except (IndexError, KeyError, TypeError, Exception) as ex:
        LOGGER.error(f'Metadata was not provided - Exception: {ex}')
        return abort(400)
    return filter_metadata
