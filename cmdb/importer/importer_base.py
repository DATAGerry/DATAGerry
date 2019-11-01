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
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.importer.importer_config import ObjectImporterConfig, BaseImporterConfig
from cmdb.importer.importer_response import BaseImporterResponse, ImporterObjectResponse
from cmdb.importer.parser_base import BaseObjectParser
from cmdb.importer.parser_response import ObjectParserResponse
from cmdb.user_management import User


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

    def generate_objects(self, parsed: ObjectParserResponse) -> list:
        raise NotImplementedError

    def generate_object(self, entry) -> dict:
        raise NotImplementedError

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
