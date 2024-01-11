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
This module manages the 'Network Infrastructure'-Profile for the DATAGERRY assistant
"""
import logging

from cmdb.framework.assistant_profiles.profile_base_class import ProfileBase
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)



class NetworkInfrastructureProfile(ProfileBase):
    """
    This class cointains all types and logics for the 'Network Infrastructure'-Profile
    """
    def __init__(self, created_type_ids: dict):
        self.created_type_ids = created_type_ids
        super().__init__(created_type_ids)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                       FUNCTIONS                                                      #
# -------------------------------------------------------------------------------------------------------------------- #
    def create_network_infrastructure_profile(self) -> dict:
        """
        Creates all types from the 'Network Infrastructure'- Profile

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
        #switch type
        switch_type_data = self.get_switch_type()
        self.create_basic_type('switch_id', switch_type_data)


    def _create_remaining_types(self):
        """
        Creates all remaining types of this profile
        """
        # router type
        router_type_data = self.get_router_type()
        self.create_basic_type('router_id', router_type_data)

        #patch_panel type
        patch_panel_type_data = self.get_patch_panel_type()
        self.create_basic_type('patch_panel_id', patch_panel_type_data)

        # wireless_access_point type
        wap_type_data = self.get_wireless_access_point_type()
        self.create_basic_type('wireless_access_point_id', wap_type_data)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                  TYPE DATA - SECTION                                                 #
