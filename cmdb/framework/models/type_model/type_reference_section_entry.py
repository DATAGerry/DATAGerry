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
This class represents a type reference section entry
"""
import logging
from typing import List
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               TypeReferenceSectionEntry                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class TypeReferenceSectionEntry:
    """This class represents a type reference section entry"""

    def __init__(self, type_id: int, section_name: str, selected_fields: List[str] = None):
        self.type_id: int = type_id
        self.section_name: str = section_name
        self.selected_fields: List[str] = selected_fields or []

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "TypeReferenceSectionEntry":
        """
        Generates a TypeReferenceSectionEntry object from a dict

        Args:
            data (dict): Data with which the TypeReferenceSectionEntry should be instantiated

        Returns:
            TypeReferenceSectionEntry: TypeReferenceSectionEntry class with given data
        """
        return cls(
            type_id = data.get('type_id'),
            section_name = data.get('section_name'),
            selected_fields = data.get('selected_fields', None)
        )


    @classmethod
    def to_json(cls, instance: "TypeReferenceSectionEntry") -> dict:
        """
        Returns a TypeReferenceSectionEntry as JSON representation

        Args:
            instance (TypeReferenceSectionEntry): TypeReferenceSectionEntry which should be transformed

        Returns:
            dict: JSON representation of the given TypeReferenceSectionEntry
        """
        return {
            'type_id': instance.type_id,
            'section_name': instance.section_name,
            'selected_fields': instance.selected_fields
        }
