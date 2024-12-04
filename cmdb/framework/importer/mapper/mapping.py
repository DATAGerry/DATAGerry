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
import logging
from typing import Iterator
from collections.abc import Iterable

from cmdb.framework.importer.mapper.map_entry import MapEntry
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                    Mapping - CLASS                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
class Mapping(Iterable):
    """TODO: document"""

    def __init__(self, entries: list[MapEntry] = None):
        self.__entries: list[MapEntry] = entries or []

    def __iter__(self) -> Iterator[MapEntry]:
        return iter(self.get_entries())

    def __len__(self) -> int:
        return len(self.get_entries())


    @classmethod
    def generate_mapping_from_list(cls, map_list: list[dict]):
        """TODO: document"""
        maps = Mapping()
        for mapper in map_list:
            maps.add_entry(MapEntry(**mapper))
        return maps


    def get_entries(self) -> list[MapEntry]:
        """TODO: document"""
        return self.__entries


    def get_entries_with_option(self, query: dict) -> list[MapEntry]:
        """TODO: document"""
        founded_entries: list[MapEntry] = []
        for entry in self:
            if entry.has_option(query):
                founded_entries.append(entry)
        return founded_entries


    def add_entry(self, entry: MapEntry):
        """TODO: document"""
        self.__entries.append(entry)


    def add_entries(self, entries: list[MapEntry]):
        """TODO: document"""
        self.__entries = self.__entries + entries


    def remove_entry(self, entry: MapEntry):
        """TODO: document"""
        self.__entries.remove(entry)