# -------------------------------------------------------------------------------------------------------------------- #


    def get_switch_type(self) -> dict:
        """
        Returns the 'Switch'-Type for the 'Network Infrastructure'-Profile
        """
        type_prefix = 'switch'

        self.type_dict[type_prefix] = {
            "name": "switch",
            "selectable_as_parent": True,
            "global_template_ids": [],
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Switch",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "far fa-object-ungroup",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-25269",
                        "label": "Information",
                        "fields": [
                            "text-60980"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-49431",
                        "label": "Device details",
                        "fields": [
                            "text-68257",
                            "text-73474",
                            "text-52277"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-84185",
                        "label": "IP data",
                        "fields": [
                            "text-64937",
                            "text-93057",
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-78906",
                        "label": "Location",
                        "fields": [
                            "text-63030",
                            "text-45199",
                            "dg_location"
                        ]
                    },
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-60980",
                        "text-73474",
                        "text-45199",
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-60980",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-68257",
                    "label": "Manufacturer"
                },
                {
                    "type": "text",
                    "name": "text-52277",
                    "label": "Serial number"
                },
                {
                    "type": "text",
                    "name": "text-73474",
                    "label": "Model"
                },
                {
                    "type": "text",
                    "name": "text-93057",
                    "label": "Hostname"
                },
                {
                    "type": "text",
                    "name": "text-64937",
                    "label": "IP"
                },
                {
                    "type": "text",
                    "name": "text-45199",
                    "label": "Rack position"
                },
                {
                    "type": "text",
                    "name": "text-63030",
                    "label": "Height unit"
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


        # get the fields and sections of switch type
        switch_type_fields: list = self.type_dict[type_prefix]['fields']
        switch_type_sections: list = self.type_dict[type_prefix]['render_meta']['sections']


        # Add the network profile dependencies
        network_type_id = self.created_type_ids['network_id']

        if network_type_id:
            network_field_name = "ref-47742"

            switch_type_fields.append(
                {
                    "type": "ref",
                    "name": network_field_name,
                    "label": "Network",
                    "ref_types": [
                        network_type_id
                    ],
                    "summaries": []
                }
            )

            self.set_type_section_field(type_prefix,'section-84185',network_field_name)


        # Add the operating system profile dependencies
        operating_system_id = self.created_type_ids['operating_system_id']

        if operating_system_id:
            os_field_name = 'ref-71899'

            switch_type_fields.append(
                {
                    "type": "ref",
                    "name": os_field_name,
                    "label": "OS",
                    "ref_types": [
                        operating_system_id
                    ],
                    "summaries": []
                }
            )

            switch_type_sections.append(
                {
                    "type": "section",
                    "name": "section-13463",
                    "label": "Operating system",
                    "fields": [
                        os_field_name
                    ]
                }
            )


        # Add the user management profile dependencies
        user_id = self.created_type_ids['user_id']
        customer_user_id = self.created_type_ids['customer_user_id']

        if user_id and customer_user_id:
            users_field_name = 'ref-41420'

            switch_type_fields.append(
                {
                    "type": "ref",
                    "name": users_field_name,
                    "label": "User",
                    "ref_types": [
                        user_id,
                        customer_user_id
                    ],
                    "summaries": []
                }
            )

            switch_type_sections.append(
                {
                    "type": "section",
                    "name": "section-73669",
                    "label": "User assignment",
                    "fields": [
                        users_field_name
                    ]
                }
            )


        return self.type_dict[type_prefix]


# -------------------------------------------------------------------------------------------------------------------- #


    def get_router_type(self):
        """
        Returns the 'Router'-Type for the 'Network Infrastructure'-Profile
        """
        type_prefix:str = 'router'

        self.type_dict[type_prefix] =   {
            "name": "router",
            "selectable_as_parent": True,
            "global_template_ids": [],
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Router",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-route",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-64712",
                        "label": "Information",
                        "fields": [
                            "text-60624"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-38599",
                        "label": "Device details",
                        "fields": [
                            "text-84004",
                            "text-99041",
                            "text-23458"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-47066",
                        "label": "IP data",
                        "fields": [
                            "text-70642",
                            "text-98052",
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-98615",
                        "label": "Location",
                        "fields": [
                            "text-65711",
                            "text-19482",
                            "dg_location"
                        ]
                    },
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-60624",
                        "text-99041",
                        "text-19482",
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-60624",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-84004",
                    "label": "Manufacturer"
                },
                {
                    "type": "text",
                    "name": "text-23458",
                    "label": "Serial number"
                },
                {
                    "type": "text",
                    "name": "text-99041",
                    "label": "Model"
                },
                {
                    "type": "text",
                    "name": "text-98052",
                    "label": "Hostname"
                },
                {
                    "type": "text",
                    "name": "text-70642",
                    "label": "IP"
                },
                {
                    "type": "text",
                    "name": "text-19482",
                    "label": "Rack position"
                },
                {
                    "type": "text",
                    "name": "text-65711",
                    "label": "Height unit"
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


        # get the fields and sections of router type
        router_type_fields: list = self.type_dict[type_prefix]['fields']
        router_type_sections: list = self.type_dict[type_prefix]['render_meta']['sections']


        # Add the network profile dependencies
        network_type_id = self.created_type_ids['network_id']

        if network_type_id:
            network_field_name = "ref-12104"

            router_type_fields.append(
                {
                    "type": "ref",
                    "name": network_field_name,
                    "label": "Network",
                    "ref_types": [
                        network_type_id
                    ],
                    "summaries": []
                }
            )

            self.set_type_section_field(type_prefix,'section-47066',network_field_name)


        # Add the operating system profile dependencies
        operating_system_id = self.created_type_ids['operating_system_id']

        if operating_system_id:
            os_field_name = 'ref-68233'

            router_type_fields.append(
                {
                    "type": "ref",
                    "name": os_field_name,
                    "label": "OS",
                    "ref_types": [
                        operating_system_id
                    ],
                    "summaries": []
                }
            )

            router_type_sections.append(
                {
                    "type": "section",
                    "name": "section-68634",
                    "label": "Operating system",
                    "fields": [
                        os_field_name
                    ]
                }
            )


        # Add the user management profile dependencies
        user_id = self.created_type_ids['user_id']
        customer_user_id = self.created_type_ids['customer_user_id']

        if user_id and customer_user_id:
            users_field_name = 'ref-58400'

            router_type_fields.append(
                {
                    "type": "ref",
                    "name": users_field_name,
                    "label": "User",
                    "ref_types": [
                        user_id,
                        customer_user_id
                    ],
                    "summaries": []
                }
            )

            router_type_sections.append(
                {
                    "type": "section",
                    "name": "section-27633",
                    "label": "User assignment",
                    "fields": [
                        users_field_name
                    ]
                }
            )

        return self.type_dict[type_prefix]


# -------------------------------------------------------------------------------------------------------------------- #


    def get_patch_panel_type(self):
        """
        Returns the 'Patch Panel'-Type for the 'Network Infrastructure'-Profile
        """
        type_prefix:str = 'patch_panel'

        self.type_dict[type_prefix] =   {
            "name": "patch_panel",
            "selectable_as_parent": True,
            "global_template_ids": [],
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Patch Panel",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-bezier-curve",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-51132",
                        "label": "Information",
                        "fields": [
                            "text-89632"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-18951",
                        "label": "Device details",
                        "fields": [
                            "text-94530",
                            "text-23594"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-99357",
                        "label": "Location",
                        "fields": [
                            "text-68993",
                            "text-18143",
                            "dg_location"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-89632",
                        "text-23594",
                        "text-18143",
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-89632",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-23594",
                    "label": "Model"
                },
                {
                    "type": "text",
                    "name": "text-94530",
                    "label": "Manufacturer"
                },
                {
                    "type": "text",
                    "name": "text-68993",
                    "label": "Height unit"
                },
                {
                    "type": "text",
                    "name": "text-18143",
                    "label": "Rack position"
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

        return self.type_dict[type_prefix]


# -------------------------------------------------------------------------------------------------------------------- #


    def get_wireless_access_point_type(self):
        """
        Returns the 'Wireless Access Point'-Type for the 'Network Infrastructure'-Profile
        """
        type_prefix:str = 'wireless_access_point'

        self.type_dict[type_prefix] = {
            "name": "wireless_access_point",
            "selectable_as_parent": True,
            "global_template_ids": [],
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Wireless Access Point",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-exchange-alt",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-18971",
                        "label": "Information",
                        "fields": [
                            "text-83971"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-52212",
                        "label": "Device details",
                        "fields": [
                            "text-58217",
                            "text-76317",
                            "text-71667",
                            "text-44347"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-99636",
                        "label": "IP data",
                        "fields": [
                            "text-83225",
                            "text-91633",
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-30882",
                        "label": "WIFI data",
                        "fields": [
                            "text-97978",
                            "text-60846",
                            "text-17637",
                            "text-46053",
                            "text-35494"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-67101",
                        "label": "Location",
                        "fields": [
                            "dg_location"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-83971",
                        "text-97978",
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-83971",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-71667",
                    "label": "Serial number"
                },
                {
                    "type": "text",
                    "name": "text-44347",
                    "label": "Firmware version"
                },
                {
                    "type": "text",
                    "name": "text-76317",
                    "label": "Model"
                },
                {
                    "type": "text",
                    "name": "text-58217",
                    "label": "Manufacturer"
                },
                {
                    "type": "text",
                    "name": "text-91633",
                    "label": "Hostname"
                },
                {
                    "type": "text",
                    "name": "text-83225",
                    "label": "IP"
                },
                {
                    "type": "text",
                    "name": "text-97978",
                    "label": "SSID"
                },
                {
                    "type": "text",
                    "name": "text-46053",
                    "label": "Authentification"
                },
                {
                    "type": "text",
                    "name": "text-35494",
                    "label": "Encryption"
                },
                {
                    "type": "text",
                    "name": "text-17637",
                    "label": "Channel"
                },
                {
                    "type": "text",
                    "name": "text-60846",
                    "label": "Standard"
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


        # get the fields and sections of router type
        wap_type_fields: list = self.type_dict[type_prefix]['fields']
        wap_type_sections: list = self.type_dict[type_prefix]['render_meta']['sections']


        # Add the network profile dependencies
        network_type_id = self.created_type_ids['network_id']

        if network_type_id:
            network_field_name = "ref-54236"

            wap_type_fields.append(
                {
                    "type": "ref",
                    "name": network_field_name,
                    "label": "Network",
                    "ref_types": [
                        network_type_id
                    ],
                    "summaries": []
                }
            )

            self.set_type_section_field(type_prefix,'section-99636',network_field_name)


        # Add the user management profile dependencies
        user_id = self.created_type_ids['user_id']
        customer_user_id = self.created_type_ids['customer_user_id']

        if user_id and customer_user_id:
            users_field_name = 'ref-36834'

            wap_type_fields.append(
                {
                    "type": "ref",
                    "name": users_field_name,
                    "label": "User",
                    "ref_types": [
                        user_id,
                        customer_user_id
                    ],
                    "summaries": []
                }
            )

            wap_type_sections.append(
                {
                    "type": "section",
                    "name": "section-89120",
                    "label": "User assignment",
                    "fields": [
                        users_field_name
                    ]
                }
            )


        return self.type_dict[type_prefix]
