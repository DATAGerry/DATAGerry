# DATAGERRY - OpenSource Enterprise CMDB
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

import logging

from datetime import datetime
from typing import List

from cmdb.framework.cmdb_dao import CmdbDAO, RequiredInitKeyNotFoundError
from cmdb.framework.cmdb_errors import ExternalFillError, FieldInitError, FieldNotFoundError
from cmdb.framework.utils import Collection, Model
from cmdb.security.acl import AccessControlList
from cmdb.utils.error import CMDBError

LOGGER = logging.getLogger(__name__)


class TypeSummary:
    __slots__ = 'fields'

    def __init__(self, fields: list = None):
        self.fields = fields or []

    def has_fields(self):
        if len(self.fields) > 0:
            return True
        return False

    def set_fields(self, fields):
        self.fields = fields

    @classmethod
    def from_data(cls, data: dict) -> "TypeSummary":
        return cls(fields=data.get('fields', None))

    @classmethod
    def to_json(cls, instance: "TypeSummary") -> dict:
        return {
            'fields': instance.fields
        }


class TypeSection:
    __slots__ = 'type', 'name', 'label', 'fields'

    def __init__(self, type: str, name: str, label: str = None, fields: list = None):
        self.type = type
        self.name = name
        self.label = label or self.name.title()
        self.fields = fields or []

    @classmethod
    def from_data(cls, data: dict) -> "TypeSection":
        return cls(
            type=data.get('type'),
            name=data.get('name'),
            label=data.get('label', None),
            fields=data.get('fields', None)
        )

    @classmethod
    def to_json(cls, instance: "TypeSection") -> dict:
        return {
            'type': instance.type,
            'name': instance.name,
            'label': instance.label,
            'fields': instance.fields
        }


class TypeExternalLink:
    __slots__ = 'name', 'href', 'label', 'icon', 'fields'

    def __init__(self, name: str, href: str, label: str = None, icon: str = None, fields: list = None):
        self.name = name
        self.href = href
        self.label = label or self.name.title()
        self.icon = icon
        self.fields = fields or []

    @classmethod
    def from_data(cls, data: dict) -> "TypeExternalLink":
        return cls(
            name=data.get('name'),
            href=data.get('href'),
            label=data.get('label', None),
            icon=data.get('icon', None),
            fields=data.get('fields', None)
        )

    @classmethod
    def to_json(cls, instance: "TypeExternalLink") -> dict:
        return {
            'name': instance.name,
            'href': instance.href,
            'label': instance.label,
            'icon': instance.icon,
            'fields': instance.fields
        }

    def has_icon(self):
        """
        check if external link has a icon
        """
        if self.icon:
            return True
        return False

    def link_requires_fields(self):
        """
        the type of arguments passed to it and formats it according to the format codes defined in the string
        checks if the href link requires field informations.
        Examples:
            http://example.org/{}/dynamic/ -> True
            http://example.org/static/ -> False
        Returns:
            bool
        """
        import re
        if re.search('{.*?}', self.href):
            return True
        return False

    def has_fields(self):
        """
        check if external link has field definitions
        """
        if len(self.fields) > 0:
            return True
        return False

    def fill_href(self, inputs):
        """fills the href brackets with data"""
        try:
            self.href = self.href.format(*inputs)
        except Exception as e:
            raise ExternalFillError(inputs, e)


class TypeRenderMeta:
    """Class of the type models `render_meta` field"""

    __slots__ = 'icon', 'sections', 'externals', 'summary'

    def __init__(self, icon: str = None, sections: List[TypeSection] = None, externals: List[TypeExternalLink] = None,
                 summary: TypeSummary = None):
        self.icon: str = icon
        self.sections: List[TypeSection] = sections or []
        self.externals: List[TypeExternalLink] = externals or []
        self.summary: TypeSummary = summary or TypeSummary(fields=None)

    @classmethod
    def from_data(cls, data: dict) -> "TypeRenderMeta":
        return cls(
            icon=data.get('icon', None),
            sections=[TypeSection.from_data(section) for section in data.get('sections', [])],
            externals=[TypeExternalLink.from_data(external) for external in
                       data.get('externals', None) or data.get('external', [])],
            summary=TypeSummary.from_data(data.get('summary', None))
        )

    @classmethod
    def to_json(cls, instance: "TypeRenderMeta") -> dict:
        return {
            'icon': instance.icon,
            'sections': [TypeSection.to_json(section) for section in instance.sections],
            'externals': [TypeExternalLink.to_json(external) for external in instance.externals],
            'summary': TypeSummary.to_json(instance.summary)
        }


