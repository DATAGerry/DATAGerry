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
from typing import List


class MapEntry:

    def __init__(self, identifier: str, value: str, **options):
        self.identifier: str = identifier
        self.value: str = value
        self.option: dict = options


class Mapping:

    def __init__(self, entries: List[MapEntry] = None):
        self.__entries: List[MapEntry] = entries or []

    def get_entries(self) -> List[MapEntry]:
        return self.__entries

    def add_entry(self, entry: MapEntry):
        self.__entries.append(entry)

    def add_entries(self, entries: List[MapEntry]):
        self.__entries = self.__entries + entries

    def remove_entry(self, entry: MapEntry):
        self.__entries.remove(entry)
