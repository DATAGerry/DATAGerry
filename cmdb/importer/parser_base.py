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

from cmdb.importer.parser_response import ParserResponse, ObjectParserResponse
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class BaseParser:
    """TODO: document"""
    DEFAULT_CONFIG = {}

    def __new__(cls, *args, **kwargs):
        return super(BaseParser, cls).__new__(cls)


    def __init__(self, parser_config: dict = None):
        _parser_config = parser_config or self.DEFAULT_CONFIG
        self.parser_config: dict = {**self.DEFAULT_CONFIG, **_parser_config}


    def get_config(self) -> dict:
        """TODO: document"""
        return self.parser_config


    def parse(self, file) -> ParserResponse:
        """TODO: document"""
        raise NotImplementedError

#TODO: CLASS-FIX
class BaseObjectParser(BaseParser):
    """TODO: document"""

    DEFAULT_CONFIG = {}

    def __init__(self, parser_config: dict):
        super().__init__(parser_config)


    def parse(self, file) -> ObjectParserResponse:
        raise NotImplementedError

#TODO: CLASS-FIX
class BaseTypeParser(BaseParser):
    """TODO: document"""

    DEFAULT_CONFIG = {}

    def __init__(self, parser_config: dict):
        super().__init__(parser_config)


    def parse(self, file) -> ObjectParserResponse:
        raise NotImplementedError
