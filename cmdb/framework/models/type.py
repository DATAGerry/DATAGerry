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

from datetime import datetime, timezone
from dateutil.parser import parse
from typing import List

from cmdb.framework.cmdb_dao import CmdbDAO, RequiredInitKeyNotFoundError
from cmdb.framework.cmdb_errors import ExternalFillError, FieldInitError, FieldNotFoundError, TypeReferenceLineFillError
from cmdb.framework.utils import Collection, Model
from cmdb.security.acl.control import AccessControlList
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
        return cls(fields=data.get('fields', []))

    @classmethod
    def to_json(cls, instance: "TypeSummary") -> dict:
        return {
            'fields': instance.fields
        }


class TypeReference:
    __slots__ = 'type_id', 'object_id', 'type_label', 'summaries', 'line', 'prefix', 'icon'

    def __init__(self, type_id: int, object_id: int, type_label: str, line: str = None,
                 prefix: bool = False, icon=None, summaries: list = None):
        self.type_id = type_id
        self.object_id = object_id
        self.type_label = type_label or ''
        self.summaries = summaries or []
        self.line = line
        self.icon = icon
        self.prefix = prefix

    @classmethod
    def from_data(cls, data: dict) -> "TypeReference":
        return cls(
            type_id=data.get('type_id'),
            object_id=data.get('object_id'),
            line=data.get('line'),
            type_label=data.get('type_label', None),
            summaries=data.get('summaries', None),
            icon=data.get('prefix', False),
            prefix=data.get('icon', None)
        )

    @classmethod
    def to_json(cls, instance: "TypeReference") -> dict:
        return {
            'type_id': instance.type_id,
            'object_id': instance.object_id,
            'line': instance.line,
            'type_label': instance.type_label,
            'summaries': instance.summaries,
            'icon': instance.icon,
            'prefix': instance.prefix
        }

    def has_prefix(self):
        """
        check if reference has a prefix
        """
        if self.prefix:
            return True
        return False

    def has_icon(self):
        """
        check if reference has a icon
        """
        if self.prefix:
            return True
        return False

    def line_requires_fields(self):
        """
        the type of arguments passed to it and formats it according to the format codes defined in the string
        checks if the line requires field informations.
        Examples:
            example {} -> True
            example -> False
        Returns:
            bool
        """
        import re
        if re.search('{.*?}', self.line):
            return True
        return False

    def has_summaries(self):
        """
        check if type references has summaries definitions
        """
        if len(self.summaries) > 0:
            return True
        return False

    def fill_line(self, inputs):
        """fills the line brackets with data"""
        try:
            self.line = self.line.format(*inputs)
        except Exception as e:
            raise TypeReferenceLineFillError(inputs, e)


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


class TypeSection:
    __slots__ = 'type', 'name', 'label'

    def __init__(self, type: str, name: str, label: str = None):
        self.type = type
        self.name = name
        self.label = label or self.name.title()

    @classmethod
    def from_data(cls, data: dict) -> "TypeSection":
        return cls(
            type=data.get('type'),
            name=data.get('name'),
            label=data.get('label', None),
        )

    @classmethod
    def to_json(cls, instance: "TypeSection") -> dict:
        return {
            'type': instance.type,
            'name': instance.name,
            'label': instance.label
        }


class TypeFieldSection(TypeSection):
    __slots__ = 'fields'

    def __init__(self, type: str, name: str, label: str = None, fields: list = None):
        self.fields = fields or []
        super(TypeFieldSection, self).__init__(type=type, name=name, label=label)

    @classmethod
    def from_data(cls, data: dict) -> "TypeFieldSection":
        return cls(
            type=data.get('type'),
            name=data.get('name'),
            label=data.get('label', None),
            fields=data.get('fields', None)
        )

    @classmethod
    def to_json(cls, instance: "TypeFieldSection") -> dict:
        return {
            'type': instance.type,
            'name': instance.name,
            'label': instance.label,
            'fields': instance.fields
        }


class TypeReferenceSectionEntry:
    __slots__ = 'type_id', 'section_name', 'selected_fields'

    def __init__(self, type_id: int, section_name: str, selected_fields: List[str] = None):
        self.type_id: int = type_id
        self.section_name: str = section_name
        self.selected_fields: List[str] = selected_fields or []

    @classmethod
    def from_data(cls, data: dict) -> "TypeReferenceSectionEntry":
        return cls(
            type_id=data.get('type_id'),
            section_name=data.get('section_name'),
            selected_fields=data.get('selected_fields', None))

    @classmethod
    def to_json(cls, instance: "TypeReferenceSectionEntry") -> dict:
        return {
            'type_id': instance.type_id,
            'section_name': instance.section_name,
            'selected_fields': instance.selected_fields
        }


