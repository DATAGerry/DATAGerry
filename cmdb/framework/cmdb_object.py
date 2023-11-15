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
This module contains the implementation of CmdbObject, which is representing
an object in Datagarry.
"""
import logging
from dateutil.parser import parse

from cmdb.framework.cmdb_dao import CmdbDAO
from cmdb.framework.cmdb_errors import FieldNotFoundError
from cmdb.framework.utils import Collection, Model

from cmdb.utils.error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  CmdbObject - CLASS                                                  #
# -------------------------------------------------------------------------------------------------------------------- #

class CmdbObject(CmdbDAO):
    """
    The CMDB object is the basic data wrapper for storing and
    holding the pure objects within the CMDB.

    Attributes:
        COLLECTION (Collection):    Name of the database collection.
        MODEL (Model):              Name of the DAO.
        DEFAULT_VERSION (str):      The default "starting" version number.
        SCHEMA (dict):              The validation schema for this DAO.
        INDEX_KEYS (list):          List of index keys for the database.
    """

    COLLECTION: Collection = 'framework.objects'
    MODEL: Model = 'Object'
    DEFAULT_VERSION: str = '1.0.0'
    REQUIRED_INIT_KEYS = ['type_id', 'creation_time', 'author_id', 'active', 'fields', 'version']
    SCHEMA: dict = {
        'public_id': {
            'type': 'integer'
        },
        'type_id': {
            'type': 'integer'
        },
        'status': {
            'type': 'boolean',
            'required': False,
            'default': True
        },
        'version': {
            'type': 'string',
            'default': DEFAULT_VERSION
        },
        'author_id': {
            'type': 'integer',
            'required': True
        },
        'creation_time': {
            'type': 'dict',
            'nullable': True,
            'required': False
        },
        'last_edit_time': {
            'type': 'dict',
            'nullable': True,
            'required': False
        },
        'active': {
            'type': 'boolean',
            'required': False,
            'default': True
        },
        'fields': {
            'type': 'list',
            'required': True,
            'default': [],
        }
    }


    def __init__(self,
                 type_id,
                 creation_time,
                 author_id,
                 active,
                 fields: list,
                 last_edit_time=None,
                 editor_id: int = None,
                 status: int = None,
                 version: str = '1.0.0',
                 **kwargs):
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
        super().__init__(**kwargs)



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
            public_id=data.get('public_id'),
            type_id=data.get('type_id'),
            status=data.get('status', False),
            version=data.get('version'),
            creation_time=creation_time,
            author_id=data.get('author_id'),
            last_edit_time=last_edit_time,
            editor_id=data.get('editor_id', None),
            active=data.get('active'),
            fields=data.get('fields', [])
        )



    @classmethod
    def to_json(cls, instance: "CmdbObject") -> dict:
        """Convert a type instance to json conform data"""
        return {
            'public_id': instance.get_public_id(),
            'type_id': instance.get_type_id(),
            'status': instance.status,
            'version': instance.version,
            'creation_time': instance.creation_time,
            'author_id': instance.author_id,
            'last_edit_time': instance.last_edit_time,
            'editor_id': instance.editor_id,
            'active': instance.active,
            'fields': instance.fields,
        }



    def get_type_id(self) -> int:
        """get input_type if of this object

        Returns:
            int: public id of input_type
        """
        if self.type_id == 0 or self.type_id is None:
            raise TypeNotSetError(self.get_public_id())

        return int(self.type_id)



    def get_all_fields(self) -> list:
        """ Get all fields with key value pair

        Returns:
            all fields
        """
        return self.fields



    def has_field(self, name) -> bool:
        """TODO: document"""
        field = next(iter([x for x in self.fields if x.get('name') == name]), None)
        if field is None:
            return False

        return True



    def set_new_value(self, field, value):
        """TODO: document"""
        self.fields.append({
            'name': field,
            'value': value
        })



    def set_value(self, field, value) -> str:
        """TODO: document"""
        for f in self.fields:
            if f['name'] == field:
                if value.isdigit():
                    value = int(value)
                f['value'] = value
                return f['name']
            continue
        raise FieldNotFoundError



    def get_value(self, field) -> (str, None):
        """Get value of a field

        Args:
            field: Name of field

        Returns:
            Value of field
        """
        for f in self.fields:
            if f['name'] == field:
                return f['value']
            continue
        raise ValueError(field)



    def get_values(self, fields: list) -> list:
        """TODO: document"""
        list_of_values = []
        for field in self.fields:
            if field['name'] in fields:
                list_of_values.append(field['value'])
        return list_of_values



    def to_value_strings(self, field_names: list) -> str:
        """TODO: document"""
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
        self.message = f'The object (ID: {public_id}) is not connected with a input_type'
        super(CMDBError, self).__init__(self.message)



class NoFoundFieldValueError(CMDBError):
    """
    Error when field does not exists
    """
    def __init__(self, field_name):
        self.message = f"Field value does not exists {field_name}"
        super(CMDBError, self).__init__(self.message)
