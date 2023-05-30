# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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

from typing import TypeVar, Dict, Set, Generic

from cmdb.security.acl.permission import AccessControlPermission

T = TypeVar('T')


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
        try:
            return permission.value in self.includes[key]
        except KeyError:
            return False

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

    @property
    def includes(self) -> dict:
        return self._includes

    @includes.setter
    def includes(self, value: AccessControlSectionDict):
        if not isinstance(value, dict):
            raise TypeError('`AccessControlListSection` only takes dict as include structure')
        else:
            value = {int(k): v for k, v in value.items()}
        self._includes = value

    @classmethod
    def from_data(cls, data: dict) -> "GroupACL":
        return cls(data.get('includes', set()))

    @classmethod
    def to_json(cls, section: "AccessControlListSection[T]") -> dict:
        return {
            'includes': {str(k): v for k, v in section.includes.items()}
        }
