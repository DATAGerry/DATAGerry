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
from typing import List

from cmdb.framework import CmdbObject
from cmdb.framework.cmdb_errors import ObjectManagerGetError
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.importer import JsonObjectParser
from cmdb.importer.importer_errors import ImportRuntimeError, ParserRuntimeError
from cmdb.importer.content_types import JSONContent, CSVContent, XLSXContent
from cmdb.importer.importer_base import ObjectImporter
from cmdb.importer.importer_config import ObjectImporterConfig
from cmdb.importer.importer_response import ImporterObjectResponse
from cmdb.importer.mapper import Mapping, MapEntry
from cmdb.importer.parser_object import JsonObjectParserResponse, CsvObjectParserResponse, ExcelObjectParserResponse
from cmdb.importer.improve_object import ImproveObject
from cmdb.user_management import UserModel

LOGGER = logging.getLogger(__name__)


class JsonObjectImporterConfig(ObjectImporterConfig, JSONContent):
    """Importer configuration for JSON files"""

    DEFAULT_MAPPING = {
        'properties': {
            'public_id': 'public_id',
            'active': 'active',
        },
        'fields': {
        }
    }

    MANUALLY_MAPPING = False

    def __init__(self, type_id: int, mapping: Mapping = None, start_element: int = 0, max_elements: int = 0,
                 overwrite_public: bool = True, *args, **kwargs):
        super(JsonObjectImporterConfig, self).__init__(type_id=type_id, mapping=mapping, start_element=start_element,
                                                       max_elements=max_elements, overwrite_public=overwrite_public)


class JsonObjectImporter(ObjectImporter, JSONContent):
    """Object importer for JSON"""

    def __init__(self, file=None, config: JsonObjectImporterConfig = None,
                 parser: JsonObjectParser = None, object_manager: CmdbObjectManager = None, request_user: UserModel = None):
        super(JsonObjectImporter, self).__init__(file=file, file_type=self.FILE_TYPE, config=config, parser=parser,
                                                 object_manager=object_manager, request_user=request_user)

    def generate_object(self, entry: dict, *args, **kwargs) -> dict:
        """create the native cmdb object from parsed content"""
        possible_fields: List[dict] = kwargs['fields']
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

        for entry_field in entry.get('fields'):
            field_exists = next((item for item in possible_fields if item["name"] == entry_field['name']), None)
            if field_exists:
                if 'checkbox' == field_exists['type']:
                    entry_field['value'] = ImproveObject.improve_boolean(entry_field['value'])
                entry_field['value'] = ImproveObject.improve_date(entry_field['value'])
                working_object.get('fields').append(entry_field)
        return working_object

    def _map_element(self, prop, entry: dict, working: dict):
        mapping: dict = self.config.get_mapping()
        map_ident: dict = mapping.get('properties')
        if map_ident:
            idx_ident = map_ident.get(prop)
            if idx_ident:
                value = entry.get(idx_ident)
                if value is not None:
                    working.update({prop: value})
        return working

    def start_import(self) -> ImporterObjectResponse:
        parsed_response: JsonObjectParserResponse = self.parser.parse(self.file)
        type_instance_fields: List = self.object_manager.get_type(self.config.get_type_id()).get_fields()

        import_objects: [dict] = self._generate_objects(parsed_response, fields=type_instance_fields)
        import_result: ImporterObjectResponse = self._import(import_objects)

        return import_result


class CsvObjectImporterConfig(ObjectImporterConfig, CSVContent):
    MANUALLY_MAPPING = True

    def __init__(self, type_id: int, mapping: list = None, start_element: int = 0, max_elements: int = 0,
                 overwrite_public: bool = True, *args, **kwargs):
        super(CsvObjectImporterConfig, self).__init__(type_id=type_id, mapping=mapping, start_element=start_element,
                                                      max_elements=max_elements, overwrite_public=overwrite_public)


