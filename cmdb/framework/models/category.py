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
from typing import Union

from cmdb.framework.models.type import TypeModel
from cmdb.cmdb_objects.cmdb_dao import CmdbDAO
from cmdb.framework.models.category_model.category_meta import CategoryMeta
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 CategoryModel - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class CategoryModel(CmdbDAO):
    """TODO: document"""

    COLLECTION = 'framework.categories'
    MODEL = 'Category'
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


    def __init__(self,
                 public_id: int,
                 name: str,
                 label: str = None,
                 meta: CategoryMeta = None,
                 parent: int = None,
                 types: Union[list[int], list[TypeModel]] = None):
        """TODO: document"""
        self.name: str = name
        self.label: str = label
        self.meta: CategoryMeta = meta

        if parent == public_id and (parent is not None):
            raise ValueError(f'Category {name} has his own ID as Parent')

        self.parent: int = parent
        self.types: Union[list[int], list[TypeModel]] = types or []
        super().__init__(public_id=public_id)


    @classmethod
    def from_data(cls, data: dict) -> "CategoryModel":
        """Create a instance of a category from database"""
        raw_meta: dict = data.get('meta', None)

        if raw_meta:
            meta = CategoryMeta(raw_meta.get('icon', ''), raw_meta.get('order', None))
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


    def get_meta(self) -> CategoryMeta:
        """Get meta data"""
        if not self.meta:
            self.meta = CategoryMeta()
        return self.meta


    def has_parent(self) -> bool:
        """Check if category has parent"""
        return bool(self.parent)


    def get_parent(self) -> int:
        """Get the public id of the parent"""
        return self.parent


    def has_types(self) -> bool:
        """Check if this category has types"""
        return self.get_number_of_types() > 0


    def get_types(self) -> Union[list[int], list[TypeModel]]:
        """Get list of type ids in this category"""
        if not self.types:
            self.types = []
        return self.types


    def get_number_of_types(self) -> int:
        """Get number of types in this category"""
        return len(self.get_types())
