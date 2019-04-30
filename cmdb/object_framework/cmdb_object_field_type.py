# Net|CMDB - OpenSource Enterprise CMDB
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

from cmdb.object_framework.cmdb_dao import CmdbDAO
from cmdb.utils.error import CMDBError


class CmdbFieldType(CmdbDAO):
    """
    Presentation of a field input_type which is created within the Cmdb input_type.
    """
    COLLECTION = 'objects.types[fields]'  # Not used - implemented into type class

    REQUIRED_INIT_KEYS = [
        'name',
        'label',
        'input_type',
    ]
    IGNORED_INIT_KEYS = [
        'public_id'
    ]
    INDEX_KEYS = [
        # {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, input_type: str, name: str, label: str = None, description: str = None, placeholder: str = None,
                 values: list = None, roles: list = None, subinput_type: str = None, maxlength: int = None,
                 required: bool = False, access: bool = False,
                 className: str = 'form-control', **kwargs):
        self.value = None
        self.input_type = input_type
        self.subinput_type = subinput_type
        self.name = name
        self.label = label or name.title()
        self.description = description
        self.placeholder = placeholder
        self.className = className
        self.values = values or []
        self.roles = roles or []
        self.maxlength = maxlength
        self.required = required
        self.access = access
        super(CmdbFieldType, self).__init__(**kwargs)

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        return self.value

    def get_type(self):
        return self.input_type

    def get_sub_type(self):
        if self.subinput_type is None or self.subinput_type == "":
            return self.input_type
        return self.subinput_type

    def is_protected(self):
        return self.access


class FieldNotFoundError(CMDBError):
    """Error if field do not exists"""

    def __init__(self, field_name, type_name):
        super().__init__()
        self.message = 'Field {} was not found inside input_type: {}'.format(field_name, type_name)
