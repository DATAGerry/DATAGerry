# DATAGERRY - OpenSource Enterprise CMDB
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


class BaseImporter:
    FILE_TYPE = ''

    def __init__(self, file_type: str, file=None):
        self.file_type = file_type
        self.file = file

    def get_file_type(self):
        return self.file_type

    def get_file(self):
        return self.file

    def exe_import(self):
        raise NotImplementedError


class BaseObjectImporter(BaseImporter):
    FILE_TYPE = ''
    DEFAULT_CONFIG = {}

    def __init__(self, file=None, config: dict = None):
        self.config = config
        super(BaseObjectImporter, self).__init__(file_type=self.FILE_TYPE, file=file)

    def get_config(self):
        return self.config

    def exe_import(self):
        raise NotImplementedError
