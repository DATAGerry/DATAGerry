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
from cmdb.importer.importer_config import ObjectImporterConfig, BaseImporterConfig
from cmdb.importer.parser_base import BaseObjectParser


class BaseImporter:
    """Superclass for all importer"""

    def __init__(self, file=None, file_type: str = None, config: BaseImporterConfig = None):
        self.file_type = file_type
        self.file = file
        self.config = config

    def get_file_type(self):
        return self.file_type

    def get_file(self):
        return self.file

    def start_import(self):
        raise NotImplementedError


class ObjectImporter(BaseImporter):
    """Superclass for object importers"""
    FILE_TYPE = ''
    CONTENT_TYPE = ''

    def __init__(self, file=None, config: ObjectImporterConfig = None,
                 parser: BaseObjectParser = None):
        self.parser = parser
        super(ObjectImporter, self).__init__(file=file, file_type=self.FILE_TYPE, config=config)

    def start_import(self):
        raise NotImplementedError


class TypeImporter(BaseImporter):
    """Superclass for type importers"""
    FILE_TYPE = ''
    DEFAULT_CONFIG = {}

    def __init__(self, file=None, config: dict = None):
        self.config = config
        super(TypeImporter, self).__init__(file=file, file_type=self.FILE_TYPE, config=config)

    def start_import(self):
        raise NotImplementedError
