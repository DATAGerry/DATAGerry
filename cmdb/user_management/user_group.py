# Net|CMDB - OpenSource Enterprise CMDB
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

from cmdb.user_management.user_base import UserManagementBase
from cmdb.utils.error import CMDBError


class UserGroup(UserManagementBase):
    COLLECTION = 'management.groups'
    REQUIRED_INIT_KEYS = ['name']
    INDEX_KEYS = [
        {'keys': [('name', UserManagementBase.ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, name: str, label: str = None, rights: list = None, **kwargs):
        self.name = name
        self.label = label or name.title()
        self.rights = rights or []
        super(UserGroup, self).__init__(**kwargs)

    def get_name(self):
        return self.name

    def get_label(self):
        return self.label

    def set_rights(self, rights: list):
        self.rights = rights

    def get_rights(self):
        return self.rights

    def get_right(self, name):
        try:
            return self.rights[self.rights.index(name)]
        except (IndexError, TypeError, ValueError):
            raise RightNotFoundError(self.name, name)

    def has_right(self, name):
        try:
            self.get_right(name)
        except RightNotFoundError:
            return False
        return True


class RightNotFoundError(CMDBError):
    def __init__(self, group, right):
        super().__init__()
        self.message = "Right was not found inside this group Groupname: {} | Rightname: {}".format(group, right)
