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
"""
This managers represents the core functionalities for the use of CMDB objects.
All communication with the objects is controlled by this managers.
The implementation of the managers used is always realized using the respective superclass.
"""
import logging
# -------------------------------------------------------------------------------------------------------------------- #
LOGGER = logging.getLogger(__name__)

class LocationNode:
    """
    Represents a node in the location tree
    """
    def __init__(self, params: dict):
        self.public_id: int = params['public_id']
        self.name: str = params['name']
        self.parent: int = params['parent']
        self.icon: str = params['type_icon']
        self.object_id: int = params['object_id']
        self.children: list[LocationNode] = []


    def get_children(self, public_id:int, locations_list: list[dict]):
        """
        Gets recursively all children for a location

        Args:
            public_id (int): public:id of the location
            locations_list (list): list of locations from database

        Returns:
            list[LocationNode]: returns all children for the given public_id
        """
        sorted_children: list["LocationNode"] = []
        filtered_list: list[dict] = []

        if len(locations_list) > 0:
            for location in locations_list:
                if location['parent'] == public_id:
                    sorted_children.append(LocationNode(location))
                else:
                    filtered_list.append(location)

            if len(filtered_list) > 0:
                for child in sorted_children:
                    child.children = self.get_children(child.get_public_id(), filtered_list)
        return sorted_children


    def get_public_id(self):
        """
        Returns the public_id of this LocationNode
        """
        return self.public_id


    def __repr__(self) -> str:
        return f"[LocationNode => public_id: {self.public_id}, \
                                  name: {self.name}, \
                                  parent: {self.parent}, \
                                  icon: {self.icon}, \
                                  object_id: {self.object_id}, \
                                  children: {len(self.children)}]"


    @classmethod
    def to_json(cls, instance: "LocationNode") -> dict:
        """Convert a LocationNode instance to json conform data"""

        json_data = {
            'public_id': instance.public_id,
            'name': instance.name,
            'parent': instance.parent,
            'icon': instance.icon,
            'object_id': instance.object_id,
        }

        # convert children to json
        children = []
        if len(instance.children) > 0:
            for child in instance.children:
                children.append(cls.to_json(child))

        # if there are any children then append the children-key
        if len(children) > 0:
            json_data['children'] = children

        return json_data
