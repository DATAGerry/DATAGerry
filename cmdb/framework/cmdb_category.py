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


class CmdbCategory(CmdbDAO):
    """
    Category
    """
    COLLECTION = 'framework.categories'

    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True},
        {'keys': [('parent', CmdbDAO.DAO_ASCENDING)], 'name': 'parent', 'unique': False},
        {'keys': [('types', CmdbDAO.DAO_ASCENDING)], 'name': 'types', 'unique': False}
    ]

    class __CmdbCategoryMeta:

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

    def __init__(self, public_id: int, name: str, label: str = None, meta: __CmdbCategoryMeta = None,
                 parent: int = None, types: List[int] = None):
        self.name: str = name
        self.label: str = label
        self.meta: CmdbCategory.__CmdbCategoryMeta = meta
        self.parent: int = parent
        self.types: List[int] = types
        super(CmdbCategory, self).__init__(public_id=public_id)

    @classmethod
    def from_data(cls, data: dict) -> "CmdbCategory":
        """Create a instance of a category from database"""

        raw_meta: dict = data.get('meta', None)
        if raw_meta:
            meta = cls.__CmdbCategoryMeta(icon=raw_meta.get('icon', ''), order=raw_meta.get('order', None))
        else:
            meta = raw_meta

        return cls(public_id=data.get('public_id'), name=data.get('name'), label=data.get('label', None),
                   meta=meta, parent=data.get('parent'), types=data.get('types', [])
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
            'parent': instance.get_parent(),
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

    def get_meta(self) -> __CmdbCategoryMeta:
        """Get meta data"""
        if not self.meta:
            self.meta = CmdbCategory.__CmdbCategoryMeta()
        return self.meta

    def has_parent(self) -> bool:
        """Check if category has parent"""
        return True if self.parent else False

    def get_parent(self) -> int:
        """Get the public id of the parent"""
        return self.parent

    def get_types(self) -> List[int]:
        """Get list of type ids in this category"""
        if not self.types:
            self.types = []
        return self.types

    def get_number_of_types(self) -> int:
        """Get number of types in this category"""
        return len(self.get_types())


class CategoryTree:
    class CategoryNodes:
        """Class of a category node inside the category tree"""

        def __init__(self, category: CmdbCategory, children: List["CategoryTree.CategoryNodes"]):
            self.category: CmdbCategory = category
            self.children: List["CategoryTree.CategoryNodes"] = children or []

        @classmethod
        def to_json(cls, instance: "CategoryTree.CategoryNodes"):
            """Get the node as json"""
            return {
                'category': CmdbCategory.to_json(instance.category),
                'children': [CategoryTree.CategoryNodes.to_json(child_node) for child_node in instance.children]
            }

    def __init__(self, categories: List[CmdbCategory]):
        self._categories = categories
        self._tree: List[CategoryTree.CategoryNodes] = self.__create_tree(self._categories)

    def __len__(self) -> int:
        """Get length of tree - this means the number of root categories"""
        return len(self._tree)

    @property
    def tree(self) -> List[CategoryNodes]:
        """Get the tree"""
        if not self._tree:
            self._tree = CategoryTree.__create_tree(self._categories)
        return self._tree

    @classmethod
    def __create_tree(cls, categories, parent: int = None) -> List[CategoryNodes]:
        """Generate the category tree from list structure"""
        tree = []
        for category in [category for category in categories if category.get_parent() == parent]:
            children = CategoryTree.__create_tree(categories, category.get_public_id())
            tree.append(CategoryTree.CategoryNodes(category, children))
        return tree

    @classmethod
    def from_data(cls, raw_categories: List[dict]) -> "CategoryTree":
        """Create the category list from raw data"""
        categories: List[CmdbCategory] = [CmdbCategory.from_data(category) for category in raw_categories]
        return cls(categories=categories)

    @classmethod
    def to_json(cls, instance: "CategoryTree"):
        """Get the complete category tree as json"""
        return [CategoryTree.CategoryNodes.to_json(node) for node in instance.tree]