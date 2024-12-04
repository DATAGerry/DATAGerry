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
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                           ExcelObjectParserResponse - CLASS                                          #
# -------------------------------------------------------------------------------------------------------------------- #
class ExcelObjectParserResponse(ObjectParserResponse):
    """TODO: document"""

    def __init__(self, count: int, entries: list, entry_length: int, header: dict = None):
        self.entry_length: int = entry_length
        self.header: dict = header or {}
        super().__init__(count=count, entries=entries)


    def get_entry_length(self) -> int:
        """TODO: document"""
        return self.entry_length


    def get_header_list(self) -> dict:
        """TODO: document"""
        return self.header
