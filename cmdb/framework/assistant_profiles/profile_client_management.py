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
This module manages the 'Client Management'-Profile for the DATAGERRY assistant
"""

import logging

from cmdb.framework.assistant_profiles.profile_base_class import ProfileBase


LOGGER = logging.getLogger(__name__)
# -------------------------------------------------------------------------------------------------------------------- #


class ClientManagementProfile(ProfileBase):
    """
    This class cointains all types and logics for the 'Client Management'-Profile
    """

    def __init__(self, created_type_ids: dict):
        super().__init__(created_type_ids)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                       FUNCTIONS                                                      #
# -------------------------------------------------------------------------------------------------------------------- #


    def create_client_management_profile(self) -> dict:
        """
        Creates all types from the 'Client Management'- Profile

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
        # operating system type
        operating_system_type_data = self.get_operating_system_type()
        self.create_basic_type('operating_system_id',operating_system_type_data)

        # client type
        client_type_data = self.get_client_type()
        self.create_basic_type('client_id', client_type_data)


    def _create_remaining_types(self):
        """
        Creates all remaining types of this profile
        """
        # monitor type
        monitor_type_data = self.get_monitor_type(self.created_type_ids['client_id'])
        self.create_basic_type('monitor_id', monitor_type_data)

        #printer type
        printer_type_data = self.get_printer_type()
        self.create_basic_type('printer_id', printer_type_data)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                  TYPE DATA - SECTION                                                 #
