# dataGerry - OpenSource Enterprise CMDB
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

import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
from cmdb.file_export.file_exporter import FileExporter
from cmdb.interface.route_utils import make_response
from cmdb.object_framework.cmdb_object_manager import object_manager


class XmlFileExporter(FileExporter):

    def main(self):
        self.set_response(self.parse_to_xml(json.loads(make_response(self.get_object_list()).data)))

    def parse_to_xml(self, json_obj):
        # object list
        cmdb_object_list = ET.Element('objects')

        # objects
        for obj in json_obj:
            # object
            cmdb_object = ET.SubElement(cmdb_object_list, 'object')
            cmdb_object_meta = ET.SubElement(cmdb_object, 'meta')
            # meta: public
            cmdb_object_meta_id = ET.SubElement(cmdb_object_meta, 'public_id')
            cmdb_object_meta_id.text = str(obj['public_id'])
            # meta: active
            cmdb_object_meta_active = ET.SubElement(cmdb_object_meta, 'active')
            cmdb_object_meta_active.text = str(obj['active'])
            # meta: type
            cmdb_object_meta_type = ET.SubElement(cmdb_object_meta, 'type')
            cmdb_object_meta_type.text = object_manager.get_type(obj['type_id']).label
            # fields
            cmdb_object_fields = ET.SubElement(cmdb_object, 'fields')
            for curr in obj['fields']:
                # fields: content
                field_attribs = {}
                field_attribs["name"] = str(curr['name'])
                field_attribs["value"] = str(curr['value'])
                ET.SubElement(cmdb_object_fields, "field", field_attribs)

        # return xml as string (pretty printed)
        return xml.dom.minidom.parseString(ET.tostring(cmdb_object_list, encoding='unicode', method='xml')).toprettyxml()
