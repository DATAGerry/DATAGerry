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
"""Module of basic importers"""
from datetime import datetime, timezone
import logging
from flask import current_app

from cmdb.manager.objects_manager import ObjectsManager
from cmdb.manager.query_builder.builder_parameters import BuilderParameters

from cmdb.models.user_model.user import UserModel
from cmdb.models.object_model.cmdb_object import CmdbObject
from cmdb.framework.results import IterationResult
from cmdb.framework.importer.importers.base_importer import BaseImporter
from cmdb.framework.importer.configs.object_importer_config import ObjectImporterConfig
from cmdb.framework.importer.responses.importer_object_response import ImporterObjectResponse
from cmdb.framework.importer.messages.import_failed_message import ImportFailedMessage
from cmdb.framework.importer.messages.import_success_message import ImportSuccessMessage
from cmdb.framework.importer.parser.base_object_parser import BaseObjectParser
from cmdb.framework.importer.responses.object_parser_response import ObjectParserResponse

from cmdb.errors.manager.object_manager import ObjectManagerDeleteError,\
                                               ObjectManagerInsertError,\
                                               ObjectManagerGetError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                ObjectImporter - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectImporter(BaseImporter):
    """Superclass for object importers"""

    def __init__(self,
                 file,
                 file_type,
                 config: ObjectImporterConfig = None,
                 parser: BaseObjectParser = None,
                 objects_manager: ObjectsManager = None,
                 request_user: UserModel = None):
        """
        Basic importer super class for object imports
        Normally should be started by start_import
        Args:
            file: File instance, name, content or loaded path to file
            file_type: file type - used with content-type
            config: importer configuration
            parser: the parser instance based on content-type
            request_user: the instance of the started user
        """
        self.parser = parser
        self.objects_manager = objects_manager
        self.request_user = request_user

        super().__init__(file=file, file_type=file_type, config=config)


    def _generate_objects(self, parsed: ObjectParserResponse, *args, **kwargs) -> list:
        """Generate a list of all data from the parser.
        The implementation of the object generation should be written in the sub class"""
        object_instance_list: list[dict] = []

        for entry in parsed.entries:
            object_instance_list.append(self.generate_object(entry, *args, **kwargs))

        return object_instance_list


    def generate_object(self, entry, *args, **kwargs) -> dict:
        """Generation of the CMDB-Objects based on the parser response
        and the imported fields"""
        raise NotImplementedError


    def _import(self, import_objects: list) -> ImporterObjectResponse:
        """Basic import wrapper - starting the import process
        Args:
            import_objects: list of all objects for import - or output of _generate_objects()
        """


        run_config = self.get_config()

        success_imports: list[ImportSuccessMessage] = []
        failed_imports: list[ImportFailedMessage] = []

        current_import_index = run_config.start_element
        importer_counter = 0
        import_objects_length: int = len(import_objects)

        while current_import_index < import_objects_length:
            current_import_object: dict = import_objects[current_import_index]
            current_public_id: int = current_import_object.get('public_id')

            # Object has PublicID and can not overwrite
            if current_public_id is not None and not run_config.overwrite_public:
                failed_imports.append(ImportFailedMessage(
                    error_message='Object import for object - has PublicID but not overwrite setting',
                    obj=current_import_object))
                current_import_index += 1
                continue

            # Object has no PublicID <- assign new
            if not current_public_id:
                current_public_id = self.objects_manager.get_new_object_public_id()
                current_import_object.update({'public_id': current_public_id})
            # else assign given PublicID
            else:
                current_public_id = current_import_object.get('public_id')

            # Insert data
            try:
                existing = self.objects_manager.get_object(current_public_id)
                current_import_object['creation_time'] = existing.creation_time
                current_import_object['last_edit_time'] = datetime.now(timezone.utc)
            except ObjectManagerGetError:
                try:
                    if current_app.cloud_mode:
                        if self.check_config_item_limit_reached(self.request_user, self.objects_manager):
                            raise ObjectManagerInsertError("Config item limit reached!")

                    self.objects_manager.insert_object(current_import_object)
                except ObjectManagerInsertError as err:
                    failed_imports.append(ImportFailedMessage(error_message=err.message, obj=current_import_object))
                    current_import_index += 1
                    continue
                else:
                    success_imports.append(ImportSuccessMessage(public_id=current_public_id, obj=current_import_object))
            else:
                try:
                    self.objects_manager.delete_object(current_public_id, self.request_user)
                except ObjectManagerDeleteError as err:
                    failed_imports.append(ImportFailedMessage(error_message=err.message, obj=current_import_object))
                    current_import_index += 1
                    continue
                else:
                    try:
                        if current_app.cloud_mode:
                            if self.check_config_item_limit_reached(self.request_user, self.objects_manager):
                                raise ObjectManagerInsertError("Config item limit reached")

                        self.objects_manager.insert_object(current_import_object)
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
        """Starting the import process.
        Should call the _import method"""
        raise NotImplementedError


    def check_config_item_limit_reached(self, request_user: UserModel, objects_manager: ObjectsManager) -> bool:
        """TODO: document"""

        builder_params = BuilderParameters({})
        iteration_result: IterationResult[CmdbObject] = objects_manager.iterate(builder_params)

        objects_count = iteration_result.total

        return objects_count >= request_user.config_items_limit
