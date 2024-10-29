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
import logging

from cmdb.framework.models.type import TypeModel
from cmdb.framework.models.category import CategoryModel
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 CategoryNode - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class CategoryNode:
    """Class of a category node inside the category tree"""

    def __init__(self, category: CategoryModel, children: list["CategoryNode"] = None,
                    types: list[TypeModel] = None):
        self.category: CategoryModel = category
        self.node_order: int = self.category.get_meta().get_order()
        self.children: list["CategoryNode"] = sorted(children or [], key=lambda node: (
                                                            node.get_order() is None, node.get_order()))
        # prevent wrong type order
        self.types: list[TypeModel] = [type_ for id_ in self.category.types for type_ in types if
                                        id_ == type_.public_id]


    @classmethod
    def to_json(cls, instance: "CategoryNode"):
        """Get the node as json"""
        return {
            'category': CategoryModel.to_json(instance.category),
            'node_order': instance.node_order,
            'children': [CategoryNode.to_json(child_node) for child_node in instance.children],
            'types': [TypeModel.to_json(type) for type in instance.types]
        }


    def get_order(self) -> int:
        """Get the order value from the main category inside this node.
        Should be equal to __CategoryMeta -> order
        """
        return self.node_order


    def flatten(self) -> list[CategoryModel]:
        """Flats a category node and its children"""
        return [self.category] + sum(
            (c.flatten() for c in self.children),
            [],
        )


    def __repr__(self):
        """String representation of the category node"""
        return f'CategoryNode(CategoryID={self.category.public_id})'
