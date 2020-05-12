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
from typing import List

from cmdb.framework.cmdb_dao import CmdbDAO


class _CmdbCategoryMeta:

    def __init__(self, icon: str = '', order: int = None):
        self.icon = icon
        self.order = order

    def get_icon(self) -> str:
        """Get a icon, string or unicode symbol"""
        return self.icon

    def has_icon(self) -> bool:
        """Check if icon is set"""
        if self.icon:
            return True
        return False

    def get_order(self) -> int:
        """Get the order"""
        return self.order

    def has_order(self) -> bool:
        """Check if order is set"""
        if self.order:
            return True
        return False


class CmdbCategory(CmdbDAO):
    """
    Category
    """
    COLLECTION = 'framework.categories'

    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True},
        # {'keys': [('children.public_id', CmdbDAO.DAO_ASCENDING)], 'name': 'children.public_id', 'unique': True},
        # {'keys': [('children.name', CmdbDAO.DAO_ASCENDING)], 'name': 'children.name', 'unique': True}
    ]

    def __init__(self, public_id: int, name: str, label: str = None, meta: _CmdbCategoryMeta = None,
                 children: List["CmdbCategory"] = None, types: List[int] = None):
        self.name: str = name
        self.label: str = label
        self.meta: _CmdbCategoryMeta = meta
        self.children: List[CmdbCategory] = children
        self.types: List[int] = types
        super(CmdbCategory, self).__init__(public_id=public_id)

    @classmethod
    def from_database(cls, data: dict) -> "CmdbCategory":
        """Create a instance of a category from database"""

        raw_meta: dict = data.get('meta', None)
        if raw_meta:
            meta = _CmdbCategoryMeta(icon=raw_meta.get('icon', ''), order=raw_meta.get('order', None))
        else:
            meta = raw_meta

        raw_children: dict = data.get('children', [])
        if raw_meta:
            children = [CmdbCategory.from_database(child) for child in raw_children]
        else:
            children = raw_children

        return cls(public_id=data.get('public_id'), name=data.get('name'), label=data.get('label', None),
                   meta=meta, children=children, types=data.get('types', [])
                   )

    @classmethod
    def to_json(cls, instance: "CmdbCategory") -> dict:
        """Convert a category instance to json conform data"""
        meta = instance.get_meta()
        return {
            'public_id': instance.get_public_id(),
            'name': instance.get_name(),
            'label': instance.get_label(),
            'meta': {
                'icon': meta.get_icon(),
                'order': meta.get_order()
            },
            'children': [CmdbCategory.to_json(child) for child in instance.children],
            'types': instance.get_types()
        }

    def get_name(self) -> str:
        """Get the identifier name"""
        return self.name

    def get_label(self) -> str:
        """Get the display name"""
        if not self.label:
            self.label = self.name.title()
        return self.label

    def get_meta(self) -> _CmdbCategoryMeta:
        """Get meta data"""
        if not self.meta:
            self.meta = _CmdbCategoryMeta()
        return self.meta

    def get_children(self) -> List["CmdbCategory"]:
        """Get child categories"""
        if not self.children:
            self.children = []
        return self.children

    def get_types(self) -> List[int]:
        """Get list of type ids in this category"""
        if not self.types:
            self.types = []
        return self.types

    def get_number_of_types(self) -> int:
        """Get number of types in this category"""
        return len(self.get_types())
