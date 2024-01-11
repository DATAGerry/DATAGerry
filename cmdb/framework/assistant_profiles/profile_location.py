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
This module manages the 'Location'-Profile for the DATAGERRY assistant
"""
import logging

from cmdb.framework.assistant_profiles.profile_base_class import ProfileBase
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class LocationProfile(ProfileBase):
    """
    This class cointains all types and logics for the 'Location'-Profile
    """
    def __init__(self, created_type_ids: dict):
        self.created_type_ids = created_type_ids
        super().__init__(created_type_ids)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                       FUNCTIONS                                                      #
# -------------------------------------------------------------------------------------------------------------------- #


    def create_location_profile(self) -> dict:
        """
        Creates all types from the 'Location'- Profile

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
        country_type_data = self.get_country_type()
        self.create_basic_type('country_id',country_type_data)



    def _create_remaining_types(self):
        """
        Creates all remaining types of this profile
        """
        # city type
        city_type_data = self.get_city_type()
        self.create_basic_type('city_id', city_type_data)

        # building type
        building_type_data = self.get_building_type()
        self.create_basic_type('building_id', building_type_data)

        # room type
        room_type_data = self.get_room_type()
        self.create_basic_type('room_id', room_type_data)

        # rack type
        rack_type_data = self.get_rack_type()
        self.create_basic_type('rack_id', rack_type_data)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                  TYPE DATA - SECTION                                                 #
# -------------------------------------------------------------------------------------------------------------------- #


    def get_country_type(self) -> dict:
        """
        Returns the 'Country'-Type for the 'Location'-Profile
        """
        return {
            "name": "country",
            "selectable_as_parent": True,
            "global_template_ids": [],
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Country",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "far fa-flag",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-15910",
                        "label": "Information",
                        "fields": [
                            "text-84872"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-58608",
                        "label": "Location",
                        "fields": [
                            "dg_location"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-84872"
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-84872",
                    "label": "Name"
                },
                {
                    "type": "location",
                    "name": "dg_location",
                    "label": "Location"
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


    def get_city_type(self) -> dict:
        """
        Returns the 'City'-Type for the 'Location'-Profile

        Args:
            country_type_id (int): public_id of created 'Country'-Type
        """
        return {
            "name": "city",
            "selectable_as_parent": True,
            "global_template_ids": [],
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "City",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-city",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-57114",
                        "label": "Information",
                        "fields": [
                            "text-31555"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-88673",
                        "label": "Location",
                        "fields": [
                            "dg_location"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-31555",
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-31555",
                    "label": "Name"
                },
                {
                    "type": "location",
                    "name": "dg_location",
                    "label": "Location"
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


    def get_building_type(self) -> dict:
        """
        Returns the 'Building'-Type for the 'Location'-Profile

        Args:
            country_type_id (int): public_id of created 'Country'-Type
            city_type_id (int): public_id of created 'City'-Type
        """
        return {
            "name": "building",
            "selectable_as_parent": True,
            "global_template_ids": [],
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Building",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-hotel",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-67402",
                        "label": "Information",
                        "fields": [
                            "text-56569"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-17996",
                        "label": "Address",
                        "fields": [
                            "text-28009",
                            "text-24247",
                            "text-36479"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-14059",
                        "label": "Location",
                        "fields": [
                            "dg_location"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-56569",
                        "text-28009",
                        "text-24247",
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-56569",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-28009",
                    "label": "Street"
                },
                {
                    "type": "text",
                    "name": "text-36479",
                    "label": "Postal code"
                },
                {
                    "type": "text",
                    "name": "text-24247",
                    "label": "House number"
                },
                {
                    "type": "location",
                    "name": "dg_location",
                    "label": "Location"
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


    def get_room_type(self) -> dict:
        """
        Returns the 'Room'-Type for the 'Location'-Profile

        Args:
            country_type_id (int): public_id of created 'Country'-Type
            city_type_id (int): public_id of created 'City'-Type
            building_type_id (int): public_id of created 'Building'-Type
        """
        return {
            "name": "room",
            "selectable_as_parent": True,
            "global_template_ids": [],
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Room",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fa fa-cube",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-11343",
                        "label": "Information",
                        "fields": [
                            "text-72385"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-48412",
                        "label": "Room details",
                        "fields": [
                            "text-30789",
                            "text-59951",
                            "dg_location"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-72385",
                        "text-30789",
                        "text-59951",
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-72385",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-30789",
                    "label": "Room number"
                },
                {
                    "type": "text",
                    "name": "text-59951",
                    "label": "Floor"
                },
                {
                    "type": "location",
                    "name": "dg_location",
                    "label": "Location"
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


    def get_rack_type(self) -> dict:
        """
        Returns the 'Rack'-Type for the 'Location'-Profile

        Args:
            country_type_id (int): public_id of created 'Country'-Type
            city_type_id (int): public_id of created 'City'-Type
            building_type_id (int): public_id of created 'Building'-Type
            room_type_id (int): public_id of created 'Room'-Type
        """
        return {
            "name": "rack",
            "selectable_as_parent": True,
            "global_template_ids": [],
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Rack",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-th-large",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-39958",
                        "label": "Information",
                        "fields": [
                            "text-65752"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-19942",
                        "label": "Rack details",
                        "fields": [
                            "text-58970",
                            "text-75963"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-55832",
                        "label": "Location",
                        "fields": [
                            "dg_location"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-65752",
                        "ref-66941"
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-65752",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-58970",
                    "label": "Height units"
                },
                {
                    "type": "text",
                    "name": "text-75963",
                    "label": "Form factor"
                },
                {
                    "type": "location",
                    "name": "dg_location",
                    "label": "Location"
                }
            ],
            "acl": {
                "activated": False,
                "groups": {
                    "includes": {}
                }
            }
        }
