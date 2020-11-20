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
from typing import Generic, TypeVar, Set, Dict

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


class AccessControlSectionDict(Dict[T, Set[AccessControlPermission]]):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AccessControlListSection(Generic[T]):
    """`AccessControlListSection` are a config element inside the complete ac-dict."""

    def __init__(self, includes: AccessControlSectionDict = None):
        self.includes: AccessControlSectionDict = includes or AccessControlSectionDict()

    @property
    def includes(self) -> AccessControlSectionDict:
        return self._includes

    @includes.setter
    def includes(self, value: AccessControlSectionDict):
        if not isinstance(value, dict):
            raise TypeError('`AccessControlListSection` only takes dict as include structure')
        self._includes = value

    def _add_entry(self, key: T) -> T:
        self.includes.update({key: Set[AccessControlPermission]()})
        return key

    def _update_entry(self, key: T, permissions: Set[AccessControlPermission]):
        self.includes.update({key: permissions})

    def grant_access(self, key: T, permission: AccessControlPermission):
        self.includes[key].add(permission)

    def revoke_access(self, key: T, permission: AccessControlPermission):
        self.includes[key].remove(permission)

    def verify_access(self, key: T, permission: AccessControlPermission) -> bool:
        return permission in self.includes[key]

    @classmethod
    def from_data(cls, data: dict) -> "AccessControlListSection[T]":
        raise NotImplementedError

    @classmethod
    def to_json(cls, section: "AccessControlListSection[T]") -> dict:
        raise NotImplementedError


class GroupACL(AccessControlListSection[int]):
    """Wrapper class for the group section"""

    def __init__(self, includes: AccessControlSectionDict[T]):
        super(GroupACL, self).__init__(includes=includes)

    @classmethod
    def from_data(cls, data: dict) -> "GroupACL":
        return cls(data.get('includes', set()))

    @classmethod
    def to_json(cls, section: "AccessControlListSection[T]") -> dict:
        return {
            'includes': section.includes
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

    def grant_access(self, section: str, key: T, permission: AccessControlPermission):
        if section == 'groups':
            self.groups.grant_access(key, permission)
        else:
            raise ValueError(f'No ACL section with name: {section}')

    def revoke_access(self, section: str, key: T, permission: AccessControlPermission):
        if section == 'groups':
            self.groups.grant_access(key, permission)
        else:
            raise ValueError(f'No ACL section with name: {section}')

    def verify_access(self, section: str, key: T, permission: AccessControlPermission) -> bool:
        if section == 'groups':
            return self.groups.verify_access(key, permission)
        else:
            raise ValueError(f'No ACL section with name: {section}')
