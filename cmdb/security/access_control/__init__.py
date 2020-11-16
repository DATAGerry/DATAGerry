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
    """Permission enum for possible ACL operations."""
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()

    def _generate_next_value_(self, start, count, last_values):
        return self


class AccessControlListEntry(Generic[T]):
    """ACL entry inside the `AccessControlListSection.`"""

    def __init__(self, role: T, permissions: List[AccessControlPermission] = None):
        self.role = role
        self.permissions = permissions or []

    @classmethod
    def from_entry(cls, role: T, permissions: AccessControlPermission = None):
        """Creates a `AccessControlListEntry` from a role and a single permission."""
        if permissions:
            permissions = [permissions]
        return cls(role=role, permissions=permissions)


class AccessControlListSection(Generic[T]):
    """`AccessControlListSection` are a config element inside the complete ac-list."""

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

    def _add_entry(self, role: T, permission: AccessControlPermission = None) -> AccessControlListEntry[T]:
        entry = AccessControlListEntry.from_entry(role, permission)
        self.include.append(entry)
        return entry

    def _get_entry(self, role: T) -> AccessControlListEntry[T]:
        for entry in self.include:
            if entry.role == role:
                return entry
        raise ValueError('No entry in the list')

    def _update_entry(self, entry: AccessControlListEntry[T]) -> List[AccessControlListEntry[T]]:
        for idx, e in enumerate(self.include):
            if e.role == entry.role:
                self.include[idx] = entry
                return self.include
        else:
            raise IndexError('Entry not exists')

    def grant_access(self, role: T, permission: AccessControlPermission):
        try:
            entry = self._get_entry(role)
        except ValueError:
            entry = self._add_entry(role)
        entry.permissions.append(permission)
        self._update_entry(entry)

    def revoke_access(self, role: T, permission: AccessControlPermission):
        entry = self._get_entry(role)
        entry.permissions.remove(permission)
        self._update_entry(entry)

    def verify_access(self, role: T, permission: AccessControlPermission) -> bool:
        entry = self._get_entry(role)
        return permission in entry.permissions


class GroupACL(AccessControlListSection[int]):
    """Wrapper class for the group section"""

    def __init__(self, activated: bool = False, include: List = None):
        super(GroupACL, self).__init__(activated=activated, include=include)


class AccessControlList:
    """
    The actual implementation of the Access Control List (ACL).
    """

    def __init__(self, activated: bool, groups: GroupACL = None):
        self.activated = activated
        self.groups: GroupACL = groups

    def grant_access(self, section: str, role: T, permission: AccessControlPermission):
        if section == 'groups':
            self.groups.grant_access(role, permission)
        else:
            raise ValueError(f'No ACL section with name: {section}')

    def revoke_access(self, section: str, role: T, permission: AccessControlPermission):
        if section == 'groups':
            self.groups.grant_access(role, permission)
        else:
            raise ValueError(f'No ACL section with name: {section}')

    def verify_access(self, section: str, role: T, permission: AccessControlPermission) -> bool:
        if section == 'groups':
            return self.groups.verify_access(role, permission)
        else:
            raise ValueError(f'No ACL section with name: {section}')

    def deny_access(self, role: T, permission: AccessControlPermission):
        raise NotImplementedError
