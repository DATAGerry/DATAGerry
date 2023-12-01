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
This module manages the 'IPAM'-Profile for the DATAGERRY assistant
"""
import logging

from cmdb.framework.assistant_profiles.profile_base_class import ProfileBase
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)



class IPAMProfile(ProfileBase):
    """
    This class cointains all types and logics for the 'IPAM'-Profile
    """
    def __init__(self, created_type_ids: dict):
        self.created_type_ids = created_type_ids
        super().__init__(created_type_ids)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                       FUNCTIONS                                                      #
# -------------------------------------------------------------------------------------------------------------------- #
    def create_ipam_profile(self) -> dict:
        """
        Creates all types from the 'IPAM'- Profile

        Returns:
            dict: The created type ids dict
        """
        self._create_types_with_dependencies()
        self._create_remaining_types()

        return self.created_type_ids



    def _create_types_with_dependencies(self):
        """
        Creates all types which are a dependancy for other types
        """
        network_type_data = self.get_network_type()
        self.create_basic_type('network_id',network_type_data)



    def _create_remaining_types(self):
        """
        Creates all remaining types of this profile
        """
        vlan_type_data = self.get_vlan_type(self.created_type_ids['network_id'])
        self.create_basic_type('vlan_id', vlan_type_data)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                  TYPE DATA - SECTION                                                 #
# -------------------------------------------------------------------------------------------------------------------- #


    def get_network_type(self) -> dict:
        """
        Returns the 'Network'-Type for the 'IPAM'-Profile
        """
        return {
            "name": "network",
            "selectable_as_parent": True,
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Network",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-network-wired",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-94720",
                        "label": "Information",
                        "fields": [
                            "text-71148"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-99747",
                        "label": "Network details",
                        "fields": [
                            "text-35330",
                            "text-66245"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-71148",
                        "text-35330",
                        "text-66245"
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-71148",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-66245",
                    "label": "Suffix"
                },
                {
                    "type": "text",
                    "name": "text-35330",
                    "label": "IP"
                }
            ],
            "acl": {
                "activated": False,
                "groups": {
                    "includes": {}
                }
            }
        }


# -------------------------------------------------------------------------------------------------------------------- #


    def get_vlan_type(self, network_type_id: int) -> dict:
        """
        Returns the 'VLAN'-Type for the 'IPAM'-Profile

        Args:
            network_type_id (int): public_id of created 'Network'-Type
        """
        return {
            "name": "vlan",
            "selectable_as_parent": True,
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "VLAN",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-wave-square",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-23481",
                        "label": "Information",
                        "fields": [
                            "text-45705"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-39385",
                        "label": "VLAN data",
                        "fields": [
                            "text-78263",
                            "ref-43922"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-45705",
                        "text-78263",
                        "ref-43922"
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-45705",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-78263",
                    "label": "VLAN ID"
                },
                {
                    "type": "ref",
                    "name": "ref-43922",
                    "label": "Network",
                    "ref_types": [
                    network_type_id
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
        }
