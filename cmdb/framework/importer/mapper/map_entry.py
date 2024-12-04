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
"""Mapping module. The connection classes of data to the respective memory areas (e.g. fields) are created here."""
from typing import Any
# -------------------------------------------------------------------------------------------------------------------- #

class MapEntry:
    """TODO: document"""

    def __init__(self, name: Any, value: str, **options):
        self.name: Any = name
        self.value: Any = value
        self.option: dict = options


    def get_name(self) -> Any:
        """TODO: document"""
        return self.name


    def get_value(self) -> Any:
        """TODO: document"""
        return self.value


    def has_option(self, option: dict) -> bool:
        """TODO: document"""
        return option.items() <= self.get_option().items()


    def get_option(self) -> dict:
        """TODO: document"""
        return self.option
