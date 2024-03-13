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
"""TODO: document"""
from enum import Enum

from cmdb.framework.cmdb_dao import CmdbDAO
from cmdb.docapi.docapi_template.docapi_template_base import TemplateManagementBase
from cmdb.framework.utils import Model
from cmdb.errors.docapi import NoPublicIDError
# -------------------------------------------------------------------------------------------------------------------- #

class DocapiTemplateType(Enum):
    """TODO: document"""
    OBJECT = 0


class DocapiTemplate(TemplateManagementBase):
    """
    Docapi Template
    """
    COLLECTION = 'docapi.templates'
    MODEL: Model = 'DocapiTemplate'

    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, name, label=None, description=None, active=None, author_id=None,
                 template_data=None, template_style=None, template_type=None, template_parameters=None, **kwargs):
        """
        Args:
            name: name of this template
            label: label of this template
            active: is template active
            author_id: author of this template
            template_data: the content of this template (e.g. HTML string or reference to an HTML file)
            template_style: style of template
            template_type: type of docapi template
            template_parameters: parameter of this template depending on the type
            **kwargs: optional params
        """
        self.name = name
        self.label = label
        self.description = description
        self.active = active
        self.author_id = author_id
        self.template_data = template_data
        self.template_style = template_style
        self.template_type = template_type or DocapiTemplateType.OBJECT.name
        self.template_parameters = template_parameters
        super().__init__(**kwargs)


    @classmethod
    def from_data(cls, data: dict) -> "DocapiTemplate":
        """TODO: document"""
        return cls(
            public_id=data.get('public_id'),
            name=data.get('name'),
            label=data.get('label', None),
            description=data.get('description', None),
            active=data.get('active', None),
            author_id=data.get('author_id', None),
            template_data=data.get('template_data', None),
            template_style=data.get('template_style', None),
            template_type=data.get('template_type', None),
            template_parameters=data.get('template_parameters', None),
        )


    @classmethod
    def to_json(cls, instance: "DocapiTemplate", *args, **kwargs) -> dict:
        """TODO: document"""
        return {
            'public_id': instance.public_id,
            'name': instance.name,
            'label': instance.label,
            'description': instance.description,
            'active': instance.active,
            'author_id': instance.author_id,
            'template_data': instance.template_data,
            'template_style': instance.template_style,
            'template_type': instance.template_type,
            'template_parameters': instance.template_parameters
        }


    def get_public_id(self) -> int:
        """
        get the public id of current element

        Note:
            Since the models object is not initializable
            the child class object will inherit this function
            SHOULD NOT BE OVERWRITTEN!
        Returns:
            int: public id
        Raises:
            NoPublicIDError: if `public_id` is zero or not set
        """
        if self.public_id == 0 or self.public_id is None:
            raise NoPublicIDError()
        return self.public_id


    def get_name(self) -> str:
        """
        Get the name of the template
        Returns:
            str: display name
        """
        if self.name is None:
            return ""
        else:
            return self.name


    def get_label(self) -> str:
        """
        Get the label of the template
        Returns:
            str: display label
        """
        if self.label is None:
            return ""

        return self.label


    def get_description(self) -> str:
        """
        Get the description of the template
        Returns:
            str: description
        """
        if self.description is None:
            return ""

        return self.description


    def get_active(self) -> bool:
        """
        Get active state of the template
        Returns:
            bool: is template executable
        """
        if self.active is None:
            return ""

        return self.active


    def get_author_id(self):
        """TODO: document"""
        return self.author_id


    def get_template_data(self):
        """
        Get data of this template
        Returns:
            str:
        """
        return self.template_data


    def get_template_style(self):
        """
        Get style of this template
        Returns:
            str:
        """
        return self.template_style


    def get_template_type(self):
        """
        Get type of this template
        Returns:
            str:
        """
        return self.template_type


    def get_template_parameters(self):
        """
        Get parameters of this template
        Returns:
            str:
        """
        return self.template_parameters
