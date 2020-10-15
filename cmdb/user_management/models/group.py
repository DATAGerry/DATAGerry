# DATAGERRY - OpenSource Enterprise CMDB
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
from json import dumps
from typing import List

from cmdb.data_storage.database_utils import default
from cmdb.framework import CmdbDAO
from cmdb.framework.utils import Collection, Model
from cmdb.user_management.models.right import GLOBAL_RIGHT_IDENTIFIER, BaseRight
from cmdb.utils.error import CMDBError

LOGGER = logging.getLogger(__name__)


class UserGroupModel(CmdbDAO):
    COLLECTION: Collection = 'management.groups'
    MODEL: Model = 'Group'
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
            'default': []
        }
    }

    __slots__ = 'public_id', 'name', 'label', 'rights'

    def __init__(self, public_id: int, name: str, label: str = None, rights: List[BaseRight] = None):
        self.name: str = name
        self.label: str = label or name.title()
        self.rights: list = rights or []
        super(UserGroupModel, self).__init__(public_id=public_id)

    @classmethod
    def from_data(cls, data: dict, rights: List[BaseRight] = None) -> "UserGroupModel":
        if rights:
            rights = [right for right in rights if right.name in data.get('rights', [])]
        else:
            rights = []
        return cls(
            public_id=data.get('public_id'),
            name=data.get('name'),
            label=data.get('label', None),
            rights=rights
        )

    @classmethod
    def to_data(cls, instance: "UserGroupModel"):
        return dumps(UserGroupModel.to_dict(instance), default=default)

    @classmethod
    def to_dict(cls, instance: "UserGroupModel") -> dict:

        return {
            'public_id': instance.public_id,
            'name': instance.name,
            'label': instance.label,
            'rights': [right.name for right in instance.rights]
        }

    def set_rights(self, rights: list):
        self.rights = rights

    def get_rights(self) -> list:
        return self.rights

    def get_right(self, name) -> str:
        try:
            return next(right for right in self.rights if right.name == name)
        except Exception:
            raise RightNotFoundError(self.name, name)

    def has_right(self, right_name) -> bool:
        try:
            self.get_right(right_name)
        except RightNotFoundError:
            return False
        return True

    def has_extended_right(self, right_name: str) -> bool:
        parent_right_name: str = right_name.rsplit(".", 1)[0]
        if self.has_right(f'{parent_right_name}.{GLOBAL_RIGHT_IDENTIFIER}'):
            return True
        if parent_right_name == 'base':
            return self.has_right(f'{parent_right_name}.{GLOBAL_RIGHT_IDENTIFIER}')
        return self.has_extended_right(right_name=parent_right_name)


class RightNotFoundError(CMDBError):
    def __init__(self, group, right):
        self.message = "Right was not found inside this group Groupname: {} | Rightname: {}".format(group, right)
        super(RightNotFoundError, self).__init__()
