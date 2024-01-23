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
from typing import List, Union

from cmdb.framework.models import TypeModel
from cmdb.framework.cmdb_dao import CmdbDAO
from cmdb.framework.utils import Model, Collection
# -------------------------------------------------------------------------------------------------------------------- #

class CategoryModel(CmdbDAO):
    """Category"""

    COLLECTION: Collection = 'framework.categories'
    MODEL: Model = 'Category'
    SCHEMA: dict = {
        'public_id': {
            'type': 'integer'
        },
        'name': {
            'type': 'string',
            'required': True,
            'regex': r'(\w+)-*(\w)([\w-]*)'  # kebab case validation,
        },
        'label': {
            'type': 'string',
            'required': False
        },
        'parent': {
            'type': 'integer',
            'nullable': True,
            'default': None
        },
        'types': {
            'type': 'list',
            'default': []
        },
        'meta': {
            'type': 'dict',
            'schema': {
                'icon': {
                    'type': 'string',
                    'empty': True
                },
                'order': {
                    'type': 'integer',
                    'nullable': True
                }
            },
            'default': {
                'icon': '',
                'order': None,
            }
        }
    }

    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True},
        {'keys': [('parent', CmdbDAO.DAO_ASCENDING)], 'name': 'parent', 'unique': False},
        {'keys': [('types', CmdbDAO.DAO_ASCENDING)], 'name': 'types', 'unique': False}
    ]

    class __CategoryMeta:
        """TODO: document"""
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


    def __init__(self, public_id: int, name: str, label: str = None, meta: __CategoryMeta = None,
                 parent: int = None, types: Union[List[int], List[TypeModel]] = None):
        self.name: str = name
        self.label: str = label
        self.meta: CategoryModel.__CategoryMeta = meta
        if parent == public_id and (parent is not None):
            raise ValueError(f'Category {name} has his own ID as Parent')
        self.parent: int = parent
        self.types: Union[List[int], List[TypeModel]] = types or []
        super(CategoryModel, self).__init__(public_id=public_id)

    @classmethod
    def from_data(cls, data: dict) -> "CategoryModel":
        """Create a instance of a category from database"""

        raw_meta: dict = data.get('meta', None)
        if raw_meta:
            meta = cls.__CategoryMeta(icon=raw_meta.get('icon', ''), order=raw_meta.get('order', None))
        else:
            meta = raw_meta

        return cls(public_id=data.get('public_id'), name=data.get('name'), label=data.get('label', None),
                   meta=meta, parent=data.get('parent'), types=data.get('types', None)
                   )


    @classmethod
    def to_json(cls, instance: "CategoryModel") -> dict:
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


    def get_meta(self) -> __CategoryMeta:
        """Get meta data"""
        if not self.meta:
            self.meta = CategoryModel.__CategoryMeta()
        return self.meta


    def has_parent(self) -> bool:
        """Check if category has parent"""
        return bool(self.parent)


    def get_parent(self) -> int:
        """Get the public id of the parent"""
        return self.parent


    def has_types(self) -> bool:
        """Check if this category has types"""
        return True if self.get_number_of_types() > 0 else False


    def get_types(self) -> Union[List[int], List[TypeModel]]:
        """Get list of type ids in this category"""
        if not self.types:
            self.types = []
        return self.types


    def get_number_of_types(self) -> int:
        """Get number of types in this category"""
        return len(self.get_types())


class CategoryTree:
    """Base tree holder"""
    MODEL: Model = 'CategoryTree'

    class CategoryNode:
        """Class of a category node inside the category tree"""

        def __init__(self, category: CategoryModel, children: List["CategoryTree.CategoryNode"] = None,
                     types: List[TypeModel] = None):
            self.category: CategoryModel = category
            self.node_order: int = self.category.get_meta().get_order()
            self.children: List["CategoryTree.CategoryNode"] = sorted(children or [], key=lambda node: (
                                                             node.get_order() is None, node.get_order()))
            # prevent wrong type order
            self.types: List[TypeModel] = [type_ for id_ in self.category.types for type_ in types if
                                           id_ == type_.public_id]


        @classmethod
        def to_json(cls, instance: "CategoryTree.CategoryNode"):
            """Get the node as json"""
            return {
                'category': CategoryModel.to_json(instance.category),
                'node_order': instance.node_order,
                'children': [CategoryTree.CategoryNode.to_json(child_node) for child_node in instance.children],
                'types': [TypeModel.to_json(type) for type in instance.types]
            }


        def get_order(self) -> int:
            """Get the order value from the main category inside this node.
            Should be equal to __CategoryMeta -> order
            """
            return self.node_order


        def flatten(self) -> List[CategoryModel]:
            """Flats a category node and its children"""
            return [self.category] + sum(
                (c.flatten() for c in self.children),
                [],
            )


        def __repr__(self):
            """String representation of the category node"""
            return f'CategoryNode(CategoryID={self.category.public_id})'


    def __init__(self, categories: List[CategoryModel], types: List[TypeModel] = None):
        self._categories = categories
        self._types = types
        self._tree: List[CategoryTree.CategoryNode] = sorted(self.__create_tree(self._categories, types=self._types),
                                                             key=lambda node: (
                                                             node.get_order() is None, node.get_order()))


    def __len__(self) -> int:
        """Get length of tree - this means the number of root categories"""
        return len(self._tree)


    def flat(self) -> List[CategoryModel]:
        """Returns a flatted tree with tree like category order"""
        flatted = []
        for node in self.tree:
            flatted += node.flatten()
        return flatted


    @property
    def tree(self) -> List[CategoryNode]:
        """Get the tree"""
        if not self._tree:
            self._tree = CategoryTree.__create_tree(self._categories, types=self._types)
        return self._tree


    @classmethod
    def __create_tree(cls, categories, parent: int = None, types: List[TypeModel] = None) -> List[CategoryNode]:
        """
        Generate the category tree from list structure
        Args:
            categories: list of root/child categories
            parent: the parent id of the current subset, None if root list
            types: list of all possible types
        """
        return [category for category in [CategoryTree.CategoryNode(category, CategoryTree.__create_tree(
            categories, category.get_public_id(), types), types) for category in categories if
                                          category.get_parent() == parent]]


    @classmethod
    def from_data(cls, raw_categories: List[dict]) -> "CategoryTree":
        """Create the category list from raw data"""
        categories: List[CategoryModel] = [CategoryModel.from_data(category) for category in raw_categories]
        return cls(categories=categories)


    @classmethod
    def to_json(cls, instance: "CategoryTree"):
        """Get the complete category tree as json"""
        return [CategoryTree.CategoryNode.to_json(node) for node in instance.tree]
