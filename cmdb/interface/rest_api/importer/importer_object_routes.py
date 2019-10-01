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

from flask import request, abort
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from cmdb.importer import CsvObjectImporter
from cmdb.importer.parser_base import BaseObjectParser
from cmdb.importer.parser_errors import ParserError
from cmdb.importer.parser_result import ParserResult
from cmdb.interface.rest_api.import_routes import importer_blueprint
from cmdb.interface.route_utils import NestedBlueprint, make_response
from cmdb.importer import __OBJECT_IMPORTER__, __OBJECT_PARSER__

LOGGER = logging.getLogger(__name__)
try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

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


@importer_object_blueprint.route('/parser/<string:parser_type>/', methods=['POST'])
@importer_object_blueprint.route('/parser/<string:parser_type>', methods=['POST'])
def parse_object_file(parser_type):
    parse_file: FileStorage = request.files['file']
    parser_config = None if request.args.to_dict() == {} else request.args.to_dict()

    if 'file' not in request.files:
        LOGGER.error('File was not provided')
        return abort(400)
    try:
        parser: BaseObjectParser = __OBJECT_PARSER__[parser_type](parser_config)
    except (IndexError, KeyError) as err:
        LOGGER.error('Parser could not be init')
        return abort(400)
    if parse_file.content_type != parser.CONTENT_TYPE:
        LOGGER.error('Wrong content type!')
        return abort(400)

    filename = secure_filename(parse_file.filename)
    parse_file.save(f'/tmp/{filename}')

    try:
        parsed_output: ParserResult = parser.parse(filename)
    except ParserError as err:
        LOGGER.error(err)
        parse_file.close()
        return abort(500)
    parse_file.close()

    return make_response(parsed_output.__dict__)


@importer_object_blueprint.route('/csv/', methods=['POST'])
@importer_object_blueprint.route('/csv', methods=['POST'])
def import_csv_objects():
    import_file = request.files['file']

    if 'file' not in request.files:
        return abort(400)
    if import_file.content_type != CsvObjectImporter.CONTENT_TYPE:
        return abort(400)

    return make_response("test")
