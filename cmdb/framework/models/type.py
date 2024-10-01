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
Represents a type in DATAGERRY
Extends: CmdbDAO
"""
import logging
from datetime import datetime, timezone
from dateutil.parser import parse

from cmdb.framework.utils import Collection, Model
from cmdb.security.acl.control import AccessControlList
from cmdb.cmdb_objects.cmdb_dao import CmdbDAO
from cmdb.framework.models.type_model import TypeSummary, TypeExternalLink, TypeSection, TypeRenderMeta

from cmdb.errors.cmdb_object import RequiredInitKeyNotFoundError
from cmdb.errors.type import FieldNotFoundError, FieldInitError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   TypeModel - CLASS                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
class TypeModel(CmdbDAO):
    """
    Model class of the framework type
    Extends: CmdbDAO
    
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
        'selectable_as_parent': {
            'type': 'boolean',
            'default': True
        },
        'global_template_ids':{
            'type': 'list',
            'required': False,
            'schema': {
                'type': 'string',
            }
        },
        'active': {
            'type': 'boolean',
            'required': False,
            'default': True
        },
        'fields': {
            'type': 'list',
            'required': False,
            'default': None,
            'schema': {
                'type': 'dict',
                'schema': {
                    "type": {
                        'type': 'string',  # Text, Password, Textarea, radio, select, date
                        'required': True
                    },
                    "required": {
                        'type': 'boolean',
                        'required': False
                    },
                    "name": {
                        'type': 'string',
                        'required': True
                    },
                    "rows": {
                        'type': 'integer',
                        'required': False
                    },
                    "label": {
                        'type': 'string',
                        'required': True
                    },
                    "description": {
                        'type': 'string',
                        'required': False,
                    },
                    "regex": {
                        'type': 'string',
                        'required': False
                    },
                    "placeholder": {
                        'type': 'string',
                        'required': False,
                    },
                    "value": {
                        'required': False,
                        'nullable': True,
                    },
                    "helperText": {
                        'type': 'string',
                        'required': False,
                    },
                    "default": {
                        'type': 'integer',
                        'nullable': True,
                        'empty': True
                    },
                    "options": {
                        'type': 'list',
                        'empty': True,
                        'required': False,
                        'schema': {
                            'type': 'dict',
                            'schema': {
                                "name": {
                                    'type': 'string',
                                    'required': True
                                },
                                "label": {
                                    'type': 'string',
                                    'required': True
                                },
                            }
                        }
                    },
                    "ref_types": {
                        'type': 'list',  # List of public_id of type
                        'required': False,
                        'empty': True,
                        'schema': {
                            'type': ['integer', 'list'],
                        }
                    },
                    "summaries": {
                        'type': 'list',
                        'empty': True,
                        'schema': {
                            'type': 'dict',
                            'schema': {
                                "type_id": {
                                    'type': 'integer',
                                    'required': True
                                },
                                "line": {
                                    'type': 'string',
                                    # enter curved brackets for field interpolation example: Customer IP {}
                                    'required': True
                                },
                                "label": {
                                    'type': 'string',
                                    'required': True
                                },
                                "fields": {  # List of field names
                                    'type': 'list',
                                    'empty': True,
                                },
                                "icon": {
                                    'type': 'string',  # Free Font Awesome example: 'fa fa-cube'
                                    'required': True
                                },
                                "prefix": {
                                    'type': 'boolean',
                                    'required': False,
                                    'default': True
                                }
                            }
                        }
                    }
                }
            },
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
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            "type": {
                                'type': 'string',
                                'required': True
                            },
                            "name": {
                                'type': 'string',
                                'required': True
                            },
                            "label": {
                                'type': 'string',
                                'required': True
                            },
                            "hidden_fields": {
                                'type': 'list',
                                'required': False
                            },
                            "reference": {
                                'type': 'dict',
                                'empty': True,
                                'schema': {
                                    "type_id": {
                                        'type': 'integer',
                                        'required': True
                                    },
                                    "section_name": {
                                        'type': 'string',
                                        'required': True
                                    },
                                    'selected_fields': {
                                        'type': 'list',
                                        'empty': True
                                    }
                                }
                            },
                            'fields': {
                                'type': 'list',
                                'empty': True,
                            }
                        }
                    },
                    'empty': True
                },
                'externals': {
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'name': {
                                'type': 'string',
                                'required': True
                            },
                            'href': {
                                'type': 'string',  # enter curved brackets for field interpolation example: Field {}
                                'required': True
                            },
                            'label': {
                                'type': 'string',
                                'required': True
                            },
                            'icon': {
                                'type': 'string',
                                'required': True
                            },
                            'fields': {
                                'type': 'list',
                                'schema': {
                                    'type': 'string',
                                    'required': False
                                },
                                'empty': True,
                            }
                        }
                    },
                    'empty': True,
                },
                'summary': {
                    'type': 'dict',
                    'schema': {
                        'fields': {
                            'type': 'list',
                            'schema': {
                                'type': 'string',
                                'required': False
                            },
                            'empty': True,
                        }
                    },
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

    INDEX_KEYS = [{
        'keys': [('name', CmdbDAO.DAO_ASCENDING)],
        'name': 'name',
        'unique': True
    }]


    def __init__(self, public_id: int, name: str, author_id: int, render_meta: TypeRenderMeta,
                 creation_time: datetime = None, last_edit_time: datetime = None, editor_id: int = None,
                 active: bool = True,  selectable_as_parent: bool = True,
                 global_template_ids: list[int] = None, fields: list = None, version: str = None,
                 label: str = None, description: str = None, acl: AccessControlList = None):
        self.name: str = name
        self.label: str = label or self.name.title()
        self.description: str = description
        self.version: str = version or TypeModel.DEFAULT_VERSION
        self.selectable_as_parent: bool = selectable_as_parent
        self.global_template_ids: list = global_template_ids or []
        self.active: bool = active
        self.author_id: int = author_id
        self.creation_time: datetime = creation_time or datetime.now(timezone.utc)
        self.editor_id: int = editor_id
        self.last_edit_time: datetime = last_edit_time
        self.render_meta: TypeRenderMeta = render_meta
        self.fields: list = fields or []
        self.acl: AccessControlList = acl
        super().__init__(public_id=public_id)

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "TypeModel":
        """
        Generates a TypeModel object from a dict

        Args:
            data (dict): Data with which the TypeModel should be instantiated

        Returns:
            TypeModel: TypeModel class with given data
        """
        creation_time = data.get('creation_time', None)
        if creation_time and isinstance(creation_time, str):
            creation_time = parse(creation_time, fuzzy=True)

        last_edit_time = data.get('last_edit_time', None)
        if last_edit_time and isinstance(last_edit_time, str):
            last_edit_time = parse(last_edit_time, fuzzy=True)

        return cls(
            public_id = data.get('public_id'),
            name = data.get('name'),
            selectable_as_parent = data.get('selectable_as_parent', True),
            global_template_ids = data.get('global_template_ids', []),
            active = data.get('active', True),
            author_id = data.get('author_id'),
            creation_time = creation_time,
            editor_id = data.get('editor_id', None),
            last_edit_time = last_edit_time,
            label = data.get('label', None),
            version = data.get('version', None),
            description = data.get('description', None),
            render_meta = TypeRenderMeta.from_data(data.get('render_meta', {})),
            fields = data.get('fields', None) or [],
            acl = AccessControlList.from_data(data.get('acl', {}))
        )


    @classmethod
    def to_json(cls, instance: "TypeModel") -> dict:
        """Convert a type instance to json conform data"""
        return {
            'public_id': instance.get_public_id(),
            'name': instance.name,
            'selectable_as_parent': instance.selectable_as_parent,
            'global_template_ids': instance.global_template_ids,
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

# ------------------------------------------------- GENERAL FUNCTIONS ------------------------------------------------ #

    def get_name(self) -> str:
        """Get the name of the type"""
        return self.name


    def get_label(self) -> str:
        """Get the display name"""
        if not self.label:
            self.label = self.name.title()

        return self.label


    def get_externals(self) -> list[TypeExternalLink]:
        """Get the render meta values of externals"""
        return self.render_meta.externals


    def has_externals(self) -> bool:
        """Check if type has external links"""
        return len(self.get_externals()) > 0


    def get_external(self, name) -> TypeExternalLink:
        """Retrive an external link"""
        return next((external for external in self.get_externals() if external.name == name), None)


    def has_summaries(self) -> bool:
        """Checks if there are any fields in the render_meta.summary object"""
        return self.render_meta.summary.has_fields()


    def get_nested_summaries(self):
        """TODO: document"""
        return next((x['summaries'] for x in self.get_fields() if x['type'] == 'ref' and 'summaries' in x), [])


    def has_nested_prefix(self, nested_summaries):
        """TODO: document"""
        return next((x['prefix'] for x in nested_summaries if x['type_id'] == self.public_id), False)


    def get_nested_summary_fields(self, nested_summaries) -> list[str]:
        """TODO: document"""
        _fields = next((x['fields'] for x in nested_summaries if x['type_id'] == self.public_id), [])
        complete_field_list = []
        for field_name in _fields:
            complete_field_list.append(self.get_field(field_name))

        return TypeSummary(fields=complete_field_list).fields


    def get_nested_summary_line(self, nested_summaries):
        """TODO: document"""
        return next((x['line'] for x in nested_summaries if x['type_id'] == self.public_id), None)


    def get_summary(self) -> TypeSummary:
        """TODO: document"""
        complete_field_list = []
        for field_name in self.render_meta.summary.fields:
            complete_field_list.append(self.get_field(field_name))
        return TypeSummary(fields=complete_field_list)


    def get_sections(self) -> list[TypeSection]:
        """TODO: document"""
        return self.render_meta.sections


    def get_section(self, name: str) -> TypeSection:
        """
        Retrieves a section with the given name

        Args:
            name (str): Name of the section

        Returns:
            TypeSection: The Typesection with the given name else None
        """
        try:
            return next((section for section in self.get_sections() if section.name == name), None)
        except IndexError:
            return None


    def get_icon(self) -> str:
        """Retrieves the icon of the current TypeModel"""
        try:
            return self.render_meta.icon
        except IndexError:
            return None


    def has_sections(self) -> bool:
        """
        Checks if the TypeModel has any sections

        Returns:
            (bool): True if at least one section is present else False
        """
        return self.get_sections() > 0


    def get_fields(self) -> list:
        """Retuns all fields of the TypeModel"""
        return self.fields


    def count_fields(self) -> int:
        """Returns the number of fields"""
        return len(self.fields)


    def get_fields_of_type_with_value(self, input_type: str, _filter: str, value) -> list:
        """TODO: document"""
        fields = [x for x in self.fields if
                  x['type'] == input_type and (value in x.get(_filter, None) if isinstance(x.get(_filter, None), list)
                                               else x.get(_filter, None) == value)]
        if fields:
            try:
                return fields
            except (RequiredInitKeyNotFoundError, Exception) as err:
                #TODO: ERROR-FIX
                raise FieldInitError(str(value)) from err
        else:
            #TODO: ERROR-FIX
            raise FieldNotFoundError(value)


    def get_field(self, name) -> dict:
        """TODO: document"""
        field = [x for x in self.fields if x['name'] == name]
        if field:
            try:
                return field[0]
            except (RequiredInitKeyNotFoundError, Exception) as err:
                #TODO: ERROR-FIX
                raise FieldInitError(name) from err

        raise FieldNotFoundError(name)
