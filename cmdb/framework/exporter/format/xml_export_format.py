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
import xml.dom.minidom
import xml.etree.ElementTree as ET

from cmdb.framework.exporter.format.base_exporter_format import BaseExporterFormat
from cmdb.framework.exporter.config.exporter_config_type_enum import ExporterConfigType
from cmdb.framework.rendering.render_result import RenderResult
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                XmlExportFormat - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class XmlExportFormat(BaseExporterFormat):
    """TODO: ducoment"""
    FILE_EXTENSION = "xml"
    LABEL = "XML"
    MULTITYPE_SUPPORT = True
    ICON = "file-alt"
    DESCRIPTION = "Export as XML"
    ACTIVE = True


    def export(self, data: list[RenderResult], *args):
        """Exports object_list as .xml file

        Args:
            data: The objects to be exported

        Returns:
            Xml file containing the data
        """
        # init values
        header = ['public_id', 'active', 'type_label']
        columns = [] if not data else [x['name'] for x in data[0].fields]
        view = 'native'

        # Export only the shown fields chosen by the user
        if args and args[0].get("metadata", False) and \
           args[0].get('view', 'native').upper() == ExporterConfigType.RENDER.name:

            _meta = json.loads(args[0].get("metadata", ""))
            view = args[0].get('view', 'native')
            header = _meta['header']
            columns = _meta['columns']

        # object list
        cmdb_object_list = ET.Element('objects')

        for obj in data:
            # get object fields as dict:
            obj_fields_dict = {}
            for field in obj.fields:
                obj_field_name = field.get('name')
                obj_fields_dict[obj_field_name] = BaseExporterFormat.summary_renderer(obj, field, view)

            # xml output: object
            cmdb_object = ET.SubElement(cmdb_object_list, 'object')
            cmdb_object_meta = ET.SubElement(cmdb_object, 'meta')

            # xml output meta: header
            for head in header:
                head = 'object_id' if head == 'public_id' else head
                if head == 'type_label':
                    cmdb_object_meta_type = ET.SubElement(cmdb_object_meta, 'type')
                    cmdb_object_meta_type.text = obj.type_information['type_label']
                else:
                    cmdb_object_meta_id = ET.SubElement(cmdb_object_meta, head)
                    cmdb_object_meta_id.text = str(obj.object_information[head])

            # xml output: fields
            cmdb_object_fields = ET.SubElement(cmdb_object, 'fields')

            # walk over all type fields and add object field values
            for field in columns:
                field_attribs = {
                    'name': str(field),
                    'value': str(obj_fields_dict.get(field))
                }
                ET.SubElement(cmdb_object_fields, "field", field_attribs)

        # return xml as string (pretty printed)
        return xml.dom.minidom.parseString(
            ET.tostring(cmdb_object_list, encoding='unicode', method='xml')).toprettyxml()
