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
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Request

LOGGER = logging.getLogger(__name__)


def get_file_in_request(file_name: str, request_files) -> FileStorage:
    if file_name not in request_files:
        LOGGER.error(f'File with name: {file_name} was not provided')
        return abort(400)
    return request.files.get(file_name)


def get_element_from_data_request(element, _request: Request) -> (dict, None):
    try:
        return json.loads(_request.form.to_dict()[element])
    except (KeyError, Exception):
        return None


def generate_parsed_output(request_file, parser_config):
    from cmdb.importer import load_parser_class
    # Load parser class
    parser_class = load_parser_class('object', request_file.content_type)

    # save file
    filename = secure_filename(request_file.filename)
    working_file = f'/tmp/{filename}'
    request_file.save(working_file)

    # parse content
    parser = parser_class(parser_config)
    output = parser.parse(working_file)
    return output
