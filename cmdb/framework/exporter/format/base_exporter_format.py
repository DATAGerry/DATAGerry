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
from cmdb.framework.exporter.config.exporter_config_type_enum import ExporterConfigType
# -------------------------------------------------------------------------------------------------------------------- #

class BaseExporterFormat:
    """TODO: document"""
    FILE_EXTENSION = None
    LABEL = None
    MULTITYPE_SUPPORT = False
    ICON = None
    DESCRIPTION = None
    ACTIVE = None


    def __init__(self, file_name=''):
        self.file_name = f'{file_name}.{self.FILE_EXTENSION}'


    def export(self, data, *args):
        """TODO: document"""


    @staticmethod
    def summary_renderer(obj, field, view: str = 'native') -> str:
        """TODO: ducoment"""
        # Export only the shown fields chosen by the user
        if view.upper() == ExporterConfigType.RENDER.name and field.get('type') == 'ref':
            summary_line = f'{obj.type_information["type_label"]} #{obj.type_information["type_id"]}  '
            first = True
            reference = field.get('reference')
            summaries = [] if not reference else reference.get('summaries')

            for line in summaries:
                if first:
                    summary_line += f'{line["value"]}'
                    first = False
                else:
                    summary_line += f' | {line["value"]}'
            return summary_line

        return field.get('value', None)
