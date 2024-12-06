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
from typing import TypeVar

from cmdb.security.acl.access_control_list_section import AccessControlListSection
from cmdb.security.acl.access_control_section_dict import AccessControlSectionDict
# -------------------------------------------------------------------------------------------------------------------- #

T = TypeVar('T')

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   GroupACL - CLASS                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
class GroupACL(AccessControlListSection[int]):
    """Wrapper class for the group section"""

    def __init__(self, includes: AccessControlSectionDict[T]):
        super().__init__(includes=includes)


    @property
    def includes(self) -> dict:
        return self._includes


    @includes.setter
    def includes(self, value: AccessControlSectionDict):
        if not isinstance(value, dict):
            raise TypeError('`AccessControlListSection` only takes dict as include structure')

        value = {int(k): v for k, v in value.items()}

        self._includes = value


    @classmethod
    def from_data(cls, data: dict) -> "GroupACL":
        """TODO: document"""
        return cls(data.get('includes', set()))


    @classmethod
    def to_json(cls, section: "AccessControlListSection[T]") -> dict:
        """TODO: document"""
        return {
            'includes': {str(k): v for k, v in section.includes.items()}
        }
