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
from cmdb.models.object_model.cmdb_object import CmdbObject
from cmdb.importer.parser.json_object_parser import JsonObjectParser
from cmdb.importer.content_types import CSVContent
from cmdb.importer.importers.object_importer import ObjectImporter
from cmdb.importer.mapper.map_entry import MapEntry
from cmdb.importer.configs.csv_object_importer_config import CsvObjectImporterConfig
from cmdb.importer.responses.csv_object_parser_response import CsvObjectParserResponse
from cmdb.importer.helper.improve_object import ImproveObject
from cmdb.importer.responses.importer_object_response import ImporterObjectResponse

from cmdb.errors.manager.object_manager import ObjectManagerGetError
from cmdb.errors.importer import ImportRuntimeError, ParserRuntimeError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               CsvObjectImporter - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class CsvObjectImporter(ObjectImporter, CSVContent):
    """TODO: document"""

    def __init__(self,
                 file=None,
                 config: CsvObjectImporterConfig = None,
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
        """TODO: document"""
        try:
            possible_fields: list[dict] = kwargs['fields']
        except (KeyError, IndexError, ValueError) as err:
            raise ImportRuntimeError(f"[generate_object] can't import objects: {err}") from err

        working_object: dict = {
            'active': True,
            'type_id': self.get_config().get_type_id(),
            'fields': [],
            'author_id': self.request_user.get_public_id(),
            'version': '1.0.0',
            'creation_time': datetime.now(timezone.utc)
        }
        current_mapping = self.get_config().get_mapping()
        property_entries: list[MapEntry] = current_mapping.get_entries_with_option(query={'type': 'property'})
        field_entries: list[MapEntry] = current_mapping.get_entries_with_option(query={'type': 'field'})
        foreign_entries: list[MapEntry] = current_mapping.get_entries_with_option(query={'type': 'ref'})

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
            LOGGER.debug('[CSV] search for object based on %s', foreign_entry.__dict__)
            try:
                working_type_id = foreign_entry.get_option()['type_id']
            except (KeyError, IndexError):
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
                LOGGER.debug('[CSV] Ref query: %s', query)
                founded_objects: list[CmdbObject] = self.objects_manager.get_objects_by(**query)
                LOGGER.debug(founded_objects)

                if len(founded_objects) != 1:
                    continue

                working_object['fields'].append(
                    {'name': foreign_entry.get_name(),
                        'value': founded_objects[0].get_public_id()
                })

            except (ObjectManagerGetError, Exception) as err:
                LOGGER.error('[CSV] Error while loading ref object %s', err.message)
                continue

        return working_object


    def start_import(self) -> ImporterObjectResponse:
        try:
            parsed_response: CsvObjectParserResponse = self.parser.parse(self.file)
        except ParserRuntimeError as err:
            raise ImportRuntimeError(f"{err.message}") from err

        type_instance_fields: list[dict] = self.objects_manager.get_object_type(self.config.get_type_id()).get_fields()

        import_objects: list[dict] = self._generate_objects(parsed_response, fields=type_instance_fields)
        import_result: ImporterObjectResponse = self._import(import_objects)

        return import_result
