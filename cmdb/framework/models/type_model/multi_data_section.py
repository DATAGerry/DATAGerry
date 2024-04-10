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

from cmdb.framework.models.type_model import TypeSection
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   MultiDataSection                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
class MultiDataSection(TypeSection):
    """
    This class represents a MultiDataSection
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
    def from_data(cls, data: dict) -> "MultiDataSection":
        """
        Generates a MultiDataSection object from a dict

        Args:
            data (dict): Data with which the MultiDataSection should be instantiated

        Returns:
            MultiDataSection: MultiDataSection class with given data
        """
        return cls(
            type = data.get('type'),
            name = data.get('name'),
            label = data.get('label', None),
            fields = data.get('fields', None),
            hidden_fields = data.get('hidden_fields', [])
        )


    @classmethod
    def to_json(cls, instance: "MultiDataSection") -> dict:
        """
        Returns a MultiDataSection as JSON representation

        Args:
            instance (MultiDataSection): MultiDataSection which should be transformed

        Returns:
            dict: JSON representation of the given MultiDataSection
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
