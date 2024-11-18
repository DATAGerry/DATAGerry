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

from cmdb.utils.helpers import load_class
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                          SupportedExporterExtension - CLASS                                          #
# -------------------------------------------------------------------------------------------------------------------- #
class SupportedExporterExtension:
    """Supported export extensions for exporting (csv, json, xlsx, xml)"""


    def __init__(self, extensions=None):
        """
        Constructor of SupportedExporterExtension
        Args:
            extensions: List of export extension
        """
        arguments = extensions if extensions else []
        self.extensions = [*["CsvExportFormat",
                             "JsonExportFormat",
                             "XlsxExportFormat",
                             "XmlExportFormat"], *arguments]

    def get_extensions(self):
        """Get list of supported export extension"""
        return self.extensions


    def convert_to(self):
        """Converts the supported export extension inside the list to a passed BaseExporterFormat list."""
        extension_list = []

        for type_element in self.get_extensions():
            type_element_class = load_class('cmdb.framework.exporter.format.' + type_element)

            extension_list.append({
                'extension': type_element,
                'label': type_element_class.LABEL,
                'icon': type_element_class.ICON,
                'multiTypeSupport': type_element_class.MULTITYPE_SUPPORT,
                'helperText': type_element_class.DESCRIPTION,
                'active': type_element_class.ACTIVE
            })

        return extension_list
