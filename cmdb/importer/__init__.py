# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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

from cmdb.importer.importer_errors import ImporterLoadError, ParserLoadError
from cmdb.importer.parser_object import CsvObjectParser, JsonObjectParser, ExcelObjectParser
from cmdb.importer.importer_object import JsonObjectImporter, CsvObjectImporter, JsonObjectImporterConfig, \
    CsvObjectImporterConfig, ExcelObjectImporter, ExcelObjectImporterConfig

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

__OBJECT_IMPORTER__ = {
    'json': JsonObjectImporter,
    'csv': CsvObjectImporter
}

__OBJECT_IMPORTER_CONFIG__ = {
    'json': JsonObjectImporterConfig,
    'csv': CsvObjectImporterConfig
}

__OBJECT_PARSER__ = {
    'json': JsonObjectParser,
    'csv': CsvObjectParser
}


def load_importer_class(importer_type: str, importer_name: str):
    global __OBJECT_IMPORTER__
    __importer = {
        'object': __OBJECT_IMPORTER__
    }
    try:
        importer_class = __importer.get(importer_type).get(importer_name)
    except (IndexError, KeyError, ValueError, TypeError):
        raise ImporterLoadError(importer_type, importer_name)
    if not importer_class:
        raise ImporterLoadError(importer_type, importer_name)
    return importer_class


def load_importer_config_class(importer_type: str, importer_name: str):
    global __OBJECT_IMPORTER_CONFIG__
    __importer_config = {
        'object': __OBJECT_IMPORTER_CONFIG__
    }
    try:
        importer_config_class = __importer_config.get(importer_type).get(importer_name)
    except (IndexError, KeyError, ValueError, TypeError):
        raise ImporterLoadError(importer_type, importer_name)
    if not importer_config_class:
        raise ImporterLoadError(importer_type, importer_name)
    return importer_config_class


def load_parser_class(parser_type: str, parser_name: str):
    global __OBJECT_PARSER__
    __parser = {
            'object': __OBJECT_PARSER__
    }
    try:
        parser_class = __parser.get(parser_type).get(parser_name)
    except (IndexError, KeyError, ValueError, TypeError):
        raise ParserLoadError(parser_type, parser_name)
    if not parser_class:
        raise ParserLoadError(parser_type, parser_name)
    return parser_class
