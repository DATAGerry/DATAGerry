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


class JsonFileExporter(FileExporter):

    def main(self):
        file_type = self.get_object_type()
        if file_type == 'object':
            data_list = self.get_object_by_id()
        elif file_type == 'type':
            data_list = self.get_type_by_id()
        else:
            data_list = self.get_all_objects_by_type_id()

        self.set_object_list(make_response(data_list).data)
