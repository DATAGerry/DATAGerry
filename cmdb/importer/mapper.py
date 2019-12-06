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
"""Mapping module. The connection classes of data to the respective memory areas (e.g. fields) are created here."""
from collections import Iterable
from typing import List, Iterator, Any


class MapEntry:

    def __init__(self, name: Any, value: str, **options):
        self.name: Any = name
        self.value: Any = value
        self.option: dict = options

    def get_name(self) -> Any:
        return self.name

    def get_value(self) -> Any:
        return self.value

    def has_option(self, option: dict) -> bool:
        return option.items() <= self.get_option().items()

    def get_option(self) -> dict:
        return self.option


class Mapping(Iterable):

    def __init__(self, entries: List[MapEntry] = None):
        self.__entries: List[MapEntry] = entries or []

    def __iter__(self) -> Iterator[MapEntry]:
        return iter(self.get_entries())

    def __len__(self) -> int:
        return len(self.get_entries())

    @classmethod
    def generate_mapping_from_list(cls, map_list: List[dict]):
        maps = Mapping()
        for mapper in map_list:
            maps.add_entry(MapEntry(**mapper))
        return maps

    def get_entries(self) -> List[MapEntry]:
        return self.__entries

    def get_entries_with_option(self, query: dict) -> List[MapEntry]:
        founded_entries: List[MapEntry] = []
        for entry in self:
            if entry.has_option(query):
                founded_entries.append(entry)
        return founded_entries

    def add_entry(self, entry: MapEntry):
        self.__entries.append(entry)

    def add_entries(self, entries: List[MapEntry]):
        self.__entries = self.__entries + entries

    def remove_entry(self, entry: MapEntry):
        self.__entries.remove(entry)
