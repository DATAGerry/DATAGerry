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

from abc import ABC, abstractmethod

from cmdb.framework import CmdbDAO, CmdbObject
from cmdb.framework.cmdb_object_manager import CmdbObjectManager

LOGGER = logging.getLogger(__name__)


class Search(ABC):
    COLLECTION = CmdbDAO.COLLECTION

    def __init__(self, object_manager: CmdbObjectManager):
        self.__object_manager: CmdbObjectManager = object_manager

    @property
    def object_manager(self):
        return self.__object_manager

    @object_manager.setter
    def object_manager(self, manager: CmdbObjectManager):
        self.__object_manager = manager

    @abstractmethod
    def search(self, *args, **kwargs):
        LOGGER.debug(f'[Search] Starting search for {self.__class__.__name__} with args {args} and kwargs {kwargs}')
        raise NotImplementedError


class SearchObject(Search):

    COLLECTION = CmdbObject.COLLECTION

    def __init__(self, object_manager: CmdbObjectManager):
        super(SearchObject, self).__init__(object_manager=object_manager)

    def search(self, *args, **kwargs):
        super().search(*args, **kwargs)