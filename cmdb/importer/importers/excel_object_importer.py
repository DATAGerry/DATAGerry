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
from cmdb.importer.content_types import XLSXContent
from cmdb.importer.importers.object_importer import ObjectImporter
from cmdb.importer.configs.excel_object_importer_config import ExcelObjectImporterConfig
from cmdb.importer.mapper.map_entry import MapEntry
from cmdb.importer.responses.excel_object_parser_response import ExcelObjectParserResponse
from cmdb.importer.helper.improve_object import ImproveObject
from cmdb.importer.responses.importer_object_response import ImporterObjectResponse

from cmdb.errors.importer import ImportRuntimeError, ParserRuntimeError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              ExcelObjectImporter - CLASS                                             #
# -------------------------------------------------------------------------------------------------------------------- #
class ExcelObjectImporter(ObjectImporter, XLSXContent):
    """TODO: document"""

    def __init__(self,
                 file=None,
                 config: ExcelObjectImporterConfig = None,
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
        try:
            possible_fields: list[dict] = kwargs['fields']
        except (KeyError, IndexError, ValueError) as err:
            raise ImportRuntimeError(f"[generate_object] cant import objects: {str(err)}") from err

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

        # Insert properties
        for property_entry in property_entries:
            working_object.update({property_entry.get_name(): entry.get(property_entry.get_value())})

        # Improve insert object
        # @NaN added property_entries to this function, needs check
        improve_object = ImproveObject(entry, property_entries, field_entries, possible_fields)
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
        except ParserRuntimeError as err:
            raise ImportRuntimeError(f"{err.message}") from err

        LOGGER.debug(parsed_response)

        return ImporterObjectResponse('Nope')