class CsvObjectImporter(ObjectImporter, CSVContent):

    def __init__(self, file=None, config: CsvObjectImporterConfig = None,
                 parser: JsonObjectParser = None, object_manager: CmdbObjectManager = None, request_user: UserModel = None):
        super(CsvObjectImporter, self).__init__(file=file, file_type=self.FILE_TYPE, config=config, parser=parser,
                                                object_manager=object_manager, request_user=request_user)

    def generate_object(self, entry: dict, *args, **kwargs) -> dict:
        try:
            possible_fields: List[dict] = kwargs['fields']
        except (KeyError, IndexError, ValueError) as err:
            raise ImportRuntimeError(CsvObjectImporter, f'[CSV] cant import objects: {err}')

        working_object: dict = {
            'active': True,
            'type_id': self.get_config().get_type_id(),
            'fields': [],
            'author_id': self.request_user.get_public_id(),
            'version': '1.0.0',
            'creation_time': datetime.datetime.utcnow()
        }
        current_mapping = self.get_config().get_mapping()
        property_entries: List[MapEntry] = current_mapping.get_entries_with_option(query={'type': 'property'})
        field_entries: List[MapEntry] = current_mapping.get_entries_with_option(query={'type': 'field'})
        foreign_entries: List[MapEntry] = current_mapping.get_entries_with_option(query={'type': 'ref'})

        # field/properties improvement
        improve_object = ImproveObject(entry, property_entries, field_entries, possible_fields)
        entry = improve_object.improve_entry()

        # Insert properties
        for property_entry in property_entries:
            working_object.update({property_entry.get_name(): entry.get(property_entry.get_value())})

        # Validate insert fields
        for entry_field in field_entries:
            field_exists = next((item for item in possible_fields if item["name"] == entry_field.get_name()), None)
            if field_exists:
                working_object['fields'].append(
                    {'name': entry_field.get_name(),
                     'value': entry.get(entry_field.get_value())
                     })

        for foreign_entry in foreign_entries:
            LOGGER.debug(f'[CSV] search for object based on {foreign_entry.__dict__}')
            try:
                working_type_id = foreign_entry.get_option()['type_id']
            except (KeyError, IndexError) as err:
                continue
            try:
                query: dict = {
                    'type_id': working_type_id,
                    'fields': {
                        '$elemMatch': {
                            '$and': [
                                {'name': foreign_entry.get_option()['ref_name']},
                                {'value': entry.get(foreign_entry.get_value())},
                            ]
                        }
                    }
                }
                LOGGER.debug(f'[CSV] Ref query: {query}')
                founded_objects: List[CmdbObject] = self.object_manager.get_objects_by(**query)
                LOGGER.debug(founded_objects)
                if len(founded_objects) != 1:
                    continue
                else:
                    working_object['fields'].append(
                        {'name': foreign_entry.get_name(),
                         'value': founded_objects[0].get_public_id()
                    })

            except (ObjectManagerGetError, Exception) as err:
                LOGGER.error(f'[CSV] Error while loading ref object {err.message}')
                continue

        return working_object

    def start_import(self) -> ImporterObjectResponse:
        try:
            parsed_response: CsvObjectParserResponse = self.parser.parse(self.file)
        except ParserRuntimeError as pre:
            raise ImportRuntimeError(self.__class__.__name__, pre)

        type_instance_fields: List[dict] = self.object_manager.get_type(self.config.get_type_id()).get_fields()

        import_objects: [dict] = self._generate_objects(parsed_response, fields=type_instance_fields)
        import_result: ImporterObjectResponse = self._import(import_objects)

        return import_result


class ExcelObjectImporterConfig(ObjectImporterConfig, XLSXContent):
    MANUALLY_MAPPING = True

    def __init__(self, type_id: int, mapping: list = None, start_element: int = 0, max_elements: int = 0,
                 overwrite_public: bool = True, *args, **kwargs):
        super(ExcelObjectImporterConfig, self).__init__(type_id=type_id, mapping=mapping, start_element=start_element,
                                                        max_elements=max_elements, overwrite_public=overwrite_public)


class ExcelObjectImporter(ObjectImporter, XLSXContent):

    def __init__(self, file=None, config: ExcelObjectImporterConfig = None,
                 parser: JsonObjectParser = None, object_manager: CmdbObjectManager = None, request_user: UserModel = None):
        super(ExcelObjectImporter, self).__init__(file=file, file_type=self.FILE_TYPE, config=config, parser=parser,
                                                  object_manager=object_manager, request_user=request_user)

    def generate_object(self, entry: dict, *args, **kwargs) -> dict:
        try:
            possible_fields: List[dict] = kwargs['fields']
        except (KeyError, IndexError, ValueError) as err:
            raise ImportRuntimeError(CsvObjectImporter, f'[CSV] cant import objects: {err}')

        working_object: dict = {
            'active': True,
            'type_id': self.get_config().get_type_id(),
            'fields': [],
            'author_id': self.request_user.get_public_id(),
            'version': '1.0.0',
            'creation_time': datetime.datetime.utcnow()
        }
        current_mapping = self.get_config().get_mapping()
        property_entries: List[MapEntry] = current_mapping.get_entries_with_option(query={'type': 'property'})
        field_entries: List[MapEntry] = current_mapping.get_entries_with_option(query={'type': 'field'})

        # Insert properties
        for property_entry in property_entries:
            working_object.update({property_entry.get_name(): entry.get(property_entry.get_value())})

        # Improve insert object
        improve_object = ImproveObject(entry, field_entries, possible_fields)
        entry = improve_object.improve_entry()

        # Validate insert fields
        for field_entry in field_entries:
            if field_entry.get_name() not in possible_fields:
                continue
            working_object['fields'].append(
                {'name': field_entry.get_name(),
                 'value': entry.get(field_entry.get_value())
                 })

        return working_object

    def start_import(self) -> ImporterObjectResponse:
        try:
            parsed_response: ExcelObjectParserResponse = self.parser.parse(self.file)
        except ParserRuntimeError as pre:
            raise ImportRuntimeError(self.__class__.__name__, pre)

        LOGGER.debug(parsed_response)

        return ImporterObjectResponse('Nope')
