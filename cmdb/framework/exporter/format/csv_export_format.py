# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C)  becon GmbH
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
import csv
import io
import json

from cmdb.framework.exporter.format.base_exporter_format import BaseExporterFormat
from cmdb.framework.exporter.config.exporter_config_type_enum import ExporterConfigType
from cmdb.framework.rendering.render_result import RenderResult
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                CsvExportFormat - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class CsvExportFormat(BaseExporterFormat):
    """Extends: BaseExporterFormat"""
    FILE_EXTENSION = "csv"
    LABEL = "CSV"
    MULTITYPE_SUPPORT = False
    ICON = "file-csv"
    DESCRIPTION = "Export as CSV (only of the same type)"
    ACTIVE = True


    def export(self, data: list[RenderResult], *args):
        """ Exports data as .csv file

        Args:
            data: The objects to be exported
        Returns:
            Csv file containing the data
        """
        # init values
        header = ['public_id', 'active']
        columns = [] if not data else [x['name'] for x in data[0].fields]
        rows = []
        view = 'native'
        current_type_id = None

        # Export only the shown fields chosen by the user
        if args and args[0].get("metadata", False) and \
           args[0].get('view', 'native').upper() == ExporterConfigType.RENDER.name:

            _meta = json.loads(args[0].get("metadata", ""))
            view = args[0].get('view', 'native')
            header = _meta['header']
            columns = _meta['columns']

        for obj in data:
            # get type from first object and setup csv header
            if current_type_id is None:
                current_type_id = obj.type_information['type_id']

            # throw Exception if objects of different type are detected
            if current_type_id != obj.type_information['type_id']:
                #TODO: ERROR-FIX
                raise Exception({'message': 'CSV can export only object of the same type'})

            # get object fields as dict:
            obj_fields_dict = {}

            for field in obj.fields:
                obj_field_name = field.get('name')
                obj_fields_dict[obj_field_name] = BaseExporterFormat.summary_renderer(obj, field, view)

            # define output row
            row = []

            for head in header:
                head = 'object_id' if head == 'public_id' else head
                row.append(str(obj.object_information[head]))

            for name in columns:
                row.append(str(obj_fields_dict.get(name, None)))

            rows.append(row)

        return self.csv_writer([*header, *columns], rows)


    def csv_writer(self, header, rows, dialect=csv.excel):
        """TODO: ducoment"""
        csv_file = io.StringIO()
        writer = csv.writer(csv_file, dialect=dialect)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
        csv_file.seek(0)
        return csv_file
