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

from flask import request, abort, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from cmdb.framework import CmdbType
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.importer import load_parser_class, load_importer_class, __OBJECT_IMPORTER__, __OBJECT_PARSER__
from cmdb.importer.importer_config import ObjectImporterConfig
from cmdb.importer.parser_base import BaseObjectParser
from cmdb.interface.rest_api.import_routes import importer_blueprint
from cmdb.interface.route_utils import NestedBlueprint, make_response
from cmdb.interface.rest_api.importer.importer_route_utils import get_file_in_request, get_element_from_data_request, \
    generate_parsed_output

LOGGER = logging.getLogger(__name__)

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

with current_app.app_context():
    object_manager: CmdbObjectManager = current_app.object_manager

importer_object_blueprint = NestedBlueprint(importer_blueprint, url_prefix='/object')


@importer_object_blueprint.route('/importer/', methods=['GET'])
@importer_object_blueprint.route('/importer', methods=['GET'])
def get_importer():
    importer = [importer for importer in __OBJECT_IMPORTER__]
    return make_response(importer)


@importer_object_blueprint.route('/parser/', methods=['GET'])
@importer_object_blueprint.route('/parser', methods=['GET'])
def get_parser():
    parser = [parser for parser in __OBJECT_PARSER__]
    return make_response(parser)


# @importer_object_blueprint.route('/default', defaults={'importer_type': 'json'}, methods=['GET'])
# @importer_object_blueprint.route('/default/', defaults={'importer_type': 'json'}, methods=['GET'])
@importer_object_blueprint.route('/parser/default/<string:parser_type>', methods=['GET'])
@importer_object_blueprint.route('/parser/default/<string:parser_type>/', methods=['GET'])
def get_default_parser_config(parser_type: str):
    try:
        parser: BaseObjectParser = __OBJECT_PARSER__[parser_type]
    except IndexError:
        return abort(400)
    return make_response(parser.DEFAULT_CONFIG)


@importer_object_blueprint.route('/parse/', methods=['POST'])
@importer_object_blueprint.route('/parse', methods=['POST'])
def parse_objects():
    LOGGER.debug(request.form)
    # Check if file exists
    request_file: FileStorage = get_file_in_request('file', request.files)
    # Load parser config
    parser_config: dict = get_element_from_data_request('parser_config', request) or {}
    parsed_output = generate_parsed_output(request_file, parser_config)

    return make_response(parsed_output)


@importer_object_blueprint.route('/', methods=['POST'])
def import_objects():
    # Check if file exists
    request_file: FileStorage = get_file_in_request('file', request.files)

    filename = secure_filename(request_file.filename)
    working_file = f'/tmp/{filename}'
    request_file.save(working_file)

    # Load parser config
    parser_config: dict = get_element_from_data_request('parser_config', request) or {}

    # Check for importer config
    importer_config_request: dict = get_element_from_data_request('importer_config', request) or None
    if not importer_config_request:
        LOGGER.error(f'No import config was provided')
        return abort(400)

    # Insert type instance
    try:
        framework_type: CmdbType = object_manager.get_type(public_id=importer_config_request.get('type_id'))
        importer_config_request.update({'type_instance': framework_type})
    except CMDBError:
        return abort(404)

    importer_config = ObjectImporterConfig(**importer_config_request)

    # Load parser class
    parser_class = load_parser_class('object', request_file.content_type)
    parser = parser_class(parser_config)

    # Load Importer
    importer_class = load_importer_class('object', request_file.content_type)
    importer = importer_class(working_file, importer_config, parser)

    import_response = importer.start_import()
    return make_response('test')
