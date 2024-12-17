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
import logging

from cmdb.framework.importer.responses.object_parser_response import ObjectParserResponse
from cmdb.framework.importer.parser.base_parser import BaseParser
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               BaseObjectParser - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class BaseObjectParser(BaseParser):
    """TODO: document"""

    DEFAULT_CONFIG = {}

    def __init__(self, parser_config: dict):
        super().__init__(parser_config)


    def parse(self, file) -> ObjectParserResponse:
        raise NotImplementedError
