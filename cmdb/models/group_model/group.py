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
import logging

from cmdb.models.cmdb_dao import CmdbDAO
from cmdb.models.right_model.base_right import BaseRight
from cmdb.models.right_model.constants import GLOBAL_RIGHT_IDENTIFIER

from cmdb.errors.security import RightNotFoundError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class UserGroupModel(CmdbDAO):
    """TODO: document"""
    COLLECTION = 'management.groups'
    MODEL = 'Group'
    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    SCHEMA: dict = {
        'public_id': {
            'type': 'integer',
            'required': False
        },
        'name': {
            'type': 'string',
            'required': True,
        },
        'label': {
            'type': 'string',
            'required': False,
        },
        'rights': {
            'type': 'list',
            'required': False,
            'default': []
        }
    }

    __slots__ = 'public_id', 'name', 'label', 'rights'

    def __init__(self, public_id: int, name: str, label: str = None, rights: list[BaseRight] = None):
        self.name: str = name
        self.label: str = label or name.title()
        self.rights: list = rights or []
        super().__init__(public_id=public_id)


    @classmethod
    def from_data(cls, data: dict, rights: list[BaseRight] = None) -> "UserGroupModel":
        """TODO: document"""
        if rights:
            rights = [right for right in rights if right['name'] in data.get('rights', [])]
        else:
            rights = []

        return cls(
            public_id=data.get('public_id'),
            name=data.get('name'),
            label=data.get('label', None),
            rights=rights
        )


    @classmethod
    def to_dict(cls, instance: "UserGroupModel") -> dict:
        """TODO: document"""
        return {
            'public_id': instance.public_id,
            'name': instance.name,
            'label': instance.label,
            'rights': [BaseRight.to_dict(right) for right in instance.rights]
        }


    @classmethod
    def to_data(cls, instance: "UserGroupModel") -> dict:
        """TODO: document"""
        return {
            'public_id': instance.public_id,
            'name': instance.name,
            'label': instance.label,
            'rights': [right.name for right in instance.rights]
        }


    def set_rights(self, rights: list):
        """TODO: document"""
        self.rights = rights


    def get_rights(self) -> list:
        """TODO: document"""
        return self.rights


    def get_right(self, name) -> str:
        """TODO: document"""
        try:
            return next(right for right in self.rights if right.name == name)
        except Exception as err:
            raise RightNotFoundError(f"Groupname: {self.name} | Rightname: {name}. Error: {err}") from err


    def has_right(self, right_name) -> bool:
        """TODO: document"""
        try:
            self.get_right(right_name)
        except RightNotFoundError:
            return False

        return True


    def has_extended_right(self, right_name: str) -> bool:
        """TODO: document"""
        parent_right_name: str = right_name.rsplit(".", 1)[0]
        if self.has_right(f'{parent_right_name}.{GLOBAL_RIGHT_IDENTIFIER}'):
            return True
        if parent_right_name == 'base':
            return self.has_right(f'{parent_right_name}.{GLOBAL_RIGHT_IDENTIFIER}')

        return self.has_extended_right(right_name=parent_right_name)
