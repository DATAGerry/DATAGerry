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

import logging

from cmdb.importer import JsonObjectParser, CsvObjectParser
from cmdb.importer.importer_base import ObjectImporter
from cmdb.importer.importer_config import ObjectImporterConfig

LOGGER = logging.getLogger(__name__)


class JsonObjectImporter(ObjectImporter):
    CONTENT_TYPE = 'application/json'
    FILE_TYPE = 'json'

    def __init__(self, file=None, config: ObjectImporterConfig = None,
                 parser: JsonObjectParser = None):
        super(JsonObjectImporter, self).__init__(file=file, config=config, parser=parser)

    def start_import(self):
        parsed_data = self.parser.parse(self.file)
        LOGGER.debug(parsed_data)


class CsvObjectImporter(ObjectImporter):
    CONTENT_TYPE = 'text/csv'
    FILE_TYPE = 'csv'

    def __init__(self, file=None, config: ObjectImporterConfig = None,
                 parser: CsvObjectParser = None):
        super(CsvObjectImporter, self).__init__(file=file, config=config, parser=parser)

    def start_import(self):
        parsed_data = self.parser.parse(self.file)
        LOGGER.debug(parsed_data)
