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
"""TODO: document"""
import logging
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class JobManagementBase:
    """TODO: document"""
    ASCENDING = 1
    DESCENDING = -1
    COLLECTION = 'exportd.*'
    __SUPER_INIT_KEYS = [
        'public_id'
    ]
    SUPER_INDEX_KEYS = [
        {'keys': [('public_id', ASCENDING)], 'name': 'public_id', 'unique': True}
    ]
    IGNORED_INIT_KEYS = []
    REQUIRED_INIT_KEYS = []
    INDEX_KEYS = []

    def __init__(self, **kwargs):
        self.public_id = None
        for key, value in kwargs.items():
            setattr(self, key, value)



    @classmethod
    def get_index_keys(cls):
        """TODO: document"""
        from pymongo import IndexModel
        index_list = list()
        for index in cls.INDEX_KEYS + cls.SUPER_INDEX_KEYS:
            index_list.append(IndexModel(**index))
        return index_list



    def to_json(self) -> dict:
        """
        converts attribute dict to json - maybe later for database updates
        Returns:
            dict: json dump with database default encoding of the object attributes
        """
        from cmdb.database.utils import default
        import json
        return json.dumps(self.__dict__, default=default)



    def to_database(self):
        """TODO: document"""
        return self.__dict__
