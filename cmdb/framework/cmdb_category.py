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

from cmdb.framework.cmdb_dao import CmdbDAO
from cmdb.utils.error import CMDBError


class CmdbCategory(CmdbDAO):
    """
    Type category
    """
    COLLECTION = 'framework.categories'
    REQUIRED_INIT_KEYS = [
        'name',
    ]

    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, name: str, label: str = None, icon: str = None, parent_id: int = None,
                 **kwargs):
        self.name = name
        self.label = label or self.name.title()
        self.icon = icon or ''
        self.parent_id = parent_id or 0
        super(CmdbCategory, self).__init__(**kwargs)

    def get_name(self) -> str:
        return self.name

    def get_label(self) -> str:
        return self.label

    def get_icon(self) -> str:
        return self.icon

    def has_icon(self) -> bool:
        if self.icon:
            return True
        return False

    def get_parent(self) -> int:
        if self.parent_id is None:
            raise NoParentCategory(self.get_name())
        return self.parent_id

    def has_parent(self) -> bool:
        if self.parent_id is None:
            return False
        else:
            return True


class NoParentCategory(CMDBError):

    def __init__(self, name):
        super().__init__()
        self.message = 'The category {} has no parent element'.format(name)
