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
This class represents a TypeMultiDataSection
Extends: TypeSection
"""
import logging
import json

from cmdb.models.type_model.type_section import TypeSection
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               TypeMultiDataSection                                                   #
# -------------------------------------------------------------------------------------------------------------------- #

class TypeMultiDataSection(TypeSection):
    """
    This class represents a TypeMultiDataSection
    Extends: TypeSection
    """

    def __init__(self,
                 type: str,
                 name: str,
                 label: str = None,
                 fields: list = None,
                 hidden_fields: list = None):
        self.fields = fields or []
        self.hidden_fields = hidden_fields or []
        super().__init__(type=type, name=name, label=label)

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "TypeMultiDataSection":
        """
        Generates a TypeMultiDataSection object from a dict

        Args:
            data (dict): Data with which the TypeMultiDataSection should be instantiated

        Returns:
            TypeMultiDataSection: TypeMultiDataSection class with given data
        """
        return cls(
            type = data.get('type'),
            name = data.get('name'),
            label = data.get('label', None),
            fields = data.get('fields', None),
            hidden_fields = data.get('hidden_fields', [])
        )


    @classmethod
    def to_json(cls, instance: "TypeMultiDataSection") -> dict:
        """
        Returns a TypeMultiDataSection as JSON representation

        Args:
            instance (TypeMultiDataSection): TypeMultiDataSection which should be transformed

        Returns:
            dict: JSON representation of the given TypeMultiDataSection
        """
        return {
            'type': instance.type,
            'name': instance.name,
            'label': instance.label,
            'fields': instance.fields,
            'hidden_fields': instance.hidden_fields
        }

# -------------------------------------------------- GENERAL METHODS ------------------------------------------------- #

    def get_fields(self) -> list:
        """
        Retrieves all fields of the section

        Returns:
            list: All fields of the section
        """
        return self.fields


    def get_hidden_fields(self) -> list:
        """
        Retrieves all hidden fields of the section

        Returns:
            list: All hidden fields of the section
        """
        return self.fields


    def __str__(self):
        return json.dumps(TypeMultiDataSection.to_json(self))
