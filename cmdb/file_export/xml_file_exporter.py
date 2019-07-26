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

from cmdb.file_export.file_exporter import FileExporter
from cmdb.interface.route_utils import make_response
import json


class XmlFileExporter(FileExporter):

    def main(self):
        self.set_response(self.new_parser(json.loads(make_response(self.get_object_list()).data)))

    def parse_to_xml(self, json_obj):

        # toDo: write as xml.etree.ElementTree
        header_tag = list()

        for obj in json_obj:
            public_id_tag = "<%s>%s</%s>\n" % ('public_id', obj['public_id'], 'public_id')
            active_tag = "<%s>%s</%s>\n" % ('active', obj['active'], 'active')
            type_tag = "<%s>%s</%s>\n" % ('type', str(obj['type_id']), 'type')
            meta_tag = ("<%s>%s</%s>\n" % ('meta', '\n\t' + public_id_tag + active_tag + type_tag, 'meta'))

            for curr in obj['fields']:
                field = "<%s name='%s' value='%s' />\n" % ('field', curr['name'], curr['value'])
                fields_tag = ("<%s>%s</%s>\n" % ('fields', '\n\t' + field, 'fields'))

            object_tag = ("<%s>%s</%s>\n" % ('object', '\n\t' + meta_tag + fields_tag, 'object'))

        header_tag.append("<?xml version='1.0'?> \n <%s>%s</%s>" % ('objects', '\n\t' + object_tag, 'objects'))
        return header_tag
