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
This module contains the implementation of CmdbLocation, which is representing
a location in Datagarry.
"""
import logging

from cmdb.framework.cmdb_dao import CmdbDAO
from cmdb.framework.utils import Collection, Model
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 CmdbLocation - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #

class CmdbLocation(CmdbDAO):
    """
    The CMDB location is the basic data wrapper for storing and
    holding locations within the CMDB.

    Attributes:
        COLLECTION (Collection):    Name of the database collection.
        MODEL (Model):              Name of the DAO.
        DEFAULT_VERSION (str):      The default "starting" version number.
        SCHEMA (dict):              The validation schema for this DAO.
        INDEX_KEYS (list):          List of index keys for the database.
    """
    COLLECTION: Collection = 'framework.locations'
    MODEL: Model = 'Location'
    DEFAULT_VERSION: str = '1.0.0'
    REQUIRED_INIT_KEYS = ['name', 'parent', 'object_id', 'type_id', 'type_label']

    SCHEMA: dict = {
        'public_id': {
            'type': 'integer'
        },
        'name': {
            'type': 'string'
        },
        'parent': {
            'type': 'integer',
            'nullable': True
        },
        'object_id': {
            'type': 'integer',
            'nullable': True
        },
        'type_id': {
            'type': 'integer',
        },
        'type_label': {
            'type': 'string',
        },
        'type_icon': {
            'type': 'string',
            'default': 'fas fa-cube'
        },
        'type_selectable': {
            'type': 'boolean',
            'default': True
        },
    }

# ---------------------------------------------------- CONSTRUCTOR --------------------------------------------------- #

    def __init__(self, name: str,
                 parent: int,
                 object_id: int,
                 type_id: int,
                 type_label: str,
                 type_icon: str = "fas fa-cube",
                 type_selectable = True,
                 **kwargs):
        """
        Initialisation of location

        Args:
            name (str): name of location displayed in location tree
            parent (int): id of parent location
            object_id (int): id of object who has this parent
            type_id (int): id of type for which this location is set
            type_label (str): label of type for which this location is set
            type_icon (str): icon of type for which this location is set, default is 'fas fa-cube'
            type_selectable (bool): sets if this type is selectable as a parent for other locations, default is yes
        """
        self.name: str = name
        self.parent: int = parent
        self.object_id: int = object_id
        self.type_id: int = type_id
        self.type_label: str = type_label
        self.type_icon: str = type_icon
        self.type_selectable: bool = type_selectable
        super().__init__(**kwargs)

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict, *args, **kwargs) -> "CmdbLocation":
        """
        Returns an Instance of CmdbLocation

        Args:
            data (dict): Dict which contains parameters to initiate a CmdbLocation 

        Returns:
            (CmdbLocation): Instance of CmdbLocation with data from dict
        """
        return cls(
            public_id = data.get('public_id'),
            name = data.get('name'),
            parent = data.get('parent'),
            object_id = data.get('object_id'),
            type_id = data.get('type_id'),
            type_label = data.get('type_label'),
            type_icon = data.get('type_icon', 'fas fa-cube'),
            type_selectable = data.get('type_selectable', True),
        )


    @classmethod
    def to_json(cls, instance: "CmdbLocation") -> dict:
        """
        Convert a CmdbLocation instance to json conform data

        Args:
            instance (CmdbLocation): Instance of CmdbLocation

        Returns:
            (dict): Json conform dict 
        """
        return {
            'public_id': instance.get_public_id(),
            'name': instance.name,
            'parent': instance.parent,
            'object_id': instance.object_id,
            'type_id': instance.type_id,
            'type_label': instance.type_label,
            'type_icon': instance.type_icon,
            'type_selectable': instance.type_selectable,
        }


    @classmethod
    def to_data(cls, instance: "CmdbLocation") -> dict:
        """
        Dict representation of a CmdbLocation
        """
        return {
            'public_id': instance['public_id'],
            'name': instance['name'],
            'parent': instance['parent'],
            'object_id': instance['object_id'],
            'type_id': instance['type_id'],
            'type_label': instance['type_label'],
            'type_icon': instance['type_icon'],
            'type_selectable': instance['type_selectable'],
        }


    @classmethod
    def to_dict(cls, instance: "CmdbLocation") -> dict:
        """
        Not used
        """
        return []
