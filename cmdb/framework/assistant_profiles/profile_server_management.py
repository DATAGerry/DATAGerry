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
This module manages the 'Server Management'-Profile for the DATAGERRY assistant
"""

import logging

from cmdb.framework.assistant_profiles.profile_base_class import ProfileBase


LOGGER = logging.getLogger(__name__)
# -------------------------------------------------------------------------------------------------------------------- #


class ServerManagementProfile(ProfileBase):
    """
    This class cointains all types and logics for the 'Server Management'-Profile
    """

    def __init__(self, created_type_ids: dict):
        super().__init__(created_type_ids)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                       FUNCTIONS                                                      #
# -------------------------------------------------------------------------------------------------------------------- #


    def create_server_management_profile(self) -> dict:
        """
        Creates all types from the 'Server Management'- Profile

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
        # server type
        server_type_data = self.get_server_type()
        self.create_basic_type('server_id', server_type_data)



    def _create_remaining_types(self):
        """
        Creates all remaining types of this profile
        """
        # appliance type
        appliance_type_data = self.get_appliance_type()
        self.create_basic_type('appliance_id', appliance_type_data)

        # virtual server type
        virtual_server_type_data = self.get_virtual_server_type(self.created_type_ids['server_id'])
        self.create_basic_type('virtual_server_id', virtual_server_type_data)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                  TYPE DATA - SECTION                                                 #
