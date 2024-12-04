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
import logging
from typing import Optional

from cmdb.framework.importer.configs.base_importer_config import BaseImporterConfig
from cmdb.framework.importer.responses.importer_object_response import ImporterObjectResponse
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 BaseImporter - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class BaseImporter:
    """Superclass for all importer"""

    def __init__(self, file, file_type: str, config: BaseImporterConfig = None):
        """
        Init constructor for importer classes
        Args:
            file: File instance, name, content or loaded path to file
            file_type: file type - used with content-type
            config: importer configuration
        """
        self.file = file
        self.file_type: str = file_type
        self.config = config


    def get_file_type(self) -> str:
        """Get the name of the file-type"""
        return self.file_type


    def get_file(self):
        """Get the loaded file"""
        return self.file


    def get_config(self) -> Optional[BaseImporterConfig]:
        """Get the configuration object"""
        return self.config


    def has_config(self) -> bool:
        """Check if importer has a config"""
        return bool(self.config)


    def start_import(self) -> ImporterObjectResponse:
        """Starting the import process"""
        raise NotImplementedError