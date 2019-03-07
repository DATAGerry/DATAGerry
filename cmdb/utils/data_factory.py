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
from faker import Faker
from jwcrypto import jwk
import random
import datetime
import base64
import logging

LOGGER = logging.getLogger(__name__)
try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception


class DataFactory:

    def __init__(self, faker: Faker = None, auto_generate: bool = True,
                 database_manager: DatabaseManagerMongo = None, num_of_objects=100):
        self._faker = faker or Faker()
        self._fake_date = self._faker.date_time_between(start_date="-30d")
        self.database_manager = database_manager
        if auto_generate:
            self.settings_conf = self.generate_settings()
            self.user_group_list = DataFactory.generate_default_groups()
            self.user_list = self.generate_users()
            self.type_list = self.generate_types()
            self.category_list = self.generate_categories()
            self.object_list = self.generate_objects(num_of_objects)

    def insert_data(self) -> list:
        """insert data into database"""
        if self.database_manager is None:
            raise NoDatabaseManagerError()
        from cmdb.utils.system_writer import SystemSettingsWriter
        from cmdb.object_framework.cmdb_object_manager import CmdbObjectManager
        from cmdb.user_management.user_manager import UserManagement
        from cmdb.utils.security import SecurityManager

        ssr = SystemSettingsWriter(database_manager=self.database_manager)
        obm = CmdbObjectManager(database_manager=self.database_manager)
        usm = UserManagement(database_manager=self.database_manager,
                             security_manager=SecurityManager(self.database_manager))

        error = []
        for data in self.settings_conf:
            try:
                ssr.write(data['_id'], data)
            except CMDBError as e:
                error.append(e.message)
                continue
        for group_element in self.user_group_list:
            try:
                usm.insert_group(group_element)
            except CMDBError as e:
                error.append(e.message)
                continue
        for user_element in self.user_list:
            try:
                usm.insert_user(user_element)
            except CMDBError as e:
                error.append(e.message)
                continue
        for type_element in self.type_list:
            try:
                obm.insert_type(type_element)
            except CMDBError as e:
                error.append(e.message)
                continue
        for category_element in self.category_list:
            try:
                obm.insert_category(category_element)
            except CMDBError as e:
                error.append(e.message)
                continue
        for object_element in self.object_list:
            try:
                obm.insert_object(object_element)
            except CMDBError as e:
                error.append(e.message)
                continue

        return error

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

    def _generate_hmac(self, data) -> str:
        """generate hash - used for password hashing"""
        import hashlib
        import hmac
        generated_hash = hmac.new(
            bytes(jwk.JWK(**self.settings_conf[0]['symmetric_key']).export_symmetric(), 'utf-8'),
            bytes(data + 'cmdb', 'utf-8'),
            hashlib.sha256
        )
        generated_hash.hexdigest()
        return base64.b64encode(generated_hash.digest()).decode("utf-8")

    @staticmethod
    def generate_settings() -> (list, dict):
        settings = [{
            '_id': 'security',
            'symmetric_key': {"k": "9kYcXTqXCOyV_Li1avnWDPxoY2LPUnDDFOfjYSWuqHg", "kty": "oct"},
            'symmetric_aes_key': "dMoStgi5svlGIXHpysH2v6eH504L0LWFsTp1M72XMe4="
        }]
        return settings

    def _encrypt_aes(self, raw):
        """
        encrypt password data
        Args:
            raw: data

        Returns:
            encrypt binary list
        """
        from cmdb.utils.security import SecurityManager
        from Cryptodome import Random
        from Cryptodome.Cipher import AES

        if type(raw) == list:
            import json
            from bson import json_util
            raw = json.dumps(raw, default=json_util.default)
        raw = SecurityManager._pad(raw).encode('UTF-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(base64.b64decode(self.settings_conf[0]['symmetric_aes_key']), AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    @staticmethod
    def generate_default_groups() -> list:
        return [
            UserGroup(
                **{
                    "label": "Admin", "name": "admin", "public_id": 1,
                    "rights": [
                        "base.system.*",
                        "base.system.security",
                        "base.system.user_management",
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

    def generate_users(self, iterations=99) -> list:
        user_list = []
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
                password=self._generate_hmac('admin')
            )
        )
        public_id_counter = 2  # 1 is admin user
        for _ in range(iterations):
            user_list.append(
                User(
                    public_id=public_id_counter,
                    group_id=random.choice(self.user_group_list).get_public_id(),
                    first_name=self._faker.first_name(),
                    last_name=self._faker.last_name(),
                    user_name=self._faker.user_name(),
                    email=self._faker.email(),
                    registration_time=self._faker.date_time_between(start_date="-30d"),
                    authenticator='LocalAuthenticationProvider',
                    password=self._generate_hmac(self._faker.password())
                )
            )
            public_id_counter = public_id_counter + 1
        return user_list

    def generate_types(self) -> list:
        type_list = []

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
                    "creation_time": self._fake_date,
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
                            "date": self._fake_date
                        }
                    ]
                }
            )
        )
        return type_list

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
            })
        ]
        return category_list

    def generate_objects(self, num=1000) -> list:
        object_list = []
        public_id_counter = 1
        for _ in range(num):
            object_list.append(
                CmdbObject(
                    **{
                        "public_id": public_id_counter,
                        "author_id": random.choice(self.user_list).get_public_id(),
                        "type_id": 1,
                        "views": 0,
                        "version": "1.0.0",
                        "last_edit_time": None,
                        "active": self._faker.boolean(chance_of_getting_true=80),
                        "creation_time": self._faker.date_time_between(start_date="-30d"),
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
                                "value": self._encrypt_aes(self._faker.password())
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

            )
            public_id_counter = public_id_counter + 1
        return object_list


class NoDatabaseManagerError(CMDBError):
    """Error if field could not be initialized"""

    def __init__(self):
        super().__init__()
        self.message = 'Database manager was not passed.'
