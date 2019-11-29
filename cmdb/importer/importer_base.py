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
"""
Module of basic importers
"""
import logging

from cmdb.framework import CmdbObject
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerInsertError, \
    ObjectManagerDeleteError
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.importer.importer_config import ObjectImporterConfig, BaseImporterConfig
from cmdb.importer.importer_response import BaseImporterResponse, ImporterObjectResponse, ImportFailedMessage, \
    ImportSuccessMessage
from cmdb.importer.parser_base import BaseObjectParser
from cmdb.importer.parser_response import ObjectParserResponse
from cmdb.user_management import User

LOGGER = logging.getLogger(__name__)


class BaseImporter:
    """Superclass for all importer"""

    def __init__(self, file, file_type: str, config: BaseImporterConfig = None):
        self.file_type = file_type
        self.file = file
        self.config = config

    def get_file_type(self):
        return self.file_type

    def get_file(self):
        return self.file

    def get_config(self):
        return self.config

    def start_import(self) -> BaseImporterResponse:
        raise NotImplementedError


class ObjectImporter(BaseImporter):
    """Superclass for object importers"""

    def __init__(self, file, file_type, config: ObjectImporterConfig = None,
                 parser: BaseObjectParser = None, object_manager: CmdbObjectManager = None, request_user: User = None):
        self.parser = parser
        if object_manager:
            self.object_manager = object_manager
        else:
            from cmdb.utils.system_reader import SystemConfigReader
            from cmdb.data_storage import DatabaseManagerMongo, MongoConnector
            object_manager = CmdbObjectManager(database_manager=DatabaseManagerMongo(
                MongoConnector(
                    **SystemConfigReader().get_all_values_from_section('Database')
                )
            ))
            self.object_manager = object_manager
        self.request_user = request_user
        super(ObjectImporter, self).__init__(file=file, file_type=file_type, config=config)

    def _generate_objects(self, parsed: ObjectParserResponse, *args, **kwargs) -> list:
        object_instance_list: [dict] = []
        for entry in parsed.entries:
            object_instance_list.append(self.generate_object(entry, *args, **kwargs))
        return object_instance_list

    def generate_object(self, entry, *args, **kwargs) -> dict:
        raise NotImplementedError

    def _import(self, import_objects: list) -> ImporterObjectResponse:
        run_config = self.config

        success_imports: [ImportSuccessMessage] = []
        failed_imports:  [ImportFailedMessage] = []

        current_import_index = run_config.start_element
        importer_counter = 0
        import_objects_length: int = len(import_objects)

        LOGGER.info(f'Starting import of {import_objects_length} objects')
        while current_import_index < import_objects_length:

            current_import_object: dict = import_objects[current_import_index]
            LOGGER.debug(f'Current working object: {current_import_object}')

            current_public_id: (int, None) = current_import_object.get('public_id')
            LOGGER.debug(f'Current working public id: {current_public_id}')

            # Object has PublicID and can not overwrite
            if current_public_id is not None and not run_config.overwrite_public:
                failed_imports.append(ImportFailedMessage(
                    error_message='Object import for object - has PublicID but not overwrite setting',
                    obj=current_import_object))
                current_import_index += 1
                continue

            # Object has no PublicID <- assign new
            elif not current_public_id:
                current_public_id = self.object_manager.get_new_id(CmdbObject.COLLECTION)
                LOGGER.debug(f'Assign new PublicID: {current_public_id}')
                current_import_object.update({'public_id': current_public_id})
            # else assign given PublicID
            else:
                current_public_id = current_import_object.get('public_id')
                LOGGER.debug(f'Assign given PublicID: {current_public_id}')

            # Insert data
            try:
                self.object_manager.get_object(current_public_id)
            except ObjectManagerGetError:
                try:
                    self.object_manager.insert_object(current_import_object)
                except ObjectManagerInsertError as err:
                    failed_imports.append(ImportFailedMessage(error_message=err.message, obj=current_import_object))
                    current_import_index += 1
                    continue
                else:
                    success_imports.append(ImportSuccessMessage(public_id=current_public_id, obj=current_import_object))
            else:
                try:
                    self.object_manager.delete_object(current_public_id, self.request_user)
                except ObjectManagerDeleteError as err:
                    failed_imports.append(ImportFailedMessage(error_message=err.message, obj=current_import_object))
                    current_import_index += 1
                    continue
                else:
                    try:
                        self.object_manager.insert_object(current_import_object)
                    except ObjectManagerInsertError as err:
                        failed_imports.append(ImportFailedMessage(error_message=err.message, obj=current_import_object))
                        current_import_index += 1
                        continue
                    else:
                        success_imports.append(
                            ImportSuccessMessage(public_id=current_public_id, obj=current_import_object))

            # check if still import valid
            current_import_index += 1
            if run_config.max_elements > 0 and (current_import_index >= run_config.max_elements):
                break

        return ImporterObjectResponse(
            message=f'Import of {importer_counter} objects',
            success_imports=success_imports,
            failed_imports=failed_imports
        )

    def start_import(self) -> ImporterObjectResponse:
        raise NotImplementedError


class TypeImporter(BaseImporter):
    """Superclass for type importers"""
    DEFAULT_CONFIG = {}

    def __init__(self, file, file_type, config: dict = None):
        self.config = config
        super(TypeImporter, self).__init__(file=file, file_type=file_type, config=config)

    def start_import(self) -> BaseImporterResponse:
        raise NotImplementedError
