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

    def _generate_next_value_(self, start, count, last_values):
        return self

    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()


class AccessControlListEntry(Generic[T]):
    """ACL entry inside the `AccessControlListSection.`"""

    def __init__(self, role: T, permissions: List[AccessControlPermission] = None):
        self.role = role
        self.permissions = permissions or []

    @classmethod
    def from_entry(cls, role: T, permission: AccessControlPermission = None):
        """Creates a `AccessControlListEntry` from a role and a single permission."""
        if permission:
            permission = [permission]
        return cls(role=role, permissions=permission)

    @classmethod
    def from_data(cls, data: dict) -> "AccessControlListEntry[T]":
        return cls(
            role=data.get('role'),
            permissions=data.get('permissions', [])
        )

    @classmethod
    def to_json(cls, entry: "AccessControlListEntry[T]") -> dict:
        return {
            'role': entry.role,
            'permissions': entry.permissions
        }


class AccessControlListSection(Generic[T]):
    """`AccessControlListSection` are a config element inside the complete ac-list."""

    def __init__(self, activated: bool = False, includes: List[AccessControlListEntry[T]] = None):
        self.activated = activated
        self.includes: List[AccessControlListEntry[T]] = includes or []

    @property
    def includes(self) -> List[AccessControlListEntry[T]]:
        return self._includes

    @includes.setter
    def includes(self, value: List[AccessControlListEntry[T]]):
        if not isinstance(value, list):
            raise TypeError('`AccessControlListSection` only takes lists as include structure')
        self._includes = value

    def _add_entry(self, role: T, permission: AccessControlPermission = None) -> AccessControlListEntry[T]:
        entry = AccessControlListEntry.from_entry(role, permission)
        self.includes.append(entry)
        return entry

    def _get_entry(self, role: T) -> AccessControlListEntry[T]:
        for entry in self.includes:
            if entry.role == role:
                return entry
        raise ValueError('No entry in the list')

    def _update_entry(self, entry: AccessControlListEntry[T]) -> List[AccessControlListEntry[T]]:
        for idx, e in enumerate(self.includes):
            if e.role == entry.role:
                self.includes[idx] = entry
                return self.includes
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

    @classmethod
    def from_data(cls, data: dict) -> "AccessControlListSection[T]":
        raise NotImplementedError

    @classmethod
    def to_json(cls, section: "AccessControlListSection[T]") -> dict:
        raise NotImplementedError


class GroupACL(AccessControlListSection[int]):
    """Wrapper class for the group section"""

    def __init__(self, activated: bool = False, includes: List[AccessControlListEntry[int]] = None):
        super(GroupACL, self).__init__(activated=activated, includes=includes)

    @classmethod
    def from_data(cls, data: dict) -> "GroupACL":
        includes = [AccessControlListEntry.from_data(entry) for entry in
                    data.get('includes', [])]
        return cls(
            activated=data.get('activated', True),
            includes=includes
        )

    @classmethod
    def to_json(cls, section: "AccessControlListSection[T]") -> dict:
        includes = [AccessControlListEntry.to_json(entry) for entry in
                    section.includes]
        return {
            'activated': section.activated,
            'includes': includes
        }


class AccessControlList:
    """
    The actual implementation of the Access Control List (ACL).
    """

    def __init__(self, activated: bool, groups: GroupACL = None):
        self.activated = activated
        self.groups: GroupACL = groups

    @classmethod
    def from_data(cls, data: dict) -> "AccessControlList":
        return cls(
            activated=data.get('activated', False),
            groups=GroupACL.from_data(data.get('groups', {}))
        )

    @classmethod
    def to_json(cls, acl: "AccessControlList") -> dict:
        return {
            'activated': acl.activated,
            'groups': GroupACL.to_json(acl.groups)
        }

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
