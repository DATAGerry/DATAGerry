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

from cmdb.framework.cmdb_dao import NoPublicIDError, RequiredInitKeyNotFoundError
try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


class UserManagementBase:
    ASCENDING = 1
    DESCENDING = -1
    COLLECTION = 'management.*'
    __SUPER_INIT_KEYS = [
        'public_id'
    ]
    __SUPER_INDEX_KEYS = [
        {'keys': [('public_id', ASCENDING)], 'name': 'public_id', 'unique': True}
    ]
    IGNORED_INIT_KEYS = []
    REQUIRED_INIT_KEYS = []
    INDEX_KEYS = []

    def __init__(self, **kwargs):
        self.public_id = None
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __new__(cls, *args, **kwargs):
        init_keys = cls.__SUPER_INIT_KEYS + cls.REQUIRED_INIT_KEYS
        if len(cls.IGNORED_INIT_KEYS) > 0:
            init_keys = [i for j, i in enumerate(init_keys) if j in cls.IGNORED_INIT_KEYS]
        for req_key in init_keys:
            if req_key in kwargs:
                continue
            else:
                raise RequiredInitKeyNotFoundError(req_key)
        return super(UserManagementBase, cls).__new__(cls)

    def get_public_id(self) -> int:
        if self.public_id == 0 or self.public_id is None:
            raise NoUserIDError(self.public_id)
        return self.public_id

    @classmethod
    def get_index_keys(cls):
        from pymongo import IndexModel
        index_list = list()
        for index in cls.INDEX_KEYS + cls.__SUPER_INDEX_KEYS:
            index_list.append(IndexModel(**index))
        return index_list

    def to_json(self) -> dict:
        """
        converts attribute dict to json - maybe later for database updates
        Returns:
            dict: json dump with database default encoding of the object attributes
        """
        from cmdb.data_storage.database_utils import default
        import json
        return json.dumps(self.__dict__, default=default)

    def to_database(self):
        return self.__dict__


class NoUserIDError(NoPublicIDError):

    def __init__(self, user_id=None):
        self.message = f'UserModel ID not set - UserID: {user_id}'
        super(NoPublicIDError, self).__init__(self.message)
