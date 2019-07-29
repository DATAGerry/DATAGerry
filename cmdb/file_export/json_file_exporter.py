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

import operator
from cmdb.file_export.file_exporter import FileExporter
from cmdb.interface.route_utils import make_response
from cmdb.object_framework.cmdb_object_manager import object_manager


class JsonFileExporter(FileExporter):

    def main(self):
        object_list = self.get_object_list()
        new_dict = {'public_id': 0, 'active': True, 'type': '', 'fields': []}
        s_keys = ['public_id', 'active', 'type_id', 'fields']
        filter_dict = []

        for obj in object_list:
            for k in s_keys:
                if k in obj.__dict__:
                    if k == 'type_id':
                        new_dict.update({'type': object_manager.get_type(obj.type_id).label})
                    else:
                        new_dict.update({k: obj.__dict__[k]})

            filter_dict.append(new_dict)
        self.set_response(make_response(filter_dict).data)
