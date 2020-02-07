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
from typing import Generic, TypeVar, List

from cmdb.framework.cmdb_base import CmdbManagerBase

LOGGER = logging.getLogger(__name__)

M: TypeVar = TypeVar('M', bound=CmdbManagerBase)


class Search(Generic[M], ABC):

    DEFAULT_SKIP: int = 0
    DEFAULT_LIMIT: int = 25

    def __init__(self, manager: M):
        self.__manager: M = manager

    @property
    def manager(self) -> M:
        return self.__manager

    @manager.setter
    def manager(self, manager: M):
        self.__manager: M = manager

    @abstractmethod
    def search(self, *args, **kwargs) -> List:
        raise NotImplementedError