# -------------------------------------------------------------------------------------------------------------------- #


    def get_server_type(self) -> dict:
        """
        Returns the 'Server'-Type for the 'Server Management'-Profile
        """
        self.type_dict['server']: dict = {
            "name": "server",
            "selectable_as_parent": True,
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Server",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-server",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-64307",
                        "label": "Information",
                        "fields": [
                            "text-23531",
                            "select-27409"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-22961",
                        "label": "Device details",
                        "fields": [
                            "text-53460",
                            "text-13009",
                            "text-11534"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-69200",
                        "label": "IP data",
                        "fields": [
                            "text-60836",
                            "text-30849",
                            # "ref-33320" #network
                        ]
                    },
                    # { #os
                    #     "type": "section",
                    #     "name": "section-54364",
                    #     "label": "Operating system",
                    #     "fields": [
                    #         "ref-38286"
                    #     ]
                    # },
                    {
                        "type": "section",
                        "name": "section-77142",
                        "label": "Location",
                        "fields": [
                            # "ref-94753", #locations
                            "text-44118",
                            "text-79176"
                        ]
                    },
                    # { #users
                    #     "type": "section",
                    #     "name": "section-69534",
                    #     "label": "User assignment",
                    #     "fields": [
                    #         "ref-47089"
                    #     ]
                    # }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-23531",
                        # "ref-33320", #network
                        # "ref-94753" #locations
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-23531",
                    "label": "Name"
                },
                {
                    "type": "select",
                    "name": "select-27409",
                    "label": "Type",
                    "options": [
                        {
                            "name": "Example",
                            "label": "Example"
                        }
                    ]
                },
                {
                    "type": "text",
                    "name": "text-11534",
                    "label": "Serial number"
                },
                {
                    "type": "text",
                    "name": "text-13009",
                    "label": "Model"
                },
                {
                    "type": "text",
                    "name": "text-53460",
                    "label": "Manufacturer"
                },
                {
                    "type": "text",
                    "name": "text-30849",
                    "label": "Hostname"
                },
                {
                    "type": "text",
                    "name": "text-60836",
                    "label": "IP"
                },
                # { #network
                #     "type": "ref",
                #     "name": "ref-33320",
                #     "label": "Network",
                #     "ref_types": [
                #         network_type_id
                #     ],
                #     "summaries": []
                # },
                # { #os
                #     "type": "ref",
                #     "name": "ref-38286",
                #     "label": "OS",
                #     "ref_types": [
                #         operating_system_id
                #     ],
                #     "summaries": []
                # },
                # { #locations
                #     "type": "ref",
                #     "name": "ref-94753",
                #     "label": "Location",
                #     "ref_types": [
                #     20,
                #     19,
                #     18,
                #     17,
                #     16
                #     ],
                #     "summaries": []
                # },
                {
                    "type": "text",
                    "name": "text-44118",
                    "label": "Height unit"
                },
                {
                    "type": "text",
                    "name": "text-79176",
                    "label": "Rack position"
                },
                # { #users
                #     "type": "ref",
                #     "name": "ref-47089",
                #     "label": "User",
                #     "ref_types": [
                #     14,
                #     15
                #     ],
                #     "summaries": []
                # }
            ],
            "acl": {
                "activated": False,
                "groups": {
                    "includes": {}
                }
            }
        }

        # get the fields and sections of server type
        server_type_fields: list = self.type_dict['server']['fields']
        server_type_sections: list = self.type_dict['server']['render_meta']['sections']


        # Add the network profile dependencies
        network_type_id = self.created_type_ids['network_id']

        if network_type_id:
            network_field_name = "ref-33320"

            server_type_fields.append(
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

            self.set_type_section_field('server','section-69200',network_field_name)
            self.set_type_summary_field('server', network_field_name)


        # Add the operating system profile dependencies
        operating_system_id = self.created_type_ids['operating_system_id']

        if operating_system_id:
            os_field_name = 'ref-38286'

            server_type_fields.append(
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

            server_type_sections.append(
                {
                    "type": "section",
                    "name": "section-54364",
                    "label": "Operating system",
                    "fields": [
                        os_field_name
                    ]
                }
            )


        # Add the location profile dependencies
        country_id = self.created_type_ids['country_id']
        city_id = self.created_type_ids['city_id']
        building_id = self.created_type_ids['building_id']
        room_id = self.created_type_ids['room_id']
        rack_id = self.created_type_ids['rack_id']

        if country_id and city_id and building_id and room_id and rack_id:
            locations_field_name = 'ref-94753'

            server_type_fields.append(
                {
                    "type": "ref",
                    "name": locations_field_name,
                    "label": "Location",
                    "ref_types": [
                        country_id,
                        city_id,
                        building_id,
                        room_id,
                        rack_id
                    ],
                    "summaries": []
                }
            )

            self.set_type_section_field('server','section-77142',locations_field_name)
            self.set_type_summary_field('server', locations_field_name)


        # Add the user management profile dependencies
        user_id = self.created_type_ids['user_id']
        customer_user_id = self.created_type_ids['customer_user_id']

        if user_id and customer_user_id:
            users_field_name = 'ref-47089'

            server_type_fields.append(
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

            server_type_sections.append(
                {
                    "type": "section",
                    "name": "section-69534",
                    "label": "User assignment",
                    "fields": [
                        users_field_name
                    ]
                }
            )


        return self.type_dict['server']


# -------------------------------------------------------------------------------------------------------------------- #


    def get_appliance_type(self) -> dict:
        """
        Returns the 'Appliance'-Type for the 'Server Management'-Profile
        """
        self.type_dict['appliance']: dict =  {
            "name": "appliance",
            "selectable_as_parent": True,
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Appliance",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-wrench",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-63931",
                        "label": "Information",
                        "fields": [
                            "text-16979"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-34550",
                        "label": "Device details",
                        "fields": [
                            "text-41650",
                            "text-64963",
                            "text-76222"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-40962",
                        "label": "IP data",
                        "fields": [
                            "text-15804",
                            "text-40334",
                            # "ref-36028" #network
                        ]
                    },
                    # { #os
                    #     "type": "section",
                    #     "name": "section-33112",
                    #     "label": "Operating system",
                    #     "fields": [
                    #         "ref-72670"
                    #     ]
                    # },
                    {
                        "type": "section",
                        "name": "section-21475",
                        "label": "Location",
                        "fields": [
                            # "ref-62068", #locations
                            "text-23325",
                            "text-26343"
                        ]
                    },
                    # { #users
                    #     "type": "section",
                    #     "name": "section-62843",
                    #     "label": "User assignment",
                    #     "fields": [
                    #         "ref-98369"
                    #     ]
                    # }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-16979",
                        # "ref-36028", #network
                        # "ref-62068", #locations
                        "text-26343"
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-16979",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-76222",
                    "label": "Serial number"
                },
                {
                    "type": "text",
                    "name": "text-64963",
                    "label": "Model"
                },
                {
                    "type": "text",
                    "name": "text-41650",
                    "label": "Manufacturer"
                },
                {
                    "type": "text",
                    "name": "text-15804",
                    "label": "IP"
                },
                # { #network
                #     "type": "ref",
                #     "name": "ref-36028",
                #     "label": "Network",
                #     "ref_types": [
                #     25
                #     ],
                #     "summaries": []
                # },
                {
                    "type": "text",
                    "name": "text-40334",
                    "label": "Hostname"
                },
                # { #os
                #     "type": "ref",
                #     "name": "ref-72670",
                #     "label": "OS",
                #     "ref_types": [
                #     24
                #     ],
                #     "summaries": []
                # },
                # { #locations
                #     "type": "ref",
                #     "name": "ref-62068",
                #     "label": "Location",
                #     "ref_types": [
                #     20,
                #     19,
                #     18,
                #     17,
                #     16
                #     ],
                #     "summaries": []
                # },
                {
                    "type": "text",
                    "name": "text-23325",
                    "label": "Height unit"
                },
                {
                    "type": "text",
                    "name": "text-26343",
                    "label": "Rack position"
                },
                # { #users
                #     "type": "ref",
                #     "name": "ref-98369",
                #     "label": "User",
                #     "ref_types": [
                #     14,
                #     15
                #     ],
                #     "summaries": []
                # }
            ],
            "acl": {
                "activated": False,
                "groups": {
                    "includes": {}
                }
            }
        }

        # get the fields and sections of appliance type
        appliance_type_fields: list = self.type_dict['appliance']['fields']
        appliance_type_sections: list = self.type_dict['appliance']['render_meta']['sections']


        # Add the network profile dependencies
        network_type_id = self.created_type_ids['network_id']

        if network_type_id:
            network_field_name = "ref-36028"

            appliance_type_fields.append(
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

            self.set_type_section_field('appliance','section-40962',network_field_name)
            self.set_type_summary_field('appliance', network_field_name)


        # Add the operating system profile dependencies
        operating_system_id = self.created_type_ids['operating_system_id']

        if operating_system_id:
            os_field_name = 'ref-72670'

            appliance_type_fields.append(
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

            appliance_type_sections.append(
                {
                    "type": "section",
                    "name": "section-33112",
                    "label": "Operating system",
                    "fields": [
                        os_field_name
                    ]
                }
            )


        # Add the location profile dependencies
        country_id = self.created_type_ids['country_id']
        city_id = self.created_type_ids['city_id']
        building_id = self.created_type_ids['building_id']
        room_id = self.created_type_ids['room_id']
        rack_id = self.created_type_ids['rack_id']

        if country_id and city_id and building_id and room_id and rack_id:
            locations_field_name = 'ref-62068'

            appliance_type_fields.append(
                {
                    "type": "ref",
                    "name": locations_field_name,
                    "label": "Location",
                    "ref_types": [
                        country_id,
                        city_id,
                        building_id,
                        room_id,
                        rack_id
                    ],
                    "summaries": []
                }
            )

            self.set_type_section_field('appliance','section-21475',locations_field_name)
            self.set_type_summary_field('appliance', locations_field_name)


        # Add the user management profile dependencies
        user_id = self.created_type_ids['user_id']
        customer_user_id = self.created_type_ids['customer_user_id']

        if user_id and customer_user_id:
            users_field_name = 'ref-98369'

            appliance_type_fields.append(
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

            appliance_type_sections.append(
                {
                    "type": "section",
                    "name": "section-62843",
                    "label": "User assignment",
                    "fields": [
                        users_field_name
                    ]
                }
            )


        return self.type_dict['appliance']


# -------------------------------------------------------------------------------------------------------------------- #


    def get_virtual_server_type(self, server_type_id: int) -> dict:
        """
        Returns the 'Virtual Server'-Type for the 'Server Management'-Profile
        """
        self.type_dict['virtual_server']: dict = {
            "name": "virtual_server",
            "selectable_as_parent": True,
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Virtual Server",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-cubes",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-60610",
                        "label": "Information",
                        "fields": [
                            "text-70141"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-21171",
                        "label": "IP data",
                        "fields": [
                            "text-30341",
                            "text-23028",
                            # "ref-50238" #netowrk
                        ]
                    },
                    # { #os
                    #     "type": "section",
                    #     "name": "section-21793",
                    #     "label": "Operating system",
                    #     "fields": [
                    #         "ref-43625"
                    #     ]
                    # },
                    {
                        "type": "section",
                        "name": "section-28198",
                        "label": "Virtual host",
                        "fields": [
                            "ref-65439"
                        ]
                    },
                    # { #users
                    #     "type": "section",
                    #     "name": "section-29427",
                    #     "label": "User assignment",
                    #     "fields": [
                    #         "ref-63703"
                    #     ]
                    # }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-70141",
                        # "ref-50238", #network
                        "ref-65439"
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-70141",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-23028",
                    "label": "Hostname"
                },
                {
                    "type": "text",
                    "name": "text-30341",
                    "label": "IP"
                },
                # { #network
                #     "type": "ref",
                #     "name": "ref-50238",
                #     "label": "Network",
                #     "ref_types": [
                #     25
                #     ],
                #     "summaries": []
                # },
                # { #os
                #     "type": "ref",
                #     "name": "ref-43625",
                #     "label": "OS",
                #     "ref_types": [
                #     24
                #     ],
                #     "summaries": []
                # },
                {
                    "type": "ref",
                    "name": "ref-65439",
                    "label": "Server",
                    "ref_types": [
                        server_type_id
                    ],
                    "summaries": []
                },
                # { #users
                #     "type": "ref",
                #     "name": "ref-63703",
                #     "label": "User",
                #     "ref_types": [
                #     14,
                #     15
                #     ],
                #     "summaries": []
                # }
            ],
            "acl": {
                "activated": False,
                "groups": {
                    "includes": {}
                }
            }
        }

        # get the fields and sections of virtual server type
        virtual_server_type_fields: list = self.type_dict['virtual_server']['fields']
        virtual_server_type_sections: list = self.type_dict['virtual_server']['render_meta']['sections']


        # Add the network profile dependencies
        network_type_id = self.created_type_ids['network_id']

        if network_type_id:
            network_field_name = "ref-50238"

            virtual_server_type_fields.append(
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

            self.set_type_section_field('virtual_server','section-21171',network_field_name)
            self.set_type_summary_field('virtual_server', network_field_name)


        # Add the operating system profile dependencies
        operating_system_id = self.created_type_ids['operating_system_id']

        if operating_system_id:
            os_field_name = 'ref-43625'

            virtual_server_type_fields.append(
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

            virtual_server_type_sections.append(
                {
                    "type": "section",
                    "name": "section-21793",
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
            users_field_name = 'ref-63703'

            virtual_server_type_fields.append(
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

            virtual_server_type_sections.append(
                {
                    "type": "section",
                    "name": "section-29427",
                    "label": "User assignment",
                    "fields": [
                        users_field_name
                    ]
                }
            )


        return self.type_dict['virtual_server']
