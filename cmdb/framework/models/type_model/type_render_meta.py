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
This class represents type render meta
"""
import logging
from typing import List

from cmdb.framework.models.type_model import TypeSection, \
                                             TypeExternalLink, \
                                             TypeSummary, \
                                             TypeFieldSection, \
                                             TypeReferenceSection
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                    TypeRenderMeta                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
class TypeRenderMeta:
    """Class of the type models `render_meta` field"""

    def __init__(self, icon: str = None, sections: List[TypeSection] = None,
                 externals: List[TypeExternalLink] = None,
                 summary: TypeSummary = None):
        self.icon: str = icon
        self.sections: List[TypeSection] = sections or []
        self.externals: List[TypeExternalLink] = externals or []
        self.summary: TypeSummary = summary or TypeSummary(fields=None)


# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "TypeRenderMeta":
        """
        Generates a TypeRenderMeta object from a dict

        Args:
            data (dict): Data with which the TypeRenderMeta should be instantiated

        Returns:
            TypeRenderMeta: TypeRenderMeta class with given data
        """
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
        """
        Returns a TypeRenderMeta as JSON representation

        Args:
            instance (TypeRenderMeta): TypeRenderMeta which should be transformed

        Returns:
            dict: JSON representation of the given TypeRenderMeta
        """
        return {
            'icon': instance.icon,
            'sections': [section.to_json(section) for section in instance.sections],
            'externals': [TypeExternalLink.to_json(external) for external in instance.externals],
            'summary': TypeSummary.to_json(instance.summary)
        }
