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
from cmdb.exporter.config.config_base import BaseExportConfig
from cmdb.exporter.format.format_base import BaseExporterFormat


class BaseExportWriter:

    def __init__(self, export_format: BaseExporterFormat, export_config: BaseExportConfig, data):
        self.export_format = export_format
        self.export_config = export_config
        self.data = data

    def export(self):
        raise NotImplementedError
