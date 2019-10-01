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

from cmdb.importer.parser_base import BaseObjectParser
from cmdb.importer.parser_errors import ParserError
from cmdb.utils.helpers import str_to_bool

LOGGER = logging.getLogger(__name__)


class JsonParser(BaseObjectParser):
    CONTENT_TYPE = 'text/json'
    FILE_TYPE = 'json'

    def __init__(self, parser_config: dict = None):
        super(JsonParser, self).__init__(parser_config)

    def parse(self, file) -> dict:
        return {}
