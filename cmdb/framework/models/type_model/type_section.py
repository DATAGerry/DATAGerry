# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
This class represents a type section
"""
import logging
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                      TypeSection                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
class TypeSection:
    """Type section class"""

    def __init__(self, type: str, name: str, label: str = None):
        self.type = type
        self.name = name
        self.label = label or self.name.title()


# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "TypeSection":
        """
        Generates a TypeSection object from a dict

        Args:
            data (dict): Data with which the TypeSection should be instantiated

        Returns:
            TypeSection: TypeSection class with given data
        """
        return cls(
            type = data.get('type'),
            name = data.get('name'),
            label = data.get('label', None),
        )


    @classmethod
    def to_json(cls, instance: "TypeSection") -> dict:
        """
        Returns a TypeSection as JSON representation

        Args:
            instance (TypeSection): TypeSection which should be transformed

        Returns:
            dict: JSON representation of the given TypeSection
        """
        return {
            'type': instance.type,
            'name': instance.name,
            'label': instance.label
        }
