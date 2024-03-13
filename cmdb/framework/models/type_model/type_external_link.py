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
This class represents an external link
"""
import logging
import re

from cmdb.framework.cmdb_errors import ExternalFillError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   TypeExternalLink                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
class TypeExternalLink:
    """This class represents an external link"""

    def __init__(self, name: str, href: str, label: str = None, icon: str = None, fields: list = None):
        self.name = name
        self.href = href
        self.label = label or self.name.title()
        self.icon = icon
        self.fields = fields or []

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "TypeExternalLink":
        """
        Generates a TypeExternalLink object from a dict

        Args:
            data (dict): Data with which the TypeExternalLink should be instantiated

        Returns:
            TypeExternalLink: TypeExternalLink class with given data
        """
        return cls(
            name = data.get('name'),
            href = data.get('href'),
            label = data.get('label', None),
            icon = data.get('icon', None),
            fields = data.get('fields', None)
        )


    @classmethod
    def to_json(cls, instance: "TypeExternalLink") -> dict:
        """
        Returns a TypeExternalLink as JSON representation

        Args:
            instance (TypeExternalLink): TypeExternalLink which should be transformed

        Returns:
            dict: JSON representation of the given TypeExternalLink
        """
        return {
            'name': instance.name,
            'href': instance.href,
            'label': instance.label,
            'icon': instance.icon,
            'fields': instance.fields
        }

# ------------------------------------------------- GENERAL FUNCTIONS ------------------------------------------------ #

    def has_icon(self) -> bool:
        """
        Checks if the TypeExternalLink has an icon

        Returns:
            (bool): True if icon is set else False
        """
        return bool(self.icon)


    def link_requires_fields(self) -> bool:
        """
        the type of arguments passed to it and formats it according to the format codes defined in the string
        checks if the href link requires field informations.
        Examples:
            http://example.org/{}/dynamic/ -> True
            http://example.org/static/ -> False
        Returns:
            bool
        """
        if re.search('{.*?}', self.href):
            return True
        return False


    def has_fields(self) -> bool:
        """
        Checks if the TypeExternalLink has any fields

        Returns:
            (bool): True if at least one field is set else False
        """
        return len(self.fields) > 0


    def fill_href(self, inputs) -> None:
        """Fills the href brackets with data"""
        try:
            self.href = self.href.format(*inputs)
        except Exception as err:
            raise ExternalFillError(inputs, err) from err
