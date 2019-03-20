"""
CMDB data faker environment
NOTE: This module is highly experimental and should only be used for development. It still needs a lot of refactoring.
"""

from cmdb.object_framework.cmdb_object import CmdbObject
from cmdb.object_framework.cmdb_object_type import CmdbType
from cmdb.object_framework.cmdb_object_category import CmdbTypeCategory
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
                    "label": "Example",
                    "name": "example",
                    "description": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, \
                         sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. \
                         At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata\
                         sanctus est Lorem ipsum dolor sit amet.",
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
                                "label": "Summary",
                                "fields": [
                                    "text-1",
                                    "text-2",
                                    "textarea-1"
                                ],
                                "name": "example_summary"
                            },
                            {
                                "label": "Date",
                                "fields": [
                                    "date-1"
                                ],
                                "name": "example_date"
                            }
                        ],
                        "sections": [
                            {
                                "tag": "h1",
                                "name": "text_fields",
                                "label": "Text Fields",
                                "fields": [
                                    "text-1",
                                    "text-2"
                                ],
                                "position": 1
                            },
                            {
                                "tag": "h2",
                                "name": "text_fields_special",
                                "label": "Special Fields",
                                "fields": [
                                    "password-1",
                                    "textarea-1"
                                ],
                                "position": 2
                            },
                            {
                                "tag": "h1",
                                "name": "check_fields",
                                "label": "Check Fields",
                                "fields": [
                                    "radio-group-1",
                                    "checkbox-group-1",
                                    "select-1",
                                    "select-2"
                                ],
                                "position": 3
                            },
                            {
                                "tag": "h1",
                                "name": "other_fields",
                                "label": "Other Fields",
                                "fields": [
                                    "date-1",
                                    "number-1",
                                    "number-2",
                                    "text-3"
                                ],
                                "position": 4
                            }
                        ]
                    },
                    "fields": [
                        {
                            "input_type": "text",
                            "label": "Basic Text Field",
                            "className": "form-control",
                            "name": "text-1",
                            "subtype": "text"
                        },
                        {
                            "input_type": "text",
                            "required": True,
                            "label": "Full Text Field",
                            "description": "example text field with all possible options",
                            "placeholder": "example",
                            "className": "form-control",
                            "name": "text-2",
                            "access": True,
                            "subtype": "text",
                            "maxlength": 120,
                            "role": 1
                        },
                        {
                            "input_type": "text",
                            "subtype": "password",
                            "required": True,
                            "label": "Password Field",
                            "className": "form-control",
                            "name": "password-1"
                        },
                        {
                            "input_type": "textarea",
                            "label": "Basic Text Area",
                            "className": "form-control",
                            "name": "textarea-1",
                            "subtype": "textarea",
                            "maxlength": 120,
                            "rows": 3
                        },
                        {
                            "input_type": "radio-group",
                            "label": "Basic Radio Group",
                            "name": "radio-group-1",
                            "values": [
                                {
                                    "label": "Option 1",
                                    "value": "option-1"
                                },
                                {
                                    "label": "Option 2",
                                    "value": "option-2"
                                },
                                {
                                    "label": "Option 3",
                                    "value": "option-3"
                                }
                            ]
                        },
                        {
                            "input_type": "checkbox-group",
                            "label": "Basic Checkbox Group",
                            "name": "checkbox-group-1",
                            "values": [
                                {
                                    "label": "Option 1",
                                    "value": "option-1",
                                    "selected": True
                                },
                                {
                                    "label": "Option 2",
                                    "value": "option-2"
                                }
                            ]
                        },
                        {
                            "input_type": "select",
                            "label": "Basic Select",
                            "className": "form-control",
                            "name": "select-1",
                            "values": [
                                {
                                    "label": "Option 1",
                                    "value": "option-1",
                                    "selected": True
                                },
                                {
                                    "label": "Option 2",
                                    "value": "option-2"
                                },
                                {
                                    "label": "Option 3",
                                    "value": "option-3"
                                }
                            ]
                        },
                        {
                            "input_type": "select",
                            "label": "Multi Select",
                            "className": "form-control",
                            "name": "select-2",
                            "multiple": True,
                            "values": [
                                {
                                    "label": "Option 1",
                                    "value": "option-1"
                                },
                                {
                                    "label": "Option 2",
                                    "value": "option-2"
                                },
                                {
                                    "label": "Option 3",
                                    "value": "option-3"
                                }
                            ]
                        },
                        {
                            "input_type": "date",
                            "label": "Basic Date Field",
                            "className": "form-control",
                            "name": "date-1"
                        },
                        {
                            "input_type": "number",
                            "label": "Basic Number",
                            "className": "form-control",
                            "name": "number-1"
                        },
                        {
                            "input_type": "number",
                            "label": "Limited Number",
                            "className": "form-control",
                            "name": "number-2",
                            "min": 10,
                            "max": 100,
                            "step": 10
                        },
                        {
                            "input_type": "text",
                            "label": "N - Text Field",
                            "n-field": True,
                            "className": "form-control",
                            "name": "text-3",
                            "subtype": "text"
                        }
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
                    "title": "Employees",
                    "name": "employees",
                    "description": "Company employees",
                    "version": "1.0.0",
                    "active": True,
                    "author_id": 1,
                    "creation_time": generation_date,
                    "render_meta": {
                        "external": [
                            {
                                "href": "https://www.xing.com/profile/{0}",
                                "icon": "fab fa-xing",
                                "fields": [
                                    "xing"
                                ],
                                "name": "xing",
                                "label": "XING"
                            }
                        ],
                        "summary": [
                            {
                                "label": "Name",
                                "fields": [
                                    "first_name",
                                    "last_name"
                                ],
                                "name": "name"
                            },
                            {
                                "label": "Job",
                                "fields": [
                                    "job"
                                ],
                                "name": "job"
                            }
                        ],
                        "sections": [
                            {
                                "tag": "h1",
                                "name": "employee_details",
                                "label": "Employee Details",
                                "fields": [
                                    "employee_number",
                                    "first_name",
                                    "last_name",
                                    "department",
                                    "job"
                                ],
                                "position": 1
                            },
                            {
                                "tag": "h2",
                                "name": "personal_details",
                                "label": "Personal Details",
                                "fields": [
                                    "address",
                                    "birthday"
                                ],
                                "position": 2
                            },
                            {
                                "tag": "h1",
                                "name": "account_data",
                                "label": "Account Data",
                                "fields": [
                                    "user_name",
                                    "email_address",
                                    "cmdb_user"
                                ],
                                "position": 3
                            },
                            {
                                "tag": "h2",
                                "name": "external_accounts",
                                "label": "External Accounts",
                                "fields": [
                                    "xing",
                                    "linked_in",
                                    "website"
                                ],
                                "position": 4
                            }
                        ]
                    },
                    "fields": [
                        {
                            "input_type": "text",
                            "required": True,
                            "label": "Employee Number",
                            "className": "form-control",
                            "name": "employee_number",
                            "access": True,
                            "subinput_type": "text",
                            "maxlength": "4",
                            "role": "1"
                        },
                        {
                            "input_type": "text",
                            "label": "Firstname",
                            "className": "form-control",
                            "name": "first_name",
                            "subinput_type": "text"
                        }, {
                            "input_type": "text",
                            "label": "Job",
                            "className": "form-control",
                            "name": "job",
                            "subinput_type": "text"
                        },
                        {
                            "input_type": "text",
                            "required": True,
                            "label": "Lastname",
                            "className": "form-control",
                            "name": "last_name",
                            "subinput_type": "text"
                        },
                        {
                            "input_type": "ref",
                            "label": "Department",
                            "className": "form-control",
                            "name": "department",
                            "type_id": 3
                        },
                        {
                            "input_type": "text",
                            "label": "Address",
                            "className": "form-control",
                            "name": "address",
                            "subinput_type": "text"
                        },
                        {
                            "input_type": "date",
                            "label": "Birthday",
                            "className": "form-control",
                            "name": "birthday"
                        },
                        {
                            "input_type": "text",
                            "required": True,
                            "label": "Username",
                            "className": "form-control",
                            "name": "user_name",
                            "subinput_type": "text"
                        },
                        {
                            "input_type": "text",
                            "subinput_type": "email",
                            "required": True,
                            "label": "Email Adress",
                            "placeholder": "example@example.org",
                            "className": "form-control",
                            "name": "email_address"
                        },
                        {
                            "input_type": "text",
                            "label": "XING Name",
                            "description": "Profile name inside https://www.xing.com/profile/<br>USERNAME</br>/",
                            "className": "form-control",
                            "name": "xing",
                            "subinput_type": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Linked In",
                            "className": "form-control",
                            "name": "linked_in",
                            "subinput_type": "text"
                        },
                        {
                            "input_type": "href",
                            "label": "Website",
                            "className": "form-control",
                            "name": "website"
                        }
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
                    "title": "Departments",
                    "name": "departments",
                    "description": "Company departments",
                    "version": "1.0.0",
                    "active": True,
                    "author_id": 1,
                    "creation_time": generation_date,
                    "render_meta": {
                        "external": [],
                        "summary": [
                            {
                                "label": "Name",
                                "fields": [
                                    "name"
                                ],
                                "name": "name"
                            }
                        ],
                        "sections": [
                            {
                                "tag": "h1",
                                "name": "informations",
                                "label": "Informations of department",
                                "fields": [
                                    "name",
                                    "department_head"
                                ],
                                "position": 1
                            }
                        ]
                    },
                    "fields": [
                        {
                            "input_type": "text",
                            "label": "Name",
                            "className": "form-control",
                            "name": "name",
                            "subinput_type": "text"
                        },
                        {
                            "input_type": "ref",
                            "label": "Head of department",
                            "className": "form-control",
                            "name": "department_head",
                            "type_id": 2
                        }
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
                            "subtype": "text"
                        },
                        {
                            "input_type": "textarea",
                            "label": "Description",
                            "className": "form-control",
                            "name": "description",
                            "subtype": "textarea",
                            "maxlength": 120,
                            "rows": 3
                        },
                        {
                            "input_type": "text",
                            "label": "Entrance",
                            "className": "form-control",
                            "name": "entrance",
                            "subtype": "text"
                        },
                        {
                            "input_type": "ref",
                            "label": "Person in Charge",
                            "className": "form-control",
                            "name": "person_in_charge",
                            "type_id": 2
                        },
                        {
                            "input_type": "text",
                            "label": "Street",
                            "className": "form-control",
                            "name": "street",
                            "subtype": "text"
                        },
                        {
                            "input_type": "number",
                            "label": "ZIP",
                            "required": True,
                            "className": "form-control",
                            "name": "zip",
                            "min": 10000,
                            "max": 99999,
                            "step": 1
                        },
                        {
                            "input_type": "text",
                            "label": "Entrance",
                            "className": "form-control",
                            "name": "city",
                            "subtype": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Latitude",
                            "required": True,
                            "className": "form-control",
                            "name": "map-lang",
                            "subtype": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "Longitude",
                            "required": True,
                            "className": "form-control",
                            "name": "map-long",
                            "subtype": "text"
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
                            "subtype": "text"
                        },
                        {
                            "input_type": "text",
                            "required": True,
                            "label": "IPv4 Public",
                            "placeholder": "127.0.0.1",
                            "className": "form-control",
                            "name": "ipv4",
                            "subtype": "text"
                        },
                        {
                            "input_type": "text",
                            "label": "IPv4 Network Class",
                            "placeholder": "A",
                            "className": "form-control",
                            "name": "ipv4_network_class",
                            "description": "An IPv4 address class is a categorical division of internet protocol "
                                           "addresses in IPv4-based routing",
                            "subtype": "text"
                        }, {
                            "input_type": "text",
                            "label": "IPv4 Private",
                            "placeholder": "127.0.0.1",
                            "className": "form-control",
                            "name": "ipv4_intranet",
                            "subtype": "text"
                        }, {
                            "input_type": "text",
                            "label": "IPv6",
                            "placeholder": "[2001:0db8:85a3:08d3::0370:7344]",
                            "className": "form-control",
                            "name": "ipv6",
                            "subtype": "text"
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

        def gen_example_object():
            return CmdbObject(
                **{
                    "public_id": public_id_counter,
                    "author_id": random.choice(user_list).get_public_id(),
                    "type_id": 1,
                    "views": self._faker.random_number(4),
                    "version": "1.0.0",
                    "last_edit_time": None,
                    "active": self._faker.boolean(chance_of_getting_true=80),
                    "creation_time": self._faker.date_time_between(start_date="-30d"),
                    "status": None,
                    "logs": [

                    ],
                    "fields": [
                        {
                            "name": "text-1",
                            "value": self._faker.word()
                        },
                        {
                            "name": "text-2",
                            "value": self._faker.words()
                        },
                        {
                            "name": "password-1",
                            "value": self._security_manager.encrypt_aes(self._faker.password())
                        },
                        {
                            "name": "textarea-1",
                            "value": self._faker.paragraph()
                        },
                        {
                            "name": "radio-group-1",
                            "value": random.randint(1, 3)
                        },
                        {
                            "name": "checkbox-group-1",
                            "value": random.randint(1, 3)
                        },
                        {
                            "name": "select-1",
                            "value": random.randint(1, 3)
                        },
                        {
                            "name": "select-2",
                            "value": random.randint(1, 3)
                        },
                        {
                            "name": "date-1",
                            "value": self._faker.date_time_between(start_date="-30d")
                        },
                        {
                            "name": "number-1",
                            "value": random.randint(1, 99)
                        },
                        {
                            "name": "number-2",
                            "value": random.randint(1, 99)
                        },
                        {
                            "name": "text-3",
                            "value": self._faker.text()
                        }
                    ]
                }
            )

        def gen_employee_object():
            try:
                department_id = random.choice(department_list).get_public_id()
            except Exception:
                department_id = None
            return CmdbObject(
                **{
                    "public_id": public_id_counter,
                    "author_id": random.choice(user_list).get_public_id(),
                    "type_id": 2,
                    "views": self._faker.random_number(4),
                    "version": "1.0.0",
                    "last_edit_time": None,
                    "active": self._faker.boolean(chance_of_getting_true=80),
                    "creation_time": self._faker.date_time_between(start_date="-30d"),
                    "status": None,
                    "logs": [

                    ],
                    "fields": [
                        {
                            "name": "employee_number",
                            "value": self._faker.itin()
                        },
                        {
                            "name": "first_name",
                            "value": self._faker.first_name()
                        },
                        {
                            "name": "last_name",
                            "value": self._faker.last_name()
                        },
                        {
                            "name": "department",
                            "value": department_id
                        },
                        {
                            "name": "job",
                            "value": self._faker.job()
                        },
                        {
                            "name": "address",
                            "value": self._faker.address()
                        },
                        {
                            "name": "birthday",
                            "value": self._faker.past_datetime(start_date="-50y")
                        },
                        {
                            "name": "user_name",
                            "value": self._faker.user_name()
                        },
                        {
                            "name": "email_address",
                            "value": self._faker.email()
                        },
                        {
                            "name": "xing",
                            "value": self._faker.user_name()
                        },
                        {
                            "name": "linked_in",
                            "value": self._faker.user_name()
                        },
                        {
                            "name": "website",
                            "value": self._faker.url()
                        }
                    ]
                }
            )

        def gen_department_object():
            try:
                employee_id = random.choice(employee_list).get_public_id()
            except Exception:
                employee_id = None
            return CmdbObject(
                **{
                    "public_id": public_id_counter,
                    "author_id": random.choice(user_list).get_public_id(),
                    "type_id": 3,
                    "views": self._faker.random_number(4),
                    "version": "1.0.0",
                    "last_edit_time": None,
                    "active": self._faker.boolean(chance_of_getting_true=80),
                    "creation_time": self._faker.date_time_between(start_date="-30d"),
                    "status": None,
                    "logs": [

                    ],
                    "fields": [
                        {
                            "name": "name",
                            "value": self._faker.company_suffix()
                        },
                        {
                            "name": "department_head",
                            "value": employee_id
                        }
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
                    "last_edit_time": None,
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
                    "last_edit_time": None,
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
                example_object_list.append(gen_example_object())
            elif type_id == 2:
                employee_list.append(gen_employee_object())
            elif type_id == 3:
                department_list.append(gen_department_object()),
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
            CmdbTypeCategory(**{
                "public_id": 1,
                "name": "example_category",
                "label": "Example",
                "icon": "fas fa-book",
                "type_list": [
                    1
                ]
            }),
            CmdbTypeCategory(**{
                "public_id": 2,
                "name": "company",
                "label": "Company",
                "icon": "fas fa-building",
                "type_list": [
                    2,
                    3
                ]
            }),
            CmdbTypeCategory(**{
                "public_id": 3,
                "name": "infrastructure",
                "label": "Infrastructure",
                "parent_id": 2,
                "type_list": [
                    4
                ]
            }),
            CmdbTypeCategory(**{
                "public_id": 4,
                "name": "hardware",
                "icon": "fas fa-memory",
                "parent_id": 3,
                "type_list": [
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
        from cmdb.object_framework.cmdb_object_manager import CmdbObjectManager
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
