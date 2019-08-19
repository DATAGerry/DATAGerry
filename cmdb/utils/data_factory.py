# dataGerry - OpenSource Enterprise CMDB
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
CMDB data faker environment
NOTE: This module is highly experimental and should only be used for development. It still needs a lot of refactoring.
"""

from cmdb.framework.cmdb_object import CmdbObject
from cmdb.framework.cmdb_type import CmdbType
from cmdb.framework.cmdb_object_category import CmdbCategory
from cmdb.user_management.user_group import UserGroup
from cmdb.user_management.user import User
from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.data_storage import get_pre_init_database
from faker import Faker
import random
import datetime
import logging

LOGGER = logging.getLogger(__name__)
try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception


class DataGenerator:

    def __init__(self, faker: Faker, database_manager: DatabaseManagerMongo):
        self._faker = faker
        self._faker.seed(67776866)  # CMDB
        from cmdb.utils.security import SecurityManager
        self._security_manager = SecurityManager(database_manager)

    def generate_settings(self):
        self._security_manager.generate_sym_key()
        self._security_manager.generate_symmetric_aes_key()
        self._security_manager.generate_key_pair()

    @staticmethod
    def generate_default_groups() -> list:
        return [
            UserGroup(
                **{
                    "label": "Admin", "name": "admin", "public_id": 1,
                    "rights": [
                        "base.system.*",
                        "base.system.security",
                        "base.system.user_management.rst",
                        "base.framework.*",
                        "base.framework.object.view",
                        "base.framework.object.edit",
                        "base.framework.object.delete",
                        "base.framework.type.view",
                        "base.framework.type.edit",
                        "base.framework.type.delete"
                    ]
                }
            ),
            UserGroup(
                **{
                    "label": "User", "name": "user", "public_id": 2,
                    "rights": [
                        "base.framework.object.view",
                        "base.framework.object.edit",
                        "base.framework.object.delete",
                        "base.framework.type.view"
                    ]
                }
            ),
            UserGroup(
                **{
                    "label": "Guest", "name": "guest", "public_id": 3,
                    "rights": [
                        "base.framework.object.view"
                    ]
                }
            ),
            UserGroup(
                **{
                    "label": "Rest", "name": "rest", "public_id": 4,
                    "rights": [
                        "base.framework.*"
                    ]
                }
            )
        ]

    def generate_users(self, group_list, iterations=99) -> list:
        user_list = list()
        user_list.append(
            User(
                public_id=1,
                group_id=1,
                first_name='Mark',
                last_name='Heumueller',
                user_name='admin',
                email='mark.heumueller@nethinks.com',
                registration_time=datetime.datetime.utcnow(),
                authenticator='LocalAuthenticationProvider',
                password=self._security_manager.generate_hmac('admin')
            )
        )
        public_id_counter = 2  # 1 is admin user
        for _ in range(iterations):
            user_list.append(
                User(
                    public_id=public_id_counter,
                    group_id=random.choice(group_list).get_public_id(),
                    first_name=self._faker.first_name(),
                    last_name=self._faker.last_name(),
                    user_name=self._faker.user_name(),
                    email=self._faker.email(),
                    registration_time=self._faker.date_time_between(start_date="-30d"),
                    authenticator='LocalAuthenticationProvider',
                    password=self._security_manager.generate_hmac(self._faker.password())
                )
            )
            public_id_counter = public_id_counter + 1
        return user_list

    def generate_types(self) -> list:
        type_list = list()
        generation_date = self._faker.date_time_between(start_date="-100d", end_date="-30d")

        type_list.append(
            CmdbType(
                **{
                    "public_id": 1,
                    "label": "Leased Lines",
                    "name": "leased_lines",
                    "description": "A leased line is a private bidirectional or symmetric telecommunications circuit "
                                   "between two or more locations provided according to a commercial contract.",
                    "version": "1.0.0",
                    "active": True,
                    "author_id": 1,
                    "creation_time": generation_date,
                    "render_meta": {
                        "external": [
                            {
                                "href": "/{2}/{0}/{1}",
                                "fields": [
                                    "text-1",
                                    "text-2",
                                    "text-3"
                                ],
                                "label": "Internal link",
                                "name": "internal_link",
                                "icon": None
                            }
                        ],
                        "summary": [
                            {
                                "label": "Connection State",
                                "fields": [
                                    "state",
                                ],
                                "name": "connection_state"
                            },
                            {
                                "label": "Linedetails",
                                "fields": [
                                    "product_name",
                                    "transfer_rate"
                                ],
                                "name": "linedetails"
                            },
                            {
                                "label": "Location A",
                                "fields": [
                                    "company_name_a",
                                    "zip_a",
                                    "city_a"
                                ],
                                "name": "location_a"
                            },
                            {
                                "label": "Location B",
                                "fields": [
                                    "company_name_b",
                                    "zip_b",
                                    "city_b"
                                ],
                                "name": "location_b"
                            }
                        ],
                        "sections": [
                            {
                                "tag": "h1",
                                "name": "connection state",
                                "label": "Connection State",
                                "fields": [
                                    "state",
                                ],
                                "position": 1
                            },
                            {
                                "tag": "h2",
                                "name": "linedetails",
                                "label": "Linedetails",
                                "fields": [
                                    "product_name",
                                    "transfer_rate"
                                ],
                                "position": 2
                            },
                            {
                                "tag": "h1",
                                "name": "location_a",
                                "label": "Location A",
                                "fields": [
                                    "company_name_a",
                                    "street_a",
                                    "zip_a",
                                    "city_a",
                                    "location_details_a"
                                ],
                                "position": 3
                            },
                            {
                                "tag": "h1",
                                "name": "location_b",
                                "label": "Location B",
                                "fields": [
                                    "company_name_b",
                                    "street_b",
                                    "zip_b",
                                    "city_b",
                                    "location_details_b"
                                ],
                                "position": 4
                            },
                        ]
                    },
                    "fields": [
                        {
                            "input_type": "checkbox",
                            "label": "State",
                            "name": "state",
                            "className": "form-control",
                            "type": "checkbox"
                        },
                        {
                            "input_type": "text",
                            "label": "Product Name",
                            "className": "form-control",
                            "name": "product_name",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Transfer Rate",
                            "className": "form-control",
                            "name": "transfer_rate",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Company Name A",
                            "className": "form-control",
                            "name": "company_name_a",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Street A",
                            "className": "form-control",
                            "name": "street_a",
                            "type": "text"
                        },
                        {
                            "input_type": "number",
                            "label": "ZIP A",
                            "required": True,
                            "className": "form-control",
                            "name": "zip_a",
                            "min": 10000,
                            "max": 99999,
                            "step": 1,
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "City A",
                            "className": "form-control",
                            "name": "city_a",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Location Details A",
                            "className": "form-control",
                            "name": "location_details_a",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Company Name B",
                            "className": "form-control",
                            "name": "company_name_b",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Street B",
                            "className": "form-control",
                            "name": "street_b",
                            "type": "text"
                        },
                        {
                            "input_type": "number",
                            "label": "ZIP B",
                            "required": True,
                            "className": "form-control",
                            "name": "zip_b",
                            "min": 10000,
                            "max": 99999,
                            "step": 1,
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "City B",
                            "className": "form-control",
                            "name": "city_b",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Location Details B",
                            "className": "form-control",
                            "name": "location_details_b",
                            "type": "text"
                        },

                    ],
                    "logs": [
                        {
                            "author_id": 1,
                            "action": "create",
                            "message": "Auto-generation of example type",
                            "date": generation_date
                        }
                    ]
                }
            )
        )
        type_list.append(
            CmdbType(
                **{
                    "public_id": 2,
                    "title": "Switch",
                    "name": "switch",
                    "description": "A switch (also called switching hub, bridging hub, officially MAC bridge) "
                                   "is a computer networking device that connects devices on a computer network "
                                   "by using packet switching to receive, process, "
                                   "and forward data to the destination device. ",
                    "version": "1.0.0",
                    "active": True,
                    "author_id": 1,
                    "creation_time": generation_date,
                    "render_meta": {
                        "external": [],
                        "summary": [
                            {
                                "label": "Management",
                                "fields": [
                                    "management_ip",
                                    "hostname"
                                ],
                                "name": "management"
                            }
                        ],
                        "sections": [
                            {
                                "tag": "h1",
                                "name": "management",
                                "label": "Management",
                                "fields": [
                                    "management_ip",
                                    "hostname",
                                    "monitoring",
                                    "os",
                                    "username",
                                    "password"
                                ],
                                "position": 1
                            },
                            {
                                "tag": "h1",
                                "name": "location",
                                "label": "Location",
                                "fields": [
                                    "address",
                                    "building",
                                    "room",
                                    "rack",
                                ],
                                "position": 2
                            },
                            {
                                "tag": "h1",
                                "name": "hardware",
                                "label": "Hardware",
                                "fields": [
                                    "manufacturer",
                                    "supplier",
                                    "model",
                                    "serial_number",
                                    "software_version"
                                ],
                                "position": 3
                            }
                        ]
                    },
                    "fields": [
                        {
                            "input_type": "text",
                            "label": "Management IP",
                            "className": "form-control",
                            "name": "management_ip",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Hostname",
                            "className": "form-control",
                            "name": "hostname",
                            "type": "text"
                        },
                        {
                            "input_type": "checkbox",
                            "label": "Monitoring",
                            "className": "form-control",
                            "name": "monitoring",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Operating System",
                            "className": "form-control",
                            "name": "os",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Username",
                            "className": "form-control",
                            "name": "username",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Password",
                            "className": "form-control",
                            "name": "password",
                            "type": "password",
                            "required": True,
                        },
                        {
                            "input_type": "text",
                            "label": "Address",
                            "className": "form-control",
                            "name": "address",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Building",
                            "className": "form-control",
                            "name": "building",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Room",
                            "className": "form-control",
                            "name": "room",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Rack",
                            "className": "form-control",
                            "name": "rack",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Manufacturer",
                            "className": "form-control",
                            "name": "manufacturer",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Supplier",
                            "className": "form-control",
                            "name": "supplier",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Model",
                            "className": "form-control",
                            "name": "model",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Serial Number",
                            "className": "form-control",
                            "name": "serial_number",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Software Version",
                            "className": "form-control",
                            "name": "software_version",
                            "type": "text"
                        },

                    ],
                    "logs": [
                        {
                            "author_id": 1,
                            "action": "create",
                            "message": "Auto-generation of employee type",
                            "date": generation_date
                        }
                    ]
                }
            )
        )

        type_list.append(
            CmdbType(
                **{
                    "public_id": 3,
                    "title": "Router",
                    "name": "router",
                    "description": "A router is a networking device that forwards data packets "
                                   "between computer networks.",
                    "version": "1.0.0",
                    "active": True,
                    "author_id": 1,
                    "creation_time": generation_date,
                    "render_meta": {
                        "external": [],
                        "summary": [
                            {
                                "label": "Management",
                                "fields": [
                                    "management_ip",
                                    "hostname"
                                ],
                                "name": "management"
                            }
                        ],
                        "sections": [
                            {
                                "tag": "h1",
                                "name": "management",
                                "label": "Management",
                                "fields": [
                                    "management_ip",
                                    "hostname",
                                    "monitoring",
                                    "os",
                                    "username",
                                    "password"
                                ],
                                "position": 1
                            },
                            {
                                "tag": "h1",
                                "name": "location",
                                "label": "Location",
                                "fields": [
                                    "address",
                                    "building",
                                    "room",
                                    "rack",
                                ],
                                "position": 2
                            },
                            {
                                "tag": "h1",
                                "name": "hardware",
                                "label": "Hardware",
                                "fields": [
                                    "manufacturer",
                                    "supplier",
                                    "model",
                                    "serial_number",
                                    "software_version"
                                ],
                                "position": 3
                            }
                        ]
                    },
                    "fields": [
                        {
                            "input_type": "text",
                            "label": "Management IP",
                            "className": "form-control",
                            "name": "management_ip",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Hostname",
                            "className": "form-control",
                            "name": "hostname",
                            "type": "text"
                        },
                        {
                            "input_type": "checkbox",
                            "label": "Monitoring",
                            "className": "form-control",
                            "name": "monitoring",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Operating System",
                            "className": "form-control",
                            "name": "os",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Username",
                            "className": "form-control",
                            "name": "username",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Password",
                            "className": "form-control",
                            "name": "password",
                            "type": "password",
                            "required": True,
                        },
                        {
                            "input_type": "text",
                            "label": "Address",
                            "className": "form-control",
                            "name": "address",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Building",
                            "className": "form-control",
                            "name": "building",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Room",
                            "className": "form-control",
                            "name": "room",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Rack",
                            "className": "form-control",
                            "name": "rack",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Manufacturer",
                            "className": "form-control",
                            "name": "manufacturer",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Supplier",
                            "className": "form-control",
                            "name": "supplier",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Model",
                            "className": "form-control",
                            "name": "model",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Serial Number",
                            "className": "form-control",
                            "name": "serial_number",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Software Version",
                            "className": "form-control",
                            "name": "software_version",
                            "type": "text"
                        },

                    ],
                    "logs": [
                        {
                            "author_id": 1,
                            "action": "create",
                            "message": "Auto-generation of departments type",
                            "date": generation_date
                        }
                    ]
                }
            )
        )
        type_list.append(
            CmdbType(
                **{
                    "public_id": 4,
                    "label": "Locations",
                    "name": "locations",
                    "description": "Company building and locations",
                    "version": "1.0.0",
                    "active": True,
                    "author_id": 1,
                    "creation_time": generation_date,
                    "render_meta": {
                        "external": [
                            {
                                "href": "/{2}/{0}/{1}",
                                "fields": [
                                    "map-lang",
                                    "map-long"
                                ],
                                "label": "Google Maps",
                                "name": "g_maps",
                                "icon": "fas fa-map-marked-alt"
                            }
                        ],
                        "summary": [
                            {
                                "label": "Address",
                                "fields": [
                                    "street",
                                    "city"
                                ],
                                "name": "address"
                            }
                        ],
                        "sections": [
                            {
                                "tag": "h1",
                                "name": "location_details",
                                "label": "Location-Details",
                                "fields": [
                                    "naming",
                                    "description",
                                    "entrance",
                                    "person_in_charge"
                                ],
                                "position": 1
                            },
                            {
                                "tag": "h2",
                                "name": "address",
                                "label": "Address",
                                "fields": [
                                    "street",
                                    "zip",
                                    "city",
                                    "map-lang",
                                    "map-long"
                                ],
                                "position": 2
                            }
                        ]
                    },
                    "fields": [
                        {
                            "input_type": "text",
                            "required": True,
                            "label": "Naming",
                            "description": "Short name of the location",
                            "placeholder": "Calling name",
                            "className": "form-control",
                            "name": "naming",
                            "type": "text"
                        },
                        {
                            "input_type": "textarea",
                            "label": "Description",
                            "className": "form-control",
                            "name": "description",
                            "type": "textarea",
                            "maxlength": 120,
                            "rows": 3
                        },
                        {
                            "input_type": "text",
                            "label": "Entrance",
                            "className": "form-control",
                            "name": "entrance",
                            "type": "text"
                        },
                        {
                            "input_type": "ref",
                            "label": "Person in Charge",
                            "className": "form-control",
                            "name": "person_in_charge",
                            "type": "text",
                            "type_id": 2
                        },
                        {
                            "input_type": "text",
                            "label": "Street",
                            "className": "form-control",
                            "name": "street",
                            "type": "text"
                        },
                        {
                            "input_type": "number",
                            "label": "ZIP",
                            "required": True,
                            "className": "form-control",
                            "name": "zip",
                            "min": 10000,
                            "max": 99999,
                            "step": 1,
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Entrance",
                            "className": "form-control",
                            "name": "city",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Latitude",
                            "required": True,
                            "className": "form-control",
                            "name": "map-lang",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Longitude",
                            "required": True,
                            "className": "form-control",
                            "name": "map-long",
                            "type": "text"
                        }
                    ],
                    "logs": [
                        {
                            "author_id": 1,
                            "action": "create",
                            "message": "Auto-generation",
                            "date": generation_date
                        }
                    ]
                }
            )
        )
        type_list.append(
            CmdbType(
                **{
                    "public_id": 5,
                    "label": "Servers",
                    "name": "servers",
                    "description": "Server connections and hostname",
                    "version": "1.0.0",
                    "active": True,
                    "author_id": 1,
                    "creation_time": generation_date,
                    "render_meta": {
                        "external": [
                            {
                                "href": "ssh:/{0}/",
                                "fields": [
                                    "ipv4"
                                ],
                                "label": "SSH",
                                "name": "ssh",
                                "icon": "fas fa-ethernet"
                            }
                        ],
                        "summary": [
                            {
                                "label": "Name",
                                "fields": [
                                    "hostname"
                                ],
                                "name": "hostname"
                            }
                        ],
                        "sections": [
                            {
                                "tag": "h1",
                                "name": "management",
                                "label": "Management",
                                "fields": [
                                    "hostname",
                                    "ipv4",
                                    "ipv4_network_class",
                                    "ipv4_intranet",
                                    "ipv6",
                                ],
                                "position": 1
                            }
                        ]
                    },
                    "fields": [
                        {
                            "input_type": "text",
                            "required": True,
                            "label": "Hostname",
                            "className": "form-control",
                            "name": "hostname",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "required": True,
                            "label": "IPv4 Public",
                            "placeholder": "127.0.0.1",
                            "className": "form-control",
                            "name": "ipv4",
                            "type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "IPv4 Network Class",
                            "placeholder": "A",
                            "className": "form-control",
                            "name": "ipv4_network_class",
                            "description": "An IPv4 address class is a categorical division of internet protocol "
                                           "addresses in IPv4-based routing",
                            "type": "text"
                        }, {
                            "input_type": "text",
                            "label": "IPv4 Private",
                            "placeholder": "127.0.0.1",
                            "className": "form-control",
                            "name": "ipv4_intranet",
                            "type": "text"
                        }, {
                            "input_type": "text",
                            "label": "IPv6",
                            "placeholder": "[2001:0db8:85a3:08d3::0370:7344]",
                            "className": "form-control",
                            "name": "ipv6",
                            "type": "text"
                        }
                    ],
                    "logs": [
                        {
                            "author_id": 1,
                            "action": "create",
                            "message": "Auto-generation",
                            "date": generation_date
                        }
                    ]
                }
            )
        )

        return type_list

    def generate_objects(self, type_list, user_list, num_objects=1000) -> list:
        public_id_counter = 1

        example_object_list = list()
        employee_list = list()
        department_list = list()
        location_list = list()
        servers_list = list()

        def gen_leased_line_object():
            try:
                location_id_a = random.choice(location_list).get_public_id()
                location_id_b = random.choice(location_list).get_public_id()
            except Exception:
                location_id_a = None
                location_id_b = None
            return CmdbObject(
                **{
                    "public_id": public_id_counter,
                    "author_id": random.choice(user_list).get_public_id(),
                    "type_id": 1,
                    "views": self._faker.random_number(4),
                    "version": "1.0.0",
                    "last_edit_time": self._faker.date_time_between(start_date="-30d"),
                    "active": self._faker.boolean(chance_of_getting_true=80),
                    "creation_time": self._faker.date_time_between(start_date="-30d"),
                    "status": None,
                    "logs": [

                    ],
                    "fields": [
                        {
                            "name": "state",
                            "value": self._faker.boolean()
                        },
                        {
                            "name": "product_name",
                            "value": self._faker.last_name() + " " + self._faker.company_suffix()
                        },
                        {
                            "name": "transfer_rate",
                            "value": str(self._faker.random_int(max=1000)) + " Mbit/s"
                        },
                        {
                            "name": "company_name_a",
                            "value": self._faker.first_name() + " " + self._faker.company_suffix()
                        },
                        {
                            "name": "street_a",
                            "value": self._faker.street_name()
                        },
                        {
                            "name": "zip_a",
                            "value": self._faker.zipcode()
                        },
                        {
                            "name": "city_a",
                            "value": self._faker.city()
                        },
                        {
                            "name": "location_details_a",
                            "value": location_id_a
                        },
                        {
                            "name": "company_name_b",
                            "value": self._faker.first_name() + " " + self._faker.company_suffix()
                        },
                        {
                            "name": "street_b",
                            "value": self._faker.street_name()
                        },
                        {
                            "name": "zip_b",
                            "value": self._faker.zipcode()
                        },
                        {
                            "name": "city_b",
                            "value": self._faker.city()
                        },
                        {
                            "name": "location_details_b",
                            "value": location_id_b
                        }

                    ]
                }
            )

        def gen_switch_object():
            try:
                location = random.choice(location_list).get_public_id()
            except Exception:
                location = None
            return CmdbObject(
                **{
                    "public_id": public_id_counter,
                    "author_id": random.choice(user_list).get_public_id(),
                    "type_id": 2,
                    "views": self._faker.random_number(4),
                    "version": "1.0.0",
                    "last_edit_time": self._faker.date_time_between(start_date="-30d"),
                    "active": self._faker.boolean(chance_of_getting_true=80),
                    "creation_time": self._faker.date_time_between(start_date="-30d"),
                    "status": None,
                    "logs": [

                    ],
                    "fields": [
                        {
                            "name": "management_ip",
                            "value": self._faker.ipv4()
                        },
                        {
                            "name": "hostname",
                            "value": self._faker.hostname()
                        },
                        {
                            "name": "monitoring",
                            "value": self._faker.boolean()
                        },
                        {
                            "name": "os",
                            "value": self._faker.word()
                        },
                        {
                            "name": "username",
                            "value": self._faker.user_name()
                        },
                        {
                            "name": "password",
                            "value": self._security_manager.encrypt_aes(self._faker.password())
                        },
                        {
                            "name": "address",
                            "value": location
                        },
                        {
                            "name": "building",
                            "value": self._faker.word()
                        },
                        {
                            "name": "room",
                            "value": self._faker.word()
                        },
                        {
                            "name": "rack",
                            "value": self._faker.word()
                        },
                        {
                            "name": "manufacturer",
                            "value": self._faker.first_name() + self._faker.company_suffix()
                        },
                        {
                            "name": "supplier",
                            "value": self._faker.last_name() + self._faker.company_suffix()
                        },
                        {
                            "name": "model",
                            "value": self._faker.word()
                        },
                        {
                            "name": "serial_number",
                            "value": self._faker.random_number()
                        },
                        {
                            "name": "software_version",
                            "value": self._faker.random_number()
                        },
                    ]
                }
            )

        def gen_router_object():
            try:
                location = random.choice(location_list).get_public_id()
            except Exception:
                location = None
            return CmdbObject(
                **{
                    "public_id": public_id_counter,
                    "author_id": random.choice(user_list).get_public_id(),
                    "type_id": 3,
                    "views": self._faker.random_number(4),
                    "version": "1.0.0",
                    "last_edit_time": self._faker.date_time_between(start_date="-30d"),
                    "active": self._faker.boolean(chance_of_getting_true=80),
                    "creation_time": self._faker.date_time_between(start_date="-30d"),
                    "status": None,
                    "logs": [

                    ],
                    "fields": [
                        {
                            "name": "management_ip",
                            "value": self._faker.ipv4()
                        },
                        {
                            "name": "hostname",
                            "value": self._faker.hostname()
                        },
                        {
                            "name": "monitoring",
                            "value": self._faker.boolean()
                        },
                        {
                            "name": "os",
                            "value": self._faker.word()
                        },
                        {
                            "name": "username",
                            "value": self._faker.user_name()
                        },
                        {
                            "name": "password",
                            "value": self._security_manager.encrypt_aes(self._faker.password())
                        },
                        {
                            "name": "address",
                            "value": location
                        },
                        {
                            "name": "building",
                            "value": self._faker.word()
                        },
                        {
                            "name": "room",
                            "value": self._faker.word()
                        },
                        {
                            "name": "rack",
                            "value": self._faker.word()
                        },
                        {
                            "name": "manufacturer",
                            "value": self._faker.first_name() + self._faker.company_suffix()
                        },
                        {
                            "name": "supplier",
                            "value": self._faker.last_name() + self._faker.company_suffix()
                        },
                        {
                            "name": "model",
                            "value": self._faker.word()
                        },
                        {
                            "name": "serial_number",
                            "value": self._faker.random_number()
                        },
                        {
                            "name": "software_version",
                            "value": self._faker.random_number()
                        },
                    ]
                }
            )

        def gen_location_object():
            try:
                employee_id = random.choice(employee_list).get_public_id()
            except Exception:
                employee_id = None
            return CmdbObject(
                **{
                    "public_id": public_id_counter,
                    "author_id": random.choice(user_list).get_public_id(),
                    "type_id": 4,
                    "views": self._faker.random_number(4),
                    "version": "1.0.0",
                    "last_edit_time": self._faker.date_time_between(start_date="-30d"),
                    "active": self._faker.boolean(chance_of_getting_true=80),
                    "creation_time": self._faker.date_time_between(start_date="-30d"),
                    "status": None,
                    "logs": [

                    ],
                    "fields": [
                        {
                            "name": "naming",
                            "value": self._faker.suffix()
                        },
                        {
                            "name": "description",
                            "value": self._faker.paragraph()
                        },
                        {
                            "name": "entrance",
                            "value": self._faker.paragraph()
                        },
                        {
                            "name": "person_in_charge",
                            "value": employee_id
                        },
                        {
                            "name": "street",
                            "value": self._faker.street_name()
                        },
                        {
                            "name": "zip",
                            "value": self._faker.zipcode()
                        },
                        {
                            "name": "city",
                            "value": self._faker.city()
                        },
                        {
                            "name": "map-lang",
                            "value": str(self._faker.latitude())
                        },
                        {
                            "name": "map-long",
                            "value": str(self._faker.longitude())
                        },
                    ]
                }
            )

        def gen_server_object():
            return CmdbObject(
                **{
                    "public_id": public_id_counter,
                    "author_id": random.choice(user_list).get_public_id(),
                    "type_id": 5,
                    "views": self._faker.random_number(4),
                    "version": "1.0.0",
                    "last_edit_time": self._faker.date_time_between(start_date="-30d"),
                    "active": self._faker.boolean(chance_of_getting_true=80),
                    "creation_time": self._faker.date_time_between(start_date="-30d"),
                    "status": None,
                    "logs": [

                    ],
                    "fields": [
                        {
                            "name": "hostname",
                            "value": self._faker.hostname()
                        },
                        {
                            "name": "ipv4",
                            "value": self._faker.ipv4()
                        },
                        {
                            "name": "ipv4_network_class",
                            "value": self._faker.ipv4_network_class()
                        },
                        {
                            "name": "ipv4_intranet",
                            "value": self._faker.ipv4_private()
                        },
                        {
                            "name": "ipv6",
                            "value": self._faker.ipv6()
                        }
                    ]
                }
            )

        def select(type_id: int):
            if type_id == 1:
                example_object_list.append(gen_leased_line_object())
            elif type_id == 2:
                employee_list.append(gen_switch_object())
            elif type_id == 3:
                department_list.append(gen_router_object()),
            elif type_id == 4:
                location_list.append(gen_location_object()),
            elif type_id == 5:
                servers_list.append(gen_server_object()),

        for _ in range(num_objects):
            select(random.choice(type_list).get_public_id())
            public_id_counter = public_id_counter + 1

        object_list = example_object_list + employee_list + department_list + location_list + servers_list
        return object_list


    @staticmethod
    def generate_categories() -> list:
        category_list = [
            CmdbCategory(**{
                "public_id": 1,
                "name": "infrastructure",
                "label": "Infrastructure",
                # "parent_id": 2,
                "type_list": [
                    1,
                    4
                ]
            }),
            CmdbCategory(**{
                "public_id": 2,
                "name": "devices",
                "label": "Devices",
                "icon": "fas fa-memory",
                # "parent_id": 3,
                "type_list": [
                    2,
                    3,
                    5
                ]
            }),
        ]
        return category_list


class DataFactory:

    def __init__(self, database_manager: DatabaseManagerMongo = None, auto: bool = True):
        self._database_manager = database_manager or get_pre_init_database()
        self._data_generator = DataGenerator(Faker(), database_manager)
        self._auto_generate = auto
        if self._auto_generate:
            self._database_manager.drop(self._database_manager.get_database_name())  # cleanup database
            self._data_generator.generate_settings()
        self.groups = self._data_generator.generate_default_groups()
        self.users = self._data_generator.generate_users(group_list=self.groups)
        self.types = self._data_generator.generate_types()
        self.objects = self._data_generator.generate_objects(type_list=self.types, user_list=self.users, num_objects=1000)
        self.categories = self._data_generator.generate_categories()

    class __FakerWrapper:
        """Schema wrapper for fake data generator - TODO"""

        def __init__(self, faker=None, locale=None, providers=None, includes=None):
            self._faker = faker or Faker(locale=locale, providers=providers, includes=includes)

        def generate_fake(self, schema: dict, iterations: int = 1) -> (list, dict):
            """
            generate fake data dict based on schema
            Args:
                schema: dict of faker functions
                iterations: number of objects to create

            Returns:
                dict or list of fake data
            """
            result = [self._generate_one_fake(schema) for _ in range(iterations)]
            return result[0] if len(result) == 1 else result

        def _generate_one_fake(self, schema) -> (list, dict):
            """
            faker caller function based on schema items
            Args:
                schema: dict of faker functions with parameters

            Returns:
                dict or list of fake data
            """
            data = {}
            for k, v in schema.items():
                if isinstance(v, dict):
                    data[k] = self._generate_one_fake(v)
                elif isinstance(v, list):
                    data[k] = [self._generate_one_fake(item) for item in v]
                elif isinstance(v, str) and hasattr(self._faker, v):
                    data[k] = getattr(self._faker, v)()
                else:
                    data[k] = getattr(self._faker, v)()
            return data

    def insert_data(self) -> list:
        """insert data into database"""
        if self._database_manager is None:
            raise NoDatabaseManagerError()
        from cmdb.framework.cmdb_object_manager import CmdbObjectManager
        from cmdb.user_management.user_manager import UserManagement
        from cmdb.utils.security import SecurityManager

        obm = CmdbObjectManager(database_manager=self._database_manager)
        usm = UserManagement(database_manager=self._database_manager,
                             security_manager=SecurityManager(self._database_manager))

        error = []
        for group_element in self.groups:
            try:
                usm.insert_group(group_element)
            except CMDBError as e:
                error.append(e.message)
                continue
        for user_element in self.users:
            try:
                usm.insert_user(user_element)
            except CMDBError as e:
                error.append(e.message)
                continue
        for type_element in self.types:
            try:
                obm.insert_type(type_element)
            except CMDBError as e:
                error.append(e.message)
                continue
        for category_element in self.categories:
            try:
                obm.insert_category(category_element)
            except CMDBError as e:
                error.append(e.message)
                continue

        for object_element in self.objects:
            try:
                obm.insert_object(object_element)
            except CMDBError as e:
                error.append(e.message)
                continue

        return error


class NoDatabaseManagerError(CMDBError):
    """Error if field could not be initialized"""

    def __init__(self):
        super().__init__()
        self.message = 'Database manager was not passed.'
