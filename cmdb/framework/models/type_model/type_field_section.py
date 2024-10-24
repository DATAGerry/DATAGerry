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
This class represents a type field section
Extends: TypeSection
"""
import logging
import json

from cmdb.framework.models.type_model.type_section import TypeSection
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   TypeFieldSection                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
class TypeFieldSection(TypeSection):
    """
    This class represents a type field section
    Extends: TypeSection
    """

    def __init__(self, type: str, name: str, label: str = None, fields: list = None):
        self.fields = fields or []
        super().__init__(type=type, name=name, label=label)

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "TypeFieldSection":
        """
        Generates a TypeFieldSection object from a dict

        Args:
            data (dict): Data with which the TypeFieldSection should be instantiated

        Returns:
            TypeFieldSection: TypeFieldSection class with given data
        """
        return cls(
            type = data.get('type'),
            name = data.get('name'),
            label = data.get('label', None),
            fields = data.get('fields', None)
        )


    @classmethod
    def to_json(cls, instance: "TypeFieldSection") -> dict:
        """
        Returns a TypeFieldSection as JSON representation

        Args:
            instance (TypeFieldSection): TypeFieldSection which should be transformed

        Returns:
            dict: JSON representation of the given TypeFieldSection
        """
        return {
            'type': instance.type,
            'name': instance.name,
            'label': instance.label,
            'fields': instance.fields
        }

# -------------------------------------------------- GENERAL METHODS ------------------------------------------------- #

    def get_fields(self) -> list:
        """
        Retrieves all fields of the section

        Returns:
            list: All fields of the section
        """
        return self.fields


    def __str__(self):
        return json.dumps(TypeFieldSection.to_json(self))
