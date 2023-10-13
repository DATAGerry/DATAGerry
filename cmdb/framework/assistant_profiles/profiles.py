# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
This file contans all profile data and logics for the initial assistant
"""
import logging
from enum import Enum
# from typing import List
from datetime import datetime, timezone

from flask import current_app

from cmdb.framework import TypeModel
from cmdb.framework.managers.type_manager import TypeManager
from cmdb.framework.cmdb_object_manager import CmdbObjectManager


LOGGER = logging.getLogger(__name__)


class ProfileName(str, Enum):
    """
    Enumeration of all valid profile names which can be created through the initial assistant
    
    Args:
        Enum (str): Name of a profile
    """
    HARDWARE_INVENTORY = 'hardware-inventory-profile'
    SOFTWARE = 'software-profile'


class ProfileAssistant:
    """
    This class holds all profiles and logics for the initial assistant
    """

    def __init__(self):
        with current_app.app_context():
            self.type_manager: TypeManager = TypeManager(current_app.database_manager)
            self.object_manager: CmdbObjectManager = CmdbObjectManager(current_app.database_manager)



# -------------------------------------------------------------------------------------------------------------------- #
#                                                   PROFILE CREATION                                                   #
# -------------------------------------------------------------------------------------------------------------------- #

    def create_profiles(self, profile_list):
        """
        Creates types from profiles in the profile_list

        Args:
            profile_list: List of profiles which should be created
        """
        created_ids = []
        LOGGER.info(f"create_profiles with: {profile_list}")

        for profile in profile_list:
            LOGGER.info(f"cur_profile: {profile}")
            LOGGER.info(f"ProfileName.HARDWARE_INVENTORY: {ProfileName.HARDWARE_INVENTORY}")

            if profile == ProfileName.HARDWARE_INVENTORY:
                LOGGER.info("Profile HARDWARE_INVENTORY")
                new_ids = self.create_hardware_inventory_profile()
                created_ids.append(new_ids)

        return created_ids



    def create_hardware_inventory_profile(self):
        """
        Creates all types of the assistant profile "hardware-inventory-profile"
        """
        created_ids = []

        initial_type = self.get_hardware_inventory_profile_initial()
        initial_type['public_id'] = self.object_manager.get_new_id(TypeModel.COLLECTION)

        # create initial type and save publicID
        owner_type_id: int = self.type_manager.insert(initial_type)
        created_ids.append(owner_type_id)

        # get all dependant types
        dependent_types = self.get_hardware_inventory_profile_dependent_types(owner_type_id)

        # create all dependant types
        for cur_type in dependent_types:
            cur_type['public_id'] = self.object_manager.get_new_id(TypeModel.COLLECTION)
            cur_type_id = self.type_manager.insert(cur_type)
            created_ids.append(cur_type_id)

        return created_ids

# -------------------------------------------------------------------------------------------------------------------- #
#                                                     PROFILE DATA                                                     #
# -------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------ HARDWARE - INVENTORY - PROFILE ------------------------------------------ #

    def get_hardware_inventory_profile_initial(self) -> dict:
        """
        Returns the initial required type which first need to be created due to refereces 

        Returns:
            dict: TypeModel of owner type
        """
        return {
                "name": "owner",
                "active": True,
                "author_id": 1,
                "creation_time": datetime.now(timezone.utc),
                "editor_id": None,
                "last_edit_time": None,
                "label": "Owner",
                "version": "1.0.0",
                "description": None,
                "render_meta": {
                    "icon": "fa fa-user",
                    "sections": [{
                        "type": "section",
                        "name": "owner",
                        "label": "General",
                        "fields": [
                            "firstname",
                            "lastname",
                            "mail",
                            "username"
                        ]
                    }],
                    "externals": [],
                    "summary": {
                        "fields": [
                        "firstname",
                        "lastname"
                        ]
                    }
                },
                "fields": [
                    {
                        "type": "text",
                        "name": "firstname",
                        "label": "Firstname"
                    },
                    {
                        "type": "text",
                        "name": "lastname",
                        "label": "Lastname"
                    },
                    {
                        "type": "text",
                        "name": "mail",
                        "label": "Mail"
                    },
                    {
                        "type": "text",
                        "name": "username",
                        "label": "Username"
                    }
                ],
                "acl": {
                    "activated": False,
                    "groups": {
                        "includes": {}
                    }
                }
            }

    def get_hardware_inventory_profile_dependent_types(self, owner_type_id: int) -> list:
        """
        Sets the public_id of owner-Type in References and returns all types which need to be
        created for the profile 'hardware-inventory-profile'
        
        Args:
            ownerTypeID (int): public_id of owner-Type

        Returns:
            dict: All depedent types for the hardware-inventory-profile
        """
        return [
            {
                "name": "VirtualServer",
                "active": True,
                "author_id": 1,
                "creation_time": datetime.now(timezone.utc),
                "editor_id": None,
                "last_edit_time": None,
                "label": "Virtual Server",
                "version": "1.0.0",
                "description": None,
                "render_meta": {
                    "icon": "fa fa-cube",
                    "sections": [
                        {
                            "type": "section",
                            "name": "general",
                            "label": "General",
                            "fields": [
                                "name",
                                "inventoryno",
                                "purpose"
                            ]
                        },
                        {
                            "type": "section",
                            "name": "cpu",
                            "label": "CPU",
                            "fields": [
                                "cpu",
                                "cpu_type"
                            ]
                        },
                        {
                            "type": "section",
                            "name": "model",
                            "label": "Model",
                            "fields": [
                                "manufacturer",
                                "model",
                                "serial"
                            ]
                        },
                        {
                            "type": "section",
                            "name": "os",
                            "label": "Operation System",
                            "fields": [
                                "os",
                                "version"
                            ]
                        },
                        {
                            "type": "section",
                            "name": "userassignment",
                            "label": "Userassignment",
                            "fields": [
                                "userassigment-ref"
                            ]
                        }
                    ],
                    "externals": [
                        {
                            "name": "loginventory",
                            "href": "http://20.224.182.51/LOGINventory9/details.aspx?pcuid={}",
                            "label": "Loginventory",
                            "icon": "fas fa-external-link-alt",
                            "fields": [
                                "name"
                            ]
                        }
                    ],
                    "summary": {
                        "fields": [
                            "name",
                            "inventoryno",
                            "serial",
                            "os",
                            "userassigment-ref"
                        ]
                    }
                },
                "fields": [
                    {
                        "type": "text",
                        "name": "name",
                        "label": "Name"
                    },
                    {
                        "type": "text",
                        "name": "inventoryno",
                        "label": "Inventory No."
                    },
                    {
                        "type": "text",
                        "name": "manufacturer",
                        "label": "Manufacturer"
                    },
                    {
                        "type": "text",
                        "name": "model",
                        "label": "Model"
                    },
                    {
                        "type": "text",
                        "name": "serial",
                        "label": "Serialnumber"
                    },
                    {
                        "type": "text",
                        "name": "purpose",
                        "label": "Purpose"
                    },
                    {
                        "type": "text",
                        "name": "os",
                        "label": "Operation System"
                    },
                    {
                        "type": "text",
                        "name": "version",
                        "label": "Version"
                    },
                    {
                        "type": "text",
                        "name": "cpu",
                        "label": "CPU"
                    },
                    {
                        "type": "text",
                        "name": "cpu_type",
                        "label": "Type"
                    },
                    {
                        "type": "ref",
                        "name": "userassigment-ref",
                        "label": "Userassignment",
                        "ref_types": [
                            owner_type_id
                        ],
                        "summaries": []
                    }
                ],
                "acl": {
                    "activated": False,
                    "groups": {
                        "includes": {}
                    }
                }
            } # end 'VirtualServer'
        ]