class TypeModel(CmdbDAO):
    """
    Model class of the framework type.

    Attributes:
        COLLECTION (Collection):    Name of the database collection.
        MODEL (Model):              Name of the DAO.
        DEFAULT_VERSION (str):      The default "starting" version number.
        SCHEMA (dict):              The validation schema for this DAO.
        INDEX_KEYS (list):          List of index keys for the database.
    """

    COLLECTION: Collection = "framework.types"
    MODEL: Model = 'Type'
    DEFAULT_VERSION: str = '1.0.0'
    SCHEMA: dict = {
        'public_id': {
            'type': 'integer'
        },
        'name': {
            'type': 'string',
            'required': True,
            'regex': r'(\w+)-*(\w)([\w-]*)'  # kebab case validation,
        },
        'label': {
            'type': 'string',
            'required': False
        },
        'author_id': {
            'type': 'integer',
            'required': True
        },
        'active': {
            'type': 'boolean',
            'required': False,
            'default': True
        },
        'fields': {
            'type': 'list',
            'default': []
        },
        'version': {
            'type': 'string',
            'default': DEFAULT_VERSION
        },
        'description': {
            'type': 'string'
        },
        'render_meta': {
            'type': 'dict',
            'allow_unknown': False,
            'schema': {
                'icon': {
                    'type': 'string',
                    'nullable': True
                },
                'sections': {
                    'type': 'list',
                    'empty': True
                },
                'externals': {
                    'type': 'list',
                    'empty': True
                },
                'summary': {
                    'type': 'dict',
                    'empty': True
                }
            }
        },
        'acl': {
            'type': 'dict',
            'allow_unknown': True,
            'required': False,
        }
    }

    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    __slots__ = 'public_id', 'name', 'label', 'description', 'version', 'active', 'author_id', \
                'creation_time', 'render_meta', 'fields', 'acl'

    def __init__(self, public_id: int, name: str, author_id: int, render_meta: TypeRenderMeta,
                 creation_time: datetime = None, active: bool = True, fields: list = None, version: str = None,
                 label: str = None, description: str = None, acl: AccessControlList = None):
        self.name: str = name
        self.label: str = label or self.name.title()
        self.description: str = description
        self.version: str = version or TypeModel.DEFAULT_VERSION
        self.active: bool = active
        self.author_id: int = author_id
        self.creation_time: datetime = creation_time or datetime.utcnow()
        self.render_meta: TypeRenderMeta = render_meta
        self.fields: list = fields or []
        self.acl: AccessControlList = acl
        super(TypeModel, self).__init__(public_id=public_id)

    @classmethod
    def from_data(cls, data: dict) -> "TypeModel":
        """Create a instance of TypeModel from database values"""
        return cls(
            public_id=data.get('public_id'),
            name=data.get('name'),
            active=data.get('active', True),
            author_id=data.get('author_id'),
            creation_time=data.get('creation_time', None),
            label=data.get('label', None),
            version=data.get('version', None),
            description=data.get('description', None),
            render_meta=TypeRenderMeta.from_data(data.get('render_meta', {})),
            fields=data.get('fields', None),
            acl=AccessControlList.from_data(data.get('acl', {}))
        )

    @classmethod
    def to_json(cls, instance: "TypeModel") -> dict:
        """Convert a type instance to json conform data"""
        return {
            'public_id': instance.get_public_id(),
            'name': instance.name,
            'active': instance.active,
            'author_id': instance.author_id,
            'creation_time': instance.creation_time,
            'label': instance.label,
            'version': instance.version,
            'description': instance.description,
            'render_meta': TypeRenderMeta.to_json(instance.render_meta),
            'fields': instance.fields,
            'acl': AccessControlList.to_json(instance.acl)
        }

    def get_name(self) -> str:
        """Get the name of the type"""
        return self.name

    def get_label(self) -> str:
        """Get the display name"""
        if not self.label:
            self.label = self.name.title()
        return self.label

    def get_externals(self) -> List[TypeExternalLink]:
        """Get the render meta values of externals"""
        return self.render_meta.externals

    def has_externals(self) -> bool:
        """Check if type has external links"""
        return True if len(self.get_externals()) > 0 else False

    def get_external(self, name) -> TypeExternalLink:
        return next((external for external in self.get_externals() if external.name == name), None)

    def has_summaries(self):
        return self.render_meta.summary.has_fields()

    def get_summary(self):
        complete_field_list = []
        for field_name in self.render_meta.summary.fields:
            complete_field_list.append(self.get_field(field_name))
        return TypeSummary(fields=complete_field_list)

    def get_sections(self) -> List[TypeSection]:
        return self.render_meta.sections

    def get_section(self, name):
        try:
            return next((section for section in self.get_sections() if section.name == name), None)
        except IndexError:
            return None

    def get_icon(self):
        try:
            return self.render_meta.icon
        except IndexError:
            return None

    def has_sections(self):
        if len(self.get_sections()) == 0:
            return False
        return True

    def get_fields(self) -> list:
        return self.fields

    def count_fields(self) -> int:
        return len(self.fields)

    def get_fields_of_type_with_value(self, input_type: str, _filter: str, value) -> list:
        fields = [x for x in self.fields if
                  x['type'] == input_type and (value in x.get(_filter, None) if isinstance(x.get(_filter, None), list)
                                               else x.get(_filter, None) == value)]
        if fields:
            try:
                return fields
            except (RequiredInitKeyNotFoundError, CMDBError) as e:
                raise FieldInitError(value)
        else:
            raise FieldNotFoundError(value, self.name)

    def get_field(self, name) -> dict:
        field = [x for x in self.fields if x['name'] == name]
        if field:
            try:
                return field[0]
            except (RequiredInitKeyNotFoundError, CMDBError) as e:
                LOGGER.warning(e.message)
                raise FieldInitError(name)
        raise FieldNotFoundError(name, self.name)
