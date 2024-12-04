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
"""Response classes. These include already parsed data and additional information based on their types."""
# -------------------------------------------------------------------------------------------------------------------- #

class BaseParserResponse:
    """Basic response only includes the number of parsed elements"""

    def __init__(self, count: int):
        self.count: int = count


    def output(self) -> dict:
        """TODO: document"""
        raise NotImplementedError
