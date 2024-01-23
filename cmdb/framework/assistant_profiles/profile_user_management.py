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
This module manages the 'User Management'-Profile for the DATAGERRY assistant
"""
import logging

from cmdb.framework.assistant_profiles.profile_base_class import ProfileBase
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class UserManagementProfile(ProfileBase):
    """
    This class cointains all types and logics for the 'User management'-Profile
    """
    def __init__(self, created_type_ids: dict):
        self.created_type_ids = created_type_ids
        super().__init__(created_type_ids)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                       FUNCTIONS                                                      #
# -------------------------------------------------------------------------------------------------------------------- #

    def create_user_management_profile(self) -> dict:
        """
        Creates all types from the 'User Management'- Profile

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
        company_type_data = self.get_company_type()
        self.create_basic_type('company_id',company_type_data)


    def _create_remaining_types(self):
        """
        Creates all remaining types of this profile
        """
        # user type
        user_type_data = self.get_user_type()
        self.create_basic_type('user_id', user_type_data)

        # customer_user type
        customer_user_type_data = self.get_customer_user_type(self.created_type_ids['company_id'])
        self.create_basic_type('customer_user_id', customer_user_type_data)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  TYPE DATA - SECTION                                                 #
# -------------------------------------------------------------------------------------------------------------------- #

    def get_company_type(self) -> dict:
        """
        Returns the 'Company'-Type for the 'User management'-Profile
        """
        return {
            "name": "company",
            "selectable_as_parent": True,
            "global_template_ids": [],
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Company",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-building",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-24931",
                        "label": "Information",
                        "fields": [
                            "text-19742"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-91843",
                        "label": "Adress",
                        "fields": [
                            "text-29607",
                            "text-11283",
                            "text-52606",
                            "text-36017"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                        "text-19742",
                        "text-52606"
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-19742",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-29607",
                    "label": "Street"
                },
                {
                    "type": "text",
                    "name": "text-11283",
                    "label": "House number"
                },
                {
                    "type": "text",
                    "name": "text-52606",
                    "label": "Location"
                },
                {
                    "type": "text",
                    "name": "text-36017",
                    "label": "Postal code"
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

    def get_user_type(self) -> dict:
        """
        Returns the 'User'-Type for the 'User management'-Profile
        """
        return {
            "name": "user",
            "selectable_as_parent": True,
            "global_template_ids": [],
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "User",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-male",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-92803",
                        "label": "Information",
                        "fields": [
                            "text-45910"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-23984",
                        "label": "Personal data",
                        "fields": [
                            "text-80103",
                            "text-75307",
                            "text-93543",
                            "text-16313"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                    "text-45910",
                    "text-93543"
                    ]
                }
            },
            "fields": [
                {
                    "type": "text",
                    "name": "text-45910",
                    "label": "Name"
                },
                {
                    "type": "text",
                    "name": "text-80103",
                    "label": "First name"
                },
                {
                    "type": "text",
                    "name": "text-75307",
                    "label": "Last name"
                },
                {
                    "type": "text",
                    "name": "text-93543",
                    "label": "Email"
                },
                {
                    "type": "text",
                    "name": "text-16313",
                    "label": "Phone number"
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

    def get_customer_user_type(self, company_type_id: int) -> dict:
        """
        Returns the 'Customer User'-Type for the 'User management'-Profile
        
        Args:
            company_type_id (int): public_id of created 'Company'-Type
        """
        return {
            "name": "customer_user",
            "selectable_as_parent": True,
            "global_template_ids": [],
            "active": True,
            "author_id": 1,
            "creation_time": self.get_current_datetime(),
            "editor_id": None,
            "last_edit_time": None,
            "label": "Customer User",
            "version": "1.0.0",
            "description": None,
            "render_meta": {
                "icon": "fas fa-user-tie",
                "sections": [
                    {
                        "type": "section",
                        "name": "section-82897",
                        "label": "Information",
                        "fields": [
                            "text-39929"
                        ]
                    },
                    {
                        "type": "section",
                        "name": "section-62012",
                        "label": "Personal data",
                        "fields": [
                            "text-91469",
                            "text-84039",
                            "text-27614",
                            "text-44997",
                            "ref-25151"
                        ]
                    }
                ],
                "externals": [],
                "summary": {
                    "fields": [
                    "text-39929",
                    "text-27614",
                    "ref-25151"
                    ]
                }
            },
            "fields": [
            {
                "type": "text",
                "name": "text-39929",
                "label": "Name"
            },
            {
                "type": "text",
                "name": "text-91469",
                "label": "First name"
            },
            {
                "type": "text",
                "name": "text-84039",
                "label": "Last name"
            },
            {
                "type": "text",
                "name": "text-27614",
                "label": "Email"
            },
            {
                "type": "text",
                "name": "text-44997",
                "label": "Phone number"
            },
            {
                "type": "ref",
                "name": "ref-25151",
                "label": "Company",
                "ref_types": [
                    company_type_id
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
