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

"""
The collection module is a compilation of different types which have to be instantiated in a predefined way.
The collections are made up of a list of types and the number of objects to be created.
This functionality will later be used to represent constructions such as services.
Integration with the status system should also be possible.
"""
from cmdb.framework.cmdb_dao import CmdbDAO
from typing import Tuple, List


class CmdbCollection(CmdbDAO):
    """
    The collection class contains the template ID, the user ID of the author
    and the list of already initialized objects.
    """
    COLLECTION = "framework.collection"
    REQUIRED_INIT_KEYS = [
        'template_id'
    ]

    def __init__(self, template_id: int, object_list: list = None, **kwargs):
        """
        Constructor of CmdbCollection
        Args:
            template_id: public_id of CmdbCollectionTemplate
            user_id: public_id of CmdbUser
            object_list: list of objects which types are defined in the template
        """
        self.template_id = template_id
        self.object_list = object_list or []

        super(CmdbCollection, self).__init__(**kwargs)

    def get_object_list(self) -> list:
        """
        get the objects in this collection
        Returns:
            List of objects
        """
        return self.object_list

    def get_template_id(self) -> int:
        """
        get the public id from the collection template
        Returns:
            Template id
        """
        return self.template_id


class CmdbCollectionTemplate(CmdbDAO):
    """
    The collection Template Class defines the structure of the respective collection similar to the CMDB types.
    However to a much smaller extent. Here only the respective types and the number of objects
    to be initialized are defined.
    """
    COLLECTION = "framework.collection.template"
    REQUIRED_INIT_KEYS = [
        'name'
    ]
    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    TEMPLATE_TUPLE = Tuple[int, int]

    def __init__(self, name: str, label: str = None, type_tuple_list: List[TEMPLATE_TUPLE] = None, **kwargs):
        """
        Constructor of CmdbCollectionTemplate
        Args:
            name: name of the collection
            user_id: original public id of the author
            type_tuple_list: Tuple of types with numbers of objects
            label: (optional) Label of the name
        """
        self.name: str = name
        self.label: str = label or self.name.title()
        self.type_tuple_list: List[CmdbCollectionTemplate.TEMPLATE_TUPLE] = type_tuple_list or []
        super(CmdbCollectionTemplate, self).__init__(**kwargs)

    def get_name(self) -> str:
        """
        get the name of the collection
        Returns:
            Collection-Name
        """
        return self.name

    def get_label(self) -> str:
        """
        get label from name
        default is the name with first letter uppercase
        Returns:
            Collection-Label
        """
        return self.label

    def get_type_tuple_list(self) -> List[TEMPLATE_TUPLE]:
        """
        get list of type tuples
        Returns:
            List of type tuples based on [TYPE_ID, NUMBER_OF_OBJECTS]
        """
        return self.type_tuple_list

    @classmethod
    def generate_type_tuple(cls, type_id: int, count: int) -> TEMPLATE_TUPLE:
        """
        generate a type tuple
        Args:
            type_id: public_id of type
            count: number of objects

        Returns:
            type tuples based on [TYPE_ID, NUMBER_OF_OBJECTS]
        """
        return type_id, count
