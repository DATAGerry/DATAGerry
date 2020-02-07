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

Notes:
    ONLY IMPLEMENTED IN BACKEND AT THE MOMENT - CANT BE USED!
"""
from datetime import datetime

from cmdb.framework.cmdb_dao import CmdbDAO
from typing import List, Dict


class CmdbCollection(CmdbDAO):
    """
    The collection class contains the template ID, the user ID of the author
    and the list of already initialized objects.
    """
    COLLECTION = "framework.collection"
    REQUIRED_INIT_KEYS = [
        'template_id'
    ]

    def __init__(self, template_id: int, object_list: List[int] = None, creation_time: datetime = None,
                 last_edit_time: datetime = None, **kwargs):
        """Constructor of CmdbCollection
        """
        self.template_id: int = template_id
        self.object_list: List[int] = object_list or []
        self.creation_time: datetime = creation_time or datetime.utcnow()
        self.last_edit_time: datetime = last_edit_time

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
    """The collection Template Class defines the structure of the respective collection similar to the CMDB types.
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
    TYPE_DATATYPE = int
    OBJECT_COUNTER_DATATYPE = int
    TEMPLATE_DICT = Dict['type_id', 'count']

    def __init__(self, name: str, label: str = None, type_order_list: List[TEMPLATE_DICT] = None,
                 creation_time: datetime = None, last_edit_time: datetime = None, **kwargs):
        """Constructor of CmdbCollectionTemplate
        """
        self.name: str = name.lower()
        self.label: str = label or self.name.title()
        self.type_order_list: List[CmdbCollectionTemplate.TEMPLATE_DICT] = type_order_list or []
        self.creation_time: datetime = creation_time or datetime.utcnow()
        self.last_edit_time: datetime = last_edit_time
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

    def get_type_order_list(self) -> List[TEMPLATE_DICT]:
        """
        get list of type tuples
        Returns:
            List of type tuples based on [TYPE_ID, NUMBER_OF_OBJECTS]
        """
        return self.type_order_list

    @classmethod
    def generate_type_dict(cls, type_id: TYPE_DATATYPE, count: OBJECT_COUNTER_DATATYPE) -> TEMPLATE_DICT:
        """
        generate a type dict
        Args:
            type_id: public_id of type
            count: number of objects

        Returns:
            type tuples based on [TYPE_ID, NUMBER_OF_OBJECTS]
        """
        return {'type_id': type_id, 'count': count}