# -------------------------------------------------------------------------------------------------------------------- #


    def get_client_type(self) -> dict:
        """
        Returns the 'Client'-Type for the 'Client Management'-Profile
        """
        type_prefix = 'client'

        self.type_dict[type_prefix]: dict = {
            "name": "client",
            "selectable_as_parent": True,
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Client",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "far fa-id-card",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-68471",
                        "label": "Information",
                        "fields": [
                            "text-98758"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-71276",
                        "label": "Device details",
                        "fields": [
                            "select-74684",
                            "text-83017",
                            "text-80085",
                            "text-18783"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-36497",
                        "label": "IP data",
                        "fields": [
                            "text-10453",
                            "text-26209",
                            # "ref-40300" #network
                        ]
                    },
                    # { #os
                    #     "type": "section",
                    #     "name": "section-44174",
                    #     "label": "Operating system",
                    #     "fields": [
                    #         "ref-47570"
                    #     ]
                    # },
                    # {
                    #     "type": "section",
                    #     "name": "section-11686",
                    #     "label": "Location",
                    #     "fields": [
                    #         "ref-67470"
                    #     ]
                    # },
                    # {
                    #     "type": "section",
                    #     "name": "section-16359",
                    #     "label": "User assignment",
                    #     "fields": [
                    #         "ref-58324"
                    #     ]
                    # }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-98758",
                        "select-74684",
                        # "ref-67470" #locations
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-98758",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-83017",
                    "label": "Manufacturer"
                },
                {
                    "type": "text",
                    "name": "text-80085",
                    "label": "Model"
                },
                {
                    "type": "text",
                    "name": "text-18783",
                    "label": "Serial number"
                },
                {
                    "type": "select",
                    "name": "select-74684",
                    "label": "Type",
                    "options": [
                        {
                            "name": "Notebook",
                            "label": "Notebook"
                        },
                        {
                            "name": "Desktop",
                            "label": "Desktop"
                        }
                    ]
                },
                {
                    "type": "text",
                    "name": "text-10453",
                    "label": "IP"
                },
                {
                    "type": "text",
                    "name": "text-26209",
                    "label": "Hostname"
                },
                # { #client
                #     "type": "ref",
                #     "name": "ref-40300",
                #     "label": "Network",
                #     "ref_types": [
                #     25
                #     ],
                #     "summaries": []
                # },
                # { #os
                #     "type": "ref",
                #     "name": "ref-47570",
                #     "label": "OS",
                #     "ref_types": [
                #     24
                #     ],
                #     "summaries": []
                # },
                # { #locations
                #     "type": "ref",
                #     "name": "ref-67470",
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
                # { #users
                #     "type": "ref",
                #     "name": "ref-58324",
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

        # get the fields and sections of client type
        client_type_fields: list = self.type_dict[type_prefix]['fields']
        client_type_sections: list = self.type_dict[type_prefix]['render_meta']['sections']

        # Add the network profile dependencies
        network_type_id = self.created_type_ids['network_id']

        if network_type_id:
            network_field_name = "ref-40300"

            client_type_fields.append(
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

            self.set_type_section_field(type_prefix,'section-36497',network_field_name)


        # Add the operating system profile dependencies
        operating_system_id = self.created_type_ids['operating_system_id']

        if operating_system_id:
            os_field_name = 'ref-47570'

            client_type_fields.append(
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

            client_type_sections.append(
                {
                    "type": "section",
                    "name": "section-44174",
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
            locations_field_name = 'ref-67470'

            client_type_fields.append(
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

            client_type_sections.append(
                {
                    "type": "section",
                    "name": "section-11686",
                    "label": "Location",
                    "fields": [
                        locations_field_name
                    ]
                }
            )

            self.set_type_summary_field(type_prefix, locations_field_name)


        # Add the user management profile dependencies
        user_id = self.created_type_ids['user_id']
        customer_user_id = self.created_type_ids['customer_user_id']

        if user_id and customer_user_id:
            users_field_name = 'ref-58324'

            client_type_fields.append(
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

            client_type_sections.append(
                {
                    "type": "section",
                    "name": "section-16359",
                    "label": "User assignment",
                    "fields": [
                        users_field_name
                    ]
                }
            )


        return self.type_dict[type_prefix]


# -------------------------------------------------------------------------------------------------------------------- #

    def get_operating_system_type(self) -> dict:
        """
        Returns the 'Operating System'-Type for the 'Client Management'-Profile
        """
        return {
            "name": "operating_system",
            "selectable_as_parent": True,
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Operating System",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "far fa-window-maximize",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-72042",
                        "label": "Information",
                        "fields": [
                            "text-42835"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-64253",
                        "label": "Version details",
                        "fields": [
                            "text-25407",
                            "text-49533"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-42835",
                        "text-25407",
                        "text-49533"
                    ]
                }
            },
            "fields": [
            {
                "type": "text",
                "name": "text-42835",
                "label": "Name"
            },
            {
                "type": "text",
                "name": "text-25407",
                "label": "Version"
            },
            {
                "type": "text",
                "name": "text-49533",
                "label": "Variant"
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


    def get_monitor_type(self, client_type_id: int) -> dict:
        """
        Returns the 'Monitor'-Type for the 'Client Management'-Profile
        """
        type_prefix = 'monitor'

        self.type_dict[type_prefix] = {
            "name": "monitor",
            "selectable_as_parent": True,
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Monitor",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-desktop",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-28964",
                        "label": "Information",
                        "fields": [
                            "text-39536"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-38508",
                        "label": "Device details",
                        "fields": [
                            "text-80518",
                            "text-94163",
                            "text-36637"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-51050",
                        "label": "Device assignment",
                        "fields": [
                            "ref-12314"
                        ]
                    },
                    # { #locations
                    #     "type": "section",
                    #     "name": "section-39684",
                    #     "label": "Location",
                    #     "fields": [
                    #         "ref-98114"
                    #     ]
                    # }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-39536",
                        "text-94163",
                        # "ref-98114" #locations
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-39536",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-80518",
                    "label": "Manufacturer"
                },
                {
                    "type": "text",
                    "name": "text-94163",
                    "label": "Model"
                },
                {
                    "type": "text",
                    "name": "text-36637",
                    "label": "Serial number"
                },
                {
                    "type": "ref",
                    "name": "ref-12314",
                    "label": "Device",
                    "ref_types": [
                        client_type_id
                    ],
                    "summaries": []
                },
                # { #locations
                #     "type": "ref",
                #     "name": "ref-98114",
                #     "label": "Location",
                #     "ref_types": [
                #     20,
                #     19,
                #     18,
                #     17
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

        # get the fields and sections of client type
        monitor_type_fields: list = self.type_dict[type_prefix]['fields']
        monitor_type_sections: list = self.type_dict[type_prefix]['render_meta']['sections']

        # Add the location profile dependencies
        country_id = self.created_type_ids['country_id']
        city_id = self.created_type_ids['city_id']
        building_id = self.created_type_ids['building_id']
        room_id = self.created_type_ids['room_id']
        rack_id = self.created_type_ids['rack_id']

        if country_id and city_id and building_id and room_id and rack_id:
            locations_field_name = 'ref-98114'

            monitor_type_fields.append(
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

            monitor_type_sections.append(
                {
                    "type": "section",
                    "name": "section-39684",
                    "label": "Location",
                    "fields": [
                        locations_field_name
                    ]
                }
            )

            self.set_type_summary_field(type_prefix, locations_field_name)


        return self.type_dict[type_prefix]


# -------------------------------------------------------------------------------------------------------------------- #


    def get_printer_type(self) -> dict:
        """
        Returns the 'Printer'-Type for the 'Client Management'-Profile
        """
        type_prefix = 'printer'

        self.type_dict[type_prefix] = {
            "name": "printer",
            "selectable_as_parent": True,
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Printer",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-print",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-95376",
                        "label": "Information",
                        "fields": [
                            "text-78614"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-79154",
                        "label": "Device details",
                        "fields": [
                            "text-81596",
                            "text-66585",
                            "text-28052"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-36988",
                        "label": "IP data",
                        "fields": [
                            "text-73582",
                            "text-97953",
                            # "ref-90293" #network
                        ]
                    },
                    # { #location
                    #     "type": "section",
                    #     "name": "section-88306",
                    #     "label": "Location",
                    #     "fields": [
                    #         "ref-45614"
                    #     ]
                    # }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-78614",
                        "text-66585",
                        # "ref-45614" #location
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-78614",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-28052",
                    "label": "Serial number"
                },
                {
                    "type": "text",
                    "name": "text-66585",
                    "label": "Model"
                },
                {
                    "type": "text",
                    "name": "text-81596",
                    "label": "Manufacturer"
                },
                {
                    "type": "text",
                    "name": "text-97953",
                    "label": "Hostname"
                },
                {
                    "type": "text",
                    "name": "text-73582",
                    "label": "IP"
                },
                # { #network
                #     "type": "ref",
                #     "name": "ref-90293",
                #     "label": "Network",
                #     "ref_types": [
                #     25
                #     ],
                #     "summaries": []
                # },
                # { #location
                #     "type": "ref",
                #     "name": "ref-45614",
                #     "label": "Location",
                #     "ref_types": [
                #     20,
                #     19,
                #     18,
                #     17
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

        # get the fields and sections of client type
        printer_type_fields: list = self.type_dict[type_prefix]['fields']
        printer_type_sections: list = self.type_dict[type_prefix]['render_meta']['sections']

        # Add the network profile dependencies
        network_type_id = self.created_type_ids['network_id']

        if network_type_id:
            network_field_name = "ref-90293"

            printer_type_fields.append(
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

            self.set_type_section_field(type_prefix,'section-36988',network_field_name)


        # Add the location profile dependencies
        country_id = self.created_type_ids['country_id']
        city_id = self.created_type_ids['city_id']
        building_id = self.created_type_ids['building_id']
        room_id = self.created_type_ids['room_id']
        rack_id = self.created_type_ids['rack_id']

        if country_id and city_id and building_id and room_id and rack_id:
            locations_field_name = 'ref-45614'

            printer_type_fields.append(
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

            printer_type_sections.append(
                {
                    "type": "section",
                    "name": "section-88306",
                    "label": "Location",
                    "fields": [
                        locations_field_name
                    ]
                }
            )

            self.set_type_summary_field(type_prefix, locations_field_name)

        return self.type_dict[type_prefix]
