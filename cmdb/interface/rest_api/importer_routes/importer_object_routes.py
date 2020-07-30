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

from cmdb.framework.cmdb_errors import ObjectManagerGetError
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.importer import load_parser_class, load_importer_class, __OBJECT_IMPORTER__, __OBJECT_PARSER__, \
    __OBJECT_IMPORTER_CONFIG__, load_importer_config_class, ParserLoadError, ImporterLoadError
from cmdb.importer.importer_errors import ImportRuntimeError, ParserRuntimeError
from cmdb.importer.importer_config import ObjectImporterConfig
from cmdb.importer.importer_response import ImporterObjectResponse
from cmdb.importer.parser_base import BaseObjectParser
from cmdb.interface.rest_api.import_routes import importer_blueprint
from cmdb.interface.route_utils import make_response, insert_request_user, login_required, \
    right_required
from cmdb.interface.blueprint import NestedBlueprint
from cmdb.interface.rest_api.importer_routes.importer_route_utils import get_file_in_request, \
    get_element_from_data_request, generate_parsed_output
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
@login_required
def get_importer():
    importer_response = []
    for importer in __OBJECT_IMPORTER__:
        importer_response.append({
            'name': __OBJECT_IMPORTER__.get(importer).FILE_TYPE,
            'content_type': __OBJECT_IMPORTER__.get(importer).CONTENT_TYPE,
            'icon': __OBJECT_IMPORTER__.get(importer).ICON
        })

    return make_response(importer_response)


@importer_object_blueprint.route('/importer/config/<string:importer_type>/', methods=['GET'])
@importer_object_blueprint.route('/importer/config<string:importer_type>', methods=['GET'])
@login_required
def get_default_importer_config(importer_type):
    try:
        importer: ObjectImporterConfig = __OBJECT_IMPORTER_CONFIG__[importer_type]
    except IndexError:
        return abort(404)
    return make_response({'manually_mapping': importer.MANUALLY_MAPPING})


@importer_object_blueprint.route('/parser/', methods=['GET'])
@importer_object_blueprint.route('/parser', methods=['GET'])
@login_required
def get_parser():
    parser = [parser for parser in __OBJECT_PARSER__]
    return make_response(parser)


# @importer_object_blueprint.route('/parser/default', defaults={'importer_type': 'json'}, methods=['GET'])
# @importer_object_blueprint.route('/parser/default/', defaults={'importer_type': 'json'}, methods=['GET'])
@importer_object_blueprint.route('/parser/default/<string:parser_type>', methods=['GET'])
@importer_object_blueprint.route('/parser/default/<string:parser_type>/', methods=['GET'])
@login_required
def get_default_parser_config(parser_type: str):
    try:
        parser: BaseObjectParser = __OBJECT_PARSER__[parser_type]
    except IndexError:
        return abort(404)
    return make_response(parser.DEFAULT_CONFIG)


@importer_object_blueprint.route('/parse/', methods=['POST'])
@importer_object_blueprint.route('/parse', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.import.object.*')
def parse_objects(request_user: User):
    # Check if file exists
    request_file: FileStorage = get_file_in_request('file', request.files)
    # Load parser config
    parser_config: dict = get_element_from_data_request('parser_config', request) or {}
    # Load file format
    file_format = request.form.get('file_format', None)
    try:
        parsed_output = generate_parsed_output(request_file, file_format, parser_config).output()
    except ParserRuntimeError as pre:
        return abort(500, pre.message)
    return make_response(parsed_output)


@importer_object_blueprint.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.import.object.*')
def import_objects(request_user: User):
    # Check if file exists
    if not request.files:
        return abort(400, 'No import file was provided')
    request_file: FileStorage = get_file_in_request('file', request.files)

    filename = secure_filename(request_file.filename)
    working_file = f'/tmp/{filename}'
    request_file.save(working_file)

    # Load file format
    file_format = request.form.get('file_format', None)

    # Load parser config
    parser_config: dict = get_element_from_data_request('parser_config', request) or {}
    if parser_config == {}:
        LOGGER.info('No parser config was provided - using default parser config')

    # Check for importer config
    importer_config_request: dict = get_element_from_data_request('importer_config', request) or None
    if not importer_config_request:
        return abort(400, 'No import config was provided')

    # Check if type exists
    try:
        object_manager.get_type(public_id=importer_config_request.get('type_id'))
    except ObjectManagerGetError as err:
        return abort(404, err.message)

    # Load parser
    try:
        parser_class = load_parser_class('object', file_format)
    except ParserLoadError as ple:
        return abort(406, ple.message)
    parser = parser_class(parser_config)

    LOGGER.info(f'Parser {parser_class} was loaded')

    # Load importer config
    try:
        importer_config_class = load_importer_config_class('object', file_format)
    except ImporterLoadError as ile:
        return abort(406, ile.message)
    importer_config = importer_config_class(**importer_config_request)
    LOGGER.debug(importer_config_request)
    # Load importer
    try:
        importer_class = load_importer_class('object', file_format)
    except ImporterLoadError as ile:
        return abort(406, ile.message)
    importer = importer_class(working_file, importer_config, parser, object_manager, request_user)
    LOGGER.info(f'Importer {importer_class} was loaded')

    try:
        import_response: ImporterObjectResponse = importer.start_import()
    except ImportRuntimeError as ire:
        LOGGER.error(f'Error while importing objects: {ire.message}')
        return abort(500, ire.message)

    # close request file
    request_file.close()

    return make_response(import_response)
