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
from cmdb.framework.importer.parser.csv_object_parser import CsvObjectParser
from cmdb.framework.importer.parser.json_object_parser import JsonObjectParser
from cmdb.framework.importer.importers.csv_object_importer import CsvObjectImporter
from cmdb.framework.importer.configs.csv_object_importer_config import CsvObjectImporterConfig
from cmdb.framework.importer.importers.json_object_importer import JsonObjectImporter
from cmdb.framework.importer.configs.json_object_importer_config import JsonObjectImporterConfig

from cmdb.errors.importer import ImporterLoadError, ParserLoadError
# -------------------------------------------------------------------------------------------------------------------- #

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
    """TODO: document"""

    __importer = {
        'object': __OBJECT_IMPORTER__
    }

    try:
        importer_class = __importer.get(importer_type).get(importer_name)
    except (IndexError, KeyError, ValueError, TypeError) as err:
        raise ImporterLoadError(f"[{importer_type} - {importer_name}]: {str(err)}") from err

    if not importer_class:
        raise ImporterLoadError(f"[{importer_type} - {importer_name}]: No importer_class!")

    return importer_class


def load_importer_config_class(importer_type: str, importer_name: str):
    """TODO: document"""

    __importer_config = {
        'object': __OBJECT_IMPORTER_CONFIG__
    }
    try:
        importer_config_class = __importer_config.get(importer_type).get(importer_name)
    except (IndexError, KeyError, ValueError, TypeError) as err:
        raise ImporterLoadError(f"[{importer_type} - {importer_name}]: {str(err)}") from err
    if not importer_config_class:
        raise ImporterLoadError(f"[{importer_type} - {importer_name}]: No importer_config_class!")
    return importer_config_class


def load_parser_class(parser_type: str, parser_name: str):
    """TODO: document"""

    __parser = {
            'object': __OBJECT_PARSER__
    }
    try:
        parser_class = __parser.get(parser_type).get(parser_name)
    except (IndexError, KeyError, ValueError, TypeError) as err:
        raise ParserLoadError(f"[{parser_type} - {parser_name}]: {str(err)}") from err

    if not parser_class:
        raise ParserLoadError(f"[{parser_type} - {parser_name}]: No parser_class!")

    return parser_class
