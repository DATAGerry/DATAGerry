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
import json

from cmdb.database.utils import default
from cmdb.framework.exporter.format.base_exporter_format import BaseExporterFormat
from cmdb.framework.exporter.config.exporter_config_type_enum import ExporterConfigType
from cmdb.framework.rendering.render_result import RenderResult
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               JsonExportFormat - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class JsonExportFormat(BaseExporterFormat):
    """Extends: BaseExporterFormat"""
    FILE_EXTENSION = "json"
    LABEL = "JSON"
    MULTITYPE_SUPPORT = True
    ICON = "file-code"
    DESCRIPTION = "Export as JSON"
    ACTIVE = True


    def export(self, data: list[RenderResult], *args):
        """Exports data as .json file

        Args:
            data: The objects to be exported

        Returns:
            Json file containing the data
        """
        meta = False
        view = 'native'

        if args:
            meta = args[0].get("metadata", False)
            view = args[0].get('view', 'native')

        header = ['public_id', 'active', 'type_label']
        output = []

        for obj in data:
            # init columns
            columns = obj.fields
            multi_data_sections = []

            if len(obj.multi_data_sections) > 0:
                multi_data_sections = obj.multi_data_sections

            # Export only the shown fields chosen by the user
            if meta and view.upper() == ExporterConfigType.RENDER.name:
                _meta = json.loads(meta)
                header = _meta['header']
                columns = [x for x in columns if x['name'] in _meta['columns']]

            # init output element
            output_element = {}

            for head in header:
                head = 'object_id' if head == 'public_id' else head

                if head == 'type_label':
                    output_element.update({head: obj.type_information[head]})
                else:
                    output_element.update({head: obj.object_information[head]})

            # get object fields
            output_element.update({'fields': []})
            for field in columns:
                output_element['fields'].append({
                    'name': field.get('name'),
                    'value': BaseExporterFormat.summary_renderer(obj, field, view)
                })

            if len(multi_data_sections) > 0:
                output_element.update({'multi_data_sections': []})

                for index, mds in enumerate(multi_data_sections):
                    # set first level items
                    output_element['multi_data_sections'].append({
                        'section_id': mds.get('section_id'),
                        'highest_id': mds.get('highest_id')
                    })
                    output_element['multi_data_sections'][index].update({'values': []})

                    #set values
                    values = mds.get('values')

                    for val_index, value in enumerate(values):
                        output_element['multi_data_sections'][index]['values'].append({
                             'multi_data_id': value.get('multi_data_id')
                        })
                        output_element['multi_data_sections'][index]['values'][val_index].update({'data': []})

                        #set all data
                        data = value.get('data')
                        for data_set in data:
                            output_element['multi_data_sections'][index]['values'][val_index]['data'].append({
                                'name': data_set.get('name'),
                                'value': data_set.get('value')
                            })

            output.append(output_element)

        return json.dumps(output, default=default, ensure_ascii=False, indent=2)
