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
"""TODO: document"""
from typing import TypeVar, Set, Generic

from cmdb.security.acl.access_control_section_dict import AccessControlSectionDict
from cmdb.security.acl.permission import AccessControlPermission
# -------------------------------------------------------------------------------------------------------------------- #

T = TypeVar('T')

# -------------------------------------------------------------------------------------------------------------------- #
#                                           AccessControlListSection - CLASS                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class AccessControlListSection(Generic[T]):
    """`AccessControlListSection` are a config element inside the complete ac-dict."""

    def __init__(self, includes: AccessControlSectionDict = None):
        self.includes: AccessControlSectionDict = includes or AccessControlSectionDict()


    @property
    def includes(self) -> AccessControlSectionDict:
        """TODO: document"""
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
        """TODO: document"""
        self.includes[key].add(permission)


    def revoke_access(self, key: T, permission: AccessControlPermission):
        """TODO: document"""
        self.includes[key].remove(permission)


    @classmethod
    def from_data(cls, data: dict) -> "AccessControlListSection[T]":
        """TODO: document"""
        raise NotImplementedError


    @classmethod
    def to_json(cls, section: "AccessControlListSection[T]") -> dict:
        """TODO: document"""
        raise NotImplementedError