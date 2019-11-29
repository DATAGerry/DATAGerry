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

import logging

from cmdb.user_management.user_base import UserManagementBase
from cmdb.user_management.user_right import GLOBAL_RIGHT_IDENTIFIER
from cmdb.utils.error import CMDBError
from cmdb.utils.wraps import timing

LOGGER = logging.getLogger(__name__)


class UserGroup(UserManagementBase):
    COLLECTION = 'management.groups'
    REQUIRED_INIT_KEYS = ['name']
    INDEX_KEYS = [
        {'keys': [('name', UserManagementBase.ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, name: str, label: str = None, rights: list = None, deletable: bool = True, **kwargs):
        self.name: str = name
        self.label: str = label or name.title()
        self.rights: list = rights or []
        self.deletable: bool = deletable
        super(UserGroup, self).__init__(**kwargs)

    def get_name(self) -> str:
        return self.name

    def get_label(self) -> str:
        return self.label

    def set_rights(self, rights: list):
        self.rights = rights

    def get_rights(self) -> list:
        return self.rights

    def get_right(self, name) -> str:
        try:
            return self.rights[self.rights.index(name)]
        except (IndexError, TypeError, ValueError):
            raise RightNotFoundError(self.name, name)

    def has_right(self, right_name) -> bool:
        try:
            self.get_right(right_name)
        except RightNotFoundError:
            return False
        return True

    def has_extended_right(self, right_name: str) -> bool:
        parent_right_name: str = right_name.rsplit(".", 1)[0]
        if self.has_right(f'{parent_right_name}.{GLOBAL_RIGHT_IDENTIFIER}'):
            return True
        if parent_right_name == 'base':
            if self.has_right(f'{parent_right_name}.{GLOBAL_RIGHT_IDENTIFIER}'):
                return True
            return False
        return self.has_extended_right(right_name=parent_right_name)

    def is_deletable(self) -> bool:
        return self.deletable


class RightNotFoundError(CMDBError):
    def __init__(self, group, right):
        self.message = "Right was not found inside this group Groupname: {} | Rightname: {}".format(group, right)
        super(RightNotFoundError, self).__init__()
