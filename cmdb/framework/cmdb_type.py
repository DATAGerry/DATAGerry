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
    COLLECTION = "objects.types"
    REQUIRED_INIT_KEYS = [
        'name',
        'active',
        'author_id',
        'creation_time',
        'render_meta',
        'fields'
    ]

    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, name: str, active: bool, author_id: int, creation_time: datetime,
                 render_meta: dict, fields: list, version: str = '1.0.0', access: list = None, label: str = None,
                 status: list = None, description: str = None, **kwargs):
        self.name = name
        self.label = label or self.name.title()
        self.description = description
        self.version = version
        self.status = status
        self.active = active
        self.access = access or []
        self.author_id = author_id
        self.creation_time = creation_time
        self.render_meta = render_meta
        self.fields = fields or []
        super(CmdbType, self).__init__(**kwargs)

    def __truediv__(self, other):
        if not isinstance(other, CmdbType):
            raise TypeError("Not a CmdbType instance")
        from deepdiff import DeepDiff
        return DeepDiff(self, other, ignore_order=True)

    def get_name(self):
        return self.name

    def get_label(self):
        return self.label

    def get_description(self):
        return self.description

    def get_externals(self):
        return self.render_meta['external']

    def has_externals(self):
        if len(self.get_externals()) > 0:
            return True
        else:
            return False

    def get_external(self, name):
        ext_data = next(ext for ext in self.render_meta['external'] if ext["name"] == name)
        return _ExternalLink(**ext_data)

    def get_summaries(self):
        return self.render_meta['summary']

    def has_summaries(self):
        if len(self.render_meta['summary']) > 0:
            return True
        return False

    def get_summary_fields(self, name):
        return self.get_summary(name)['fields']

    def get_summary(self, name):
        sum_data = next(sum for sum in self.render_meta['summary'] if sum["name"] == name)
        return _Summary(**sum_data)

    def get_sections(self):
        return sorted(self.render_meta['sections'], key=lambda k: k['position'])

    def get_section(self, name):
        try:
            return self.render_meta['sections'][name]
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
        field = [x for x in self.fields if x['input_type'] == input_type and x[_filter] == value]
        if field:
            LOGGER.debug('Field of type {}'.format(input_type))
            LOGGER.debug('Field len'.format(field))
            LOGGER.debug('Field {}'.format(len(field)))
            try:
                return field[0]
            except (RequiredInitKeyNotFoundError, CMDBError) as e:
                LOGGER.warning(e.message)
                raise FieldInitError(value)
        else:
            LOGGER.debug('Field of type {} NOT found'.format(input_type))
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

    def __init__(self, name: str, label: str = None, labels: [] = None, fields: list = None, values: list = None):
        self.name = name
        self.label = label or self.name.title()
        self.labels = labels or []
        self.fields = fields or []
        self.values = values

    def has_fields(self):
        if len(self.fields) > 0:
            return True
        return False

    def set_values(self, values):
        self.values = values

    def set_labels(self, labels):
        self.labels = labels

    def __repr__(self):
        output_string = "{}: {}".format(self.label, self.values)
        return output_string
