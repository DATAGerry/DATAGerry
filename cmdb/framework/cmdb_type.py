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

from cmdb.framework.cmdb_dao import CmdbDAO, RequiredInitKeyNotFoundError
from cmdb.framework.cmdb_errors import ExternalFillError, FieldInitError, FieldNotFoundError

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


class CmdbType(CmdbDAO):
    """
    Definition of an object type - which fields were created and how.
    """
    COLLECTION = "framework.types"
    REQUIRED_INIT_KEYS = [
        'name',
        'active',
        'author_id',
        'creation_time',
        'render_meta',
        'fields',
        'category_id'
    ]

    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, name: str, active: bool, author_id: int, creation_time: datetime,
                 render_meta: dict, fields: list, category_id: int, version: str = '1.0.0', access: list = None,
                 label: str = None,
                 clean_db: bool = None,
                 status: list = None, description: str = None, **kwargs):
        self.name = name
        self.label = label or self.name.title()
        self.description = description
        self.version = version
        self.status = status
        self.active = active
        self.clean_db = clean_db
        self.access = access or []
        self.author_id = author_id
        self.creation_time = creation_time
        self.render_meta = render_meta
        self.fields = fields or []
        self.category_id = category_id or 0
        super(CmdbType, self).__init__(**kwargs)

    def get_name(self) -> str:
        """Get the name of the type"""
        return self.name

    def get_label(self) -> str:
        """Get the label
        Notes:
            If no label was set the class will set the title of the name
        """
        return self.label

    def get_description(self) -> str:
        """Get the description"""
        return self.description

    def get_externals(self):
        """Get the render meta values of externals"""
        return self.render_meta['external']

    def has_externals(self) -> bool:
        """Check if type has external links"""
        return True if len(self.get_externals()) > 0 else False

    def get_external(self, name):
        ext_data = next(ext for ext in self.render_meta['external'] if ext["name"] == name)
        return _ExternalLink(**ext_data)

    def has_summaries(self):
        if len(self.render_meta['summary'].get('fields')) > 0:
            return True
        return False

    def get_summary(self):
        complete_field_list = []
        for field_name in self.render_meta['summary']['fields']:
            complete_field_list.append(self.get_field(field_name))
        return _Summary(fields=complete_field_list)

    def get_sections(self):
        return sorted(self.render_meta['sections'], key=lambda k: k['position'])

    def get_section(self, name):
        try:
            return self.render_meta['sections'][name]
        except IndexError:
            return None

    def get_icon(self):
        try:
            return self.render_meta['icon']
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

    def get_field_of_type_with_value(self, input_type: str, _filter: str, value) -> dict:
        field = [x for x in self.fields if x['type'] == input_type and x[_filter] == value]
        if field:
            try:
                return field[0]
            except (RequiredInitKeyNotFoundError, CMDBError) as e:
                raise FieldInitError(value)
        else:
            raise FieldNotFoundError(value, self.get_name())

    def get_field(self, name) -> dict:
        field = [x for x in self.fields if x['name'] == name]
        if field:
            try:
                return field[0]
            except (RequiredInitKeyNotFoundError, CMDBError) as e:
                LOGGER.warning(e.message)
                raise FieldInitError(name)
        raise FieldNotFoundError(name, self.get_name())


class _ExternalLink:

    def __init__(self, name: str, href: str, label: str = None, icon: str = None, fields: list = None):
        self.name = name
        self.href = href
        self.label = label or self.name.title()
        self.icon = icon
        self.fields = fields or []

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


class _Summary:

    def __init__(self, fields: list = None):
        self.fields = fields or []

    def has_fields(self):
        if len(self.fields) > 0:
            return True
        return False

    def set_fields(self, fields):
        self.fields = fields