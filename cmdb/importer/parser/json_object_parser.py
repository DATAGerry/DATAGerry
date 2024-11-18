# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""TODO: document"""
import json
import logging

from cmdb.importer.content_types import JSONContent
from cmdb.importer.parser.base_object_parser import BaseObjectParser
from cmdb.importer.responses.json_object_parser_response import JsonObjectParserResponse
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               JsonObjectParser - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class JsonObjectParser(BaseObjectParser, JSONContent):
    """TODO: document"""

    DEFAULT_CONFIG = {
        'indent': 2,
        'encoding': 'UTF-8'
    }

    def __init__(self, parser_config: dict = None):
        super().__init__(parser_config)


    def parse(self, file) -> JsonObjectParserResponse:
        run_config = self.get_config()

        with open(file, 'r', encoding=run_config.get('encoding')) as json_file:
            parsed = json.load(json_file)

        return JsonObjectParserResponse(count=len(parsed), entries=parsed)
