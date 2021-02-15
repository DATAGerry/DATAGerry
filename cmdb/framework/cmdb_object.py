# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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

import logging

from cmdb.framework.cmdb_dao import CmdbDAO
from cmdb.framework.cmdb_errors import FieldNotFoundError
from cmdb.framework.utils import Collection, Model
from dateutil.parser import parse

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


class CmdbObject(CmdbDAO):
    """The CMDB object is the basic data wrapper for storing and holding the pure objects within the CMDB.
    """

    COLLECTION: Collection = 'framework.objects'
    MODEL: Model = 'Object'
    REQUIRED_INIT_KEYS = [
        'type_id',
        'creation_time',
        'author_id',
        'active',
        'fields',
        'version'
    ]

    def __init__(self, type_id, creation_time, author_id, active, fields, last_edit_time=None, editor_id: int = None,
                 status: int = None, version: str = '1.0.0', **kwargs):
        """init of object

        Args:
            type_id: public input_type id which implements the object
            version: current version of object
            creation_time: date of object creation
            author_id: public id of author
            last_edit_time: last date of editing
            editor_id: id of the last editor
            active: object activation status
            fields: data inside fields
            **kwargs: additional data
        """
        self.type_id = type_id
        self.status = status
        self.version = version
        self.creation_time = creation_time
        self.author_id = author_id
        self.last_edit_time = last_edit_time
        self.editor_id = editor_id
        self.active = active
        self.fields = fields
        super(CmdbObject, self).__init__(**kwargs)

    def __truediv__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Not the same class")
        return {**{'old': [i for i in self.fields if i not in other.fields]},
                **{'new': [j for j in other.fields if j not in self.fields]}}

    @classmethod
    def from_data(cls, data: dict, *args, **kwargs) -> "CmdbObject":
        creation_time = data.get('creation_time', None)
        last_edit_time = data.get('last_edit_time', None)
        if creation_time and isinstance(creation_time, str):
            creation_time = parse(creation_time, fuzzy=True)
        if last_edit_time and isinstance(last_edit_time, str):
            last_edit_time = parse(last_edit_time, fuzzy=True)
        return cls(
            type_id=data.get('type_id'),
            version=data.get('version'),
            creation_time=creation_time,
            author_id=data.get('author_id'),
            last_edit_time=last_edit_time,
            editor_id=data.get('editor_id', None),
            active=data.get('active'),
            fields=data.get('fields', []),
            public_id=data.get('public_id')
        )

    def get_type_id(self) -> int:
        """get input_type if of this object

        Returns:
            int: public id of input_type

        """
        if self.type_id == 0 or self.type_id is None:
            raise TypeNotSetError(self.get_public_id())
        return int(self.type_id)

    def update_view_counter(self) -> int:
        """update the number of times this object was viewed

        Returns:
            int: number of views

        """
        self.views += 1
        return self.views

    def get_all_fields(self) -> list:
        """ get all fields with key value pair

        Returns:
            all fields

        """

        return self.fields

    def has_field(self, name) -> bool:
        field = next(iter([x for x in self.fields if x.get('name') == name]), None)
        if field is None:
            return False
        return True

    def set_new_value(self, field, value):
        self.fields.append({
            'name': field,
            'value': value
        })

    def set_value(self, field, value) -> str:
        for f in self.fields:
            if f['name'] == field:
                if value.isdigit():
                    value = int(value)
                f['value'] = value
                return f['name']
            continue
        raise FieldNotFoundError

    def get_value(self, field) -> (str, None):
        """get value of an field

        Args:
            field: field_name

        Returns:
            value of field
        """
        for f in self.fields:
            if f['name'] == field:
                return f['value']
            continue
        raise ValueError(field)

    def get_values(self, fields: list) -> list:
        list_of_values = []
        for field in self.fields:
            if field['name'] in fields:
                list_of_values.append(field['value'])
        return list_of_values

    def to_value_strings(self, field_names: list) -> str:
        value_string = ''
        for field_name in field_names:
            try:
                field_value = self.get_value(field_name)
                value_string += str(field_value)
                value_string += str(' ')
            except CMDBError:
                continue
        return value_string.strip()


class TypeNotSetError(CMDBError):
    """
    @deprecated
    """

    def __init__(self, public_id):
        self.message = 'The object (ID: {}) is not connected with a input_type'.format(public_id)
        super(CMDBError, self).__init__(self.message)


class NoFoundFieldValueError(CMDBError):
    """
    Error when field does not exists
    """

    def __init__(self, field_name):
        self.message = "Field value does not exists {}".format(field_name)
        super(CMDBError, self).__init__(self.message)


class NoLinksAvailableError(CMDBError):
    """
    @deprecated
    """

    def __init__(self, public_id):
        self.message = 'The object (ID: {}) has no links'.format(public_id)
        super(CMDBError, self).__init__(self.message)
