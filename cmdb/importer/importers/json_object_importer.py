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
import logging
from datetime import datetime, timezone

from cmdb.manager.objects_manager import ObjectsManager

from cmdb.models.user_model.user import UserModel
from cmdb.importer.parser.json_object_parser import JsonObjectParser
from cmdb.importer.content_types import JSONContent
from cmdb.importer.importers.object_importer import ObjectImporter
from cmdb.importer.responses.json_object_parser_response import JsonObjectParserResponse
from cmdb.importer.helper.improve_object import ImproveObject
from cmdb.importer.responses.importer_object_response import ImporterObjectResponse
from cmdb.importer.configs.json_object_importer_config import JsonObjectImporterConfig
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              JsonObjectImporter - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class JsonObjectImporter(ObjectImporter, JSONContent):
    """Object importer for JSON"""

    def __init__(self,
                 file=None,
                 config: JsonObjectImporterConfig = None,
                 parser: JsonObjectParser = None,
                 objects_manager: ObjectsManager = None,
                 request_user: UserModel = None):
        super().__init__(
            file=file,
            file_type=self.FILE_TYPE,
            config=config,
            parser=parser,
            objects_manager=objects_manager,
            request_user=request_user
        )


    def generate_object(self, entry: dict, *args, **kwargs) -> dict:
        """create the native cmdb object from parsed content"""
        possible_fields: list[dict] = kwargs['fields']
        mapping: dict = self.config.get_mapping()

        working_object: dict = {
            'type_id': self.config.get_type_id(),
            'fields': [],
            'author_id': self.request_user.get_public_id(),
            'version': '1.0.0',
            'creation_time': datetime.now(timezone.utc)
        }

        if 'multi_data_sections' in entry:
            working_object['multi_data_sections'] = entry['multi_data_sections']

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
        """TODO: document"""
        parsed_response: JsonObjectParserResponse = self.parser.parse(self.file)
        type_instance_fields: list = self.objects_manager.get_object_type(self.config.get_type_id()).get_fields()

        import_objects: list[dict] = self._generate_objects(parsed_response, fields=type_instance_fields)
        import_result: ImporterObjectResponse = self._import(import_objects)

        return import_result