class TypeReferenceSection(TypeSection):
    __slots__ = 'reference', 'fields'

    def __init__(self, type: str, name: str, label: str = None, reference: TypeReferenceSectionEntry = None,
                 fields: list = None):
        self.reference: reference = reference or {}
        self.fields = fields or []
        super(TypeReferenceSection, self).__init__(type=type, name=name, label=label)

    @classmethod
    def from_data(cls, data: dict) -> "TypeReferenceSection":
        reference = data.get('reference', None)
        if reference:
            reference = TypeReferenceSectionEntry.from_data(reference)
        return cls(
            type=data.get('type'),
            name=data.get('name'),
            label=data.get('label', None),
            reference=reference,
            fields=data.get('fields', None)
        )

    @classmethod
    def to_json(cls, instance: "TypeReferenceSection") -> dict:
        return {
            'type': instance.type,
            'name': instance.name,
            'label': instance.label,
            'reference': TypeReferenceSectionEntry.to_json(instance.reference),
            'fields': instance.fields,
        }


class TypeRenderMeta:
    """Class of the type models `render_meta` field"""

    __slots__ = 'icon', 'sections', 'externals', 'summary'

    def __init__(self, icon: str = None, sections: List[TypeSection] = None,
                 externals: List[TypeExternalLink] = None,
                 summary: TypeSummary = None):
        self.icon: str = icon
        self.sections: List[TypeSection] = sections or []
        self.externals: List[TypeExternalLink] = externals or []
        self.summary: TypeSummary = summary or TypeSummary(fields=None)

    @classmethod
    def from_data(cls, data: dict) -> "TypeRenderMeta":
        sections: List[TypeSection] = []
        for section in data.get('sections', []):
            section_type = section.get('type', 'section')
            if section_type == 'section':
                sections.append(TypeFieldSection.from_data(section))
            elif section_type == 'ref-section':
                sections.append(TypeReferenceSection.from_data(section))
            else:
                sections.append(TypeFieldSection.from_data(section))


        return cls(
            icon=data.get('icon', None),
            sections=sections,
            externals=[TypeExternalLink.from_data(external) for external in
                       data.get('externals', None) or data.get('external', [])],
            summary=TypeSummary.from_data(data.get('summary', {}))
        )

    @classmethod
    def to_json(cls, instance: "TypeRenderMeta") -> dict:
        return {
            'icon': instance.icon,
            'sections': [section.to_json(section) for section in instance.sections],
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
        'editor_id': {
            'type': 'integer',
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
            'required': False,
            'default': None
        },
        'version': {
            'type': 'string',
            'default': DEFAULT_VERSION
        },
        'description': {
            'type': 'string',
            'nullable': True,
            'empty': True
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
                 creation_time: datetime = None, last_edit_time: datetime = None, editor_id: int = None,
                 active: bool = True, fields: list = None, version: str = None,
                 label: str = None, description: str = None, acl: AccessControlList = None):
        self.name: str = name
        self.label: str = label or self.name.title()
        self.description: str = description
        self.version: str = version or TypeModel.DEFAULT_VERSION
        self.active: bool = active
        self.author_id: int = author_id
        self.creation_time: datetime = creation_time or datetime.now(timezone.utc)
        self.editor_id: int = editor_id
        self.last_edit_time: datetime = last_edit_time
        self.render_meta: TypeRenderMeta = render_meta
        self.fields: list = fields or []
        self.acl: AccessControlList = acl
        super(TypeModel, self).__init__(public_id=public_id)

    @classmethod
    def from_data(cls, data: dict) -> "TypeModel":
        """Create a instance of TypeModel from database values"""
        creation_time = data.get('creation_time', None)
        if creation_time and isinstance(creation_time, str):
            creation_time = parse(creation_time, fuzzy=True)

        last_edit_time = data.get('last_edit_time', None)
        if last_edit_time and isinstance(last_edit_time, str):
            last_edit_time = parse(last_edit_time, fuzzy=True)

        return cls(
            public_id=data.get('public_id'),
            name=data.get('name'),
            active=data.get('active', True),
            author_id=data.get('author_id'),
            creation_time=creation_time,
            editor_id=data.get('editor_id', None),
            last_edit_time=last_edit_time,
            label=data.get('label', None),
            version=data.get('version', None),
            description=data.get('description', None),
            render_meta=TypeRenderMeta.from_data(data.get('render_meta', {})),
            fields=data.get('fields', None) or [],
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
            'editor_id': instance.editor_id,
            'last_edit_time': instance.last_edit_time,
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

    def get_nested_summaries(self):
        return next((x['summaries'] for x in self.get_fields() if x['type'] == 'ref' and 'summaries' in x), [])

    def has_nested_prefix(self, nested_summaries):
        return next((x['prefix'] for x in nested_summaries if x['type_id'] == self.public_id), False)

    def get_nested_summary_fields(self, nested_summaries):
        _fields = next((x['fields'] for x in nested_summaries if x['type_id'] == self.public_id), [])
        complete_field_list = []
        for field_name in _fields:
            complete_field_list.append(self.get_field(field_name))
        return TypeSummary(fields=complete_field_list).fields

    def get_nested_summary_line(self, nested_summaries):
        return next((x['line'] for x in nested_summaries if x['type_id'] == self.public_id), None)

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
