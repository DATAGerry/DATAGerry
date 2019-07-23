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
        self.set_response(self.parse_to_xml(json.loads(make_response(self.get_object_list()).data)))

    def parse_to_xml(self, json_obj, line_spacing=""):
        result_list = list()
        json_obj_type = type(json_obj)

        if json_obj_type is list:
            for sub_elem in json_obj:
                result_list.append(self.parse_to_xml(sub_elem, line_spacing))
            return "\n".join(result_list)

        if json_obj_type is dict:
            for tag_name in json_obj:
                sub_obj = json_obj[tag_name]
                result_list.append("%s<%s>" % (line_spacing, tag_name))
                result_list.append(self.parse_to_xml(sub_obj, "\t" + line_spacing))
                result_list.append("%s</%s>" % (line_spacing, tag_name))
            return "\n".join(result_list)
        return "%s%s" % (line_spacing, json_obj)
