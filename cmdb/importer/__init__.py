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

from cmdb.importer.parser_object import CsvObjectParser, JsonObjectParser
from cmdb.importer.importer_object import JsonObjectImporter, CsvObjectImporter, JsonObjectImporterConfig

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

__OBJECT_IMPORTER__ = {
    'json': JsonObjectImporter,
    'csv': CsvObjectImporter
}

__OBJECT_IMPORTER_CONFIG__ = {
    'json': JsonObjectImporterConfig
}

__OBJECT_PARSER__ = {
    'csv': CsvObjectParser,
    'json': JsonObjectParser
}


class ImporterLoadError(CMDBError):
    def __init__(self, importer_type, importer_name):
        self.message = f'Could not load importer {importer_name} of type {importer_type}'
        super(ImporterLoadError, self).__init__()


class ParserLoadError(CMDBError):
    def __init__(self, parser_type, parser_name):
        self.message = f'Could not load parser {parser_name} of type {parser_type}'
        super(ParserLoadError, self).__init__()


def load_importer_class(importer_type: str, importer_name: str):
    __importer = {
        'object': {
            JsonObjectImporter.CONTENT_TYPE: JsonObjectImporter,
            CsvObjectImporter.CONTENT_TYPE: CsvObjectImporter
        }
    }
    try:
        importer_class = __importer.get(importer_type).get(importer_name)
    except (IndexError, KeyError, ValueError):
        raise ImporterLoadError(importer_type, importer_name)
    return importer_class


def load_importer_config_class(importer_type: str, importer_name: str):
    __importer_config = {
        'object': {
            JsonObjectImporterConfig.CONTENT_TYPE: JsonObjectImporterConfig,
        }
    }
    try:
        importer_config_class = __importer_config.get(importer_type).get(importer_name)
    except (IndexError, KeyError, ValueError):
        raise ImporterLoadError(importer_type, importer_name)
    return importer_config_class


def load_parser_class(parser_type: str, parser_name: str):
    __parser = {
        'object': {
            JsonObjectParser.CONTENT_TYPE: JsonObjectParser,
            CsvObjectParser.CONTENT_TYPE: CsvObjectParser
        }
    }
    try:
        parser_class = __parser.get(parser_type).get(parser_name)
    except (IndexError, KeyError, ValueError):
        raise ParserLoadError(parser_type, parser_name)
    return parser_class
