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

from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.importer import load_parser_class, load_importer_class, __OBJECT_IMPORTER__, __OBJECT_PARSER__, \
    __OBJECT_IMPORTER_CONFIG__, load_importer_config_class
from cmdb.importer.importer_response import ImporterObjectResponse
from cmdb.importer.parser_base import BaseObjectParser
from cmdb.interface.rest_api.import_routes import importer_blueprint
from cmdb.interface.route_utils import NestedBlueprint, make_response, insert_request_user
from cmdb.interface.rest_api.importer.importer_route_utils import get_file_in_request, get_element_from_data_request, \
    generate_parsed_output
from cmdb.user_management import User

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


@importer_object_blueprint.route('/importer/config/', methods=['GET'])
@importer_object_blueprint.route('/importer/config', methods=['GET'])
def get_importer_config():
    config = [config for config in __OBJECT_IMPORTER_CONFIG__]
    return make_response(config)


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
    # Check if file exists
    request_file: FileStorage = get_file_in_request('file', request.files)

    # Load parser config
    parser_config: dict = get_element_from_data_request('parser_config', request) or {}
    LOGGER.debug(f'Parser config: {parser_config}')
    parsed_output = generate_parsed_output(request_file, parser_config).output()

    return make_response(parsed_output)


@importer_object_blueprint.route('/', methods=['POST'])
@insert_request_user
def import_objects(request_user: User):
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

    # Check if type exists
    try:
        object_manager.get_type(public_id=importer_config_request.get('type_id'))
    except CMDBError:
        return abort(404)

    # Load parser
    parser_class = load_parser_class('object', request_file.content_type)
    parser = parser_class(parser_config)

    # Load importer config
    importer_config_class = load_importer_config_class('object', request_file.content_type)
    importer_config = importer_config_class(**importer_config_request)

    # Load importer
    importer_class = load_importer_class('object', request_file.content_type)
    importer = importer_class(working_file, importer_config, parser, object_manager, request_user)

    import_response: ImporterObjectResponse = importer.start_import()

    return make_response(import_response.__dict__)
