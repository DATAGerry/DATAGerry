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

from pymongo import IndexModel
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                            TemplateManagementBase - CLASS                                            #
# -------------------------------------------------------------------------------------------------------------------- #
class TemplateManagementBase:
    """TODO: document"""
    ASCENDING = 1
    DESCENDING = -1
    COLLECTION = 'docapi.*'

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
        index_list = []
        for index in cls.INDEX_KEYS + cls.SUPER_INDEX_KEYS:
            index_list.append(IndexModel(**index))

        return index_list


    def to_database(self):
        """TODO: document"""
        return self.__dict__
