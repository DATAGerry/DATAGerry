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
import datetime

from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.importer import JsonObjectParser, CsvObjectParser
from cmdb.importer.content_types import JSONContent, CSVContent
from cmdb.importer.importer_base import ObjectImporter
from cmdb.importer.importer_config import ObjectImporterConfig, FieldMapperMode
from cmdb.importer.importer_response import ImporterObjectResponse
from cmdb.importer.parser_object import JsonObjectParserResponse, CsvObjectParserResponse
from cmdb.importer.parser_response import ObjectParserResponse
from cmdb.user_management import User

LOGGER = logging.getLogger(__name__)


class JsonObjectImporterConfig(ObjectImporterConfig, JSONContent):
    MANUALLY_MAPPING = False
    DEFAULT_FIELD_MAPPER_VALUE = FieldMapperMode.MATCH
    DEFAULT_FIELD_MAPPER: DEFAULT_FIELD_MAPPER_VALUE = DEFAULT_FIELD_MAPPER_VALUE.value
    DEFAULT_MAPPING = {
        'properties': {
            'public_id': 'public_id',
            'active': 'active',
        },
        'field_mode': DEFAULT_FIELD_MAPPER,
        'fields': {
        }
    }

    def __init__(self, type_id: int, mapping: dict = None, start_element: int = 0, max_elements: int = 0,
                 overwrite_public: bool = True, *args, **kwargs):
        super(JsonObjectImporterConfig, self).__init__(type_id=type_id, mapping=mapping, start_element=start_element,
                                                       max_elements=max_elements, overwrite_public=overwrite_public)


class JsonObjectImporter(ObjectImporter, JSONContent):

    def __init__(self, file=None, config: JsonObjectImporterConfig = None,
                 parser: JsonObjectParser = None, object_manager: CmdbObjectManager = None, request_user: User = None):
        super(JsonObjectImporter, self).__init__(file=file, file_type=self.FILE_TYPE, config=config, parser=parser,
                                                 object_manager=object_manager, request_user=request_user)

    def generate_object(self, entry: dict) -> dict:
        mapping: dict = self.config.get_mapping()
        working_object: dict = {
            'type_id': self.config.get_type_id(),
            'fields': [],
            'author_id': self.request_user.get_public_id(),
            'version': '1.0.0',
            'creation_time': datetime.datetime.utcnow()
        }
        map_properties = mapping.get('properties')
        for prop in map_properties:
            working_object = self._map_element(prop, entry, working_object)

        working_object.update({'fields': entry.get('fields')})
        return working_object

    def _map_element(self, prop, entry: dict, working: dict):
        mapping: dict = self.config.get_mapping()
        map_ident: dict = mapping.get('properties')
        if map_ident:
            idx_ident = map_ident.get(prop)
            if idx_ident:
                value = entry.get(idx_ident)
                if value:
                    working.update({prop: value})
        return working

    def start_import(self) -> ImporterObjectResponse:
        parsed_response: JsonObjectParserResponse = self.parser.parse(self.file)
        import_objects: [dict] = self._generate_objects(parsed_response)
        import_result: ImporterObjectResponse = self._import(import_objects)

        return import_result


class CsvObjectImporterConfig(ObjectImporterConfig, JSONContent):
    MANUALLY_MAPPING = True
    DEFAULT_FIELD_MAPPER_VALUE = FieldMapperMode.MATCH
    DEFAULT_FIELD_MAPPER: DEFAULT_FIELD_MAPPER_VALUE = DEFAULT_FIELD_MAPPER_VALUE.value
    DEFAULT_MAPPING = {
        'properties': {
            'public_id': 'public_id',
            'active': 'active',
        },
        'field_mode': DEFAULT_FIELD_MAPPER,
        'fields': {
        }
    }

    def __init__(self, type_id: int, mapping: dict = None, start_element: int = 0, max_elements: int = 0,
                 overwrite_public: bool = True, *args, **kwargs):
        super(CsvObjectImporterConfig, self).__init__(type_id=type_id, mapping=mapping, start_element=start_element,
                                                      max_elements=max_elements, overwrite_public=overwrite_public)


class CsvObjectImporter(ObjectImporter, CSVContent):

    def __init__(self, file=None, config: CsvObjectImporterConfig = None,
                 parser: CsvObjectParser = None):
        super(CsvObjectImporter, self).__init__(file=file, config=config, parser=parser)

    def generate_object(self, entry: dict) -> dict:
        return entry

    def start_import(self) -> ImporterObjectResponse:
        parsed_response: CsvObjectParserResponse = self.parser.parse(self.file)
        import_objects: [dict] = self._generate_objects(parsed_response)
        LOGGER.debug(f'CSV Object generation: \n {import_objects}')
        # import_result: ImporterObjectResponse = self._import(import_objects)

        return None
