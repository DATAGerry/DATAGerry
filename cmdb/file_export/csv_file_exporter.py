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
from flask import abort

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception


class CsvFileExporter(FileExporter):

    def main(self):
        self.set_response(self.parse_to_csv(data_list=self.get_object_list()))

    def parse_to_csv(self, data_list):
        header = ['public_id', 'active']
        rows = [',']
        run_into = True
        publ_id = data_list[0].type_id

        for obj in data_list:

            if publ_id != obj.type_id:
                raise abort(400, {'message': 'CSV can export only object of the same type'})

            fields = obj.fields
            row = [str(obj.public_id), str(obj.active)]

            for key in fields:
                if run_into:
                    header.append(key.get('name'))
                row.append(str(key.get('value')))
            rows.append(','.join(row))
            run_into = False

        return ','.join(header) + '\n'.join(rows)
