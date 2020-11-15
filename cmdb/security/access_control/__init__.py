# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2020 NETHINKS GmbH
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
from enum import Enum, unique, auto
from typing import Generic, TypeVar, List

T = TypeVar('T')


@unique
class AccessControlPermission(Enum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()

    def _generate_next_value_(self, start, count, last_values):
        return self


class AccessControlListEntry(Generic[T]):
    def __init__(self, role: T, permissions: List[AccessControlPermission]):
        self.role = role
        self.permissions = permissions or []


class AccessControlListSection(Generic[T]):

    def __init__(self, activated: bool = False, include: List[AccessControlListEntry[T]] = None):
        self.activated = activated
        self.include: List[AccessControlListEntry[T]] = include or []

    @property
    def include(self) -> List[AccessControlListEntry[T]]:
        return self._include

    @include.setter
    def include(self, value: List[AccessControlListEntry[T]]):
        if not isinstance(value, list):
            raise TypeError('`AccessControlListSection` only takes lists as include structure')
        self._include = value


class GroupACL(AccessControlListSection[int]):

    def __init__(self, activated: bool = False, include: List = None):
        super(GroupACL, self).__init__(activated=activated, include=include)


class AccessControlList:

    def __init__(self, activated: bool, groups: GroupACL = None):
        self.activated = activated
        self.groups: GroupACL = groups
