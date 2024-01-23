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

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

from cmdb.framework.cmdb_base import CmdbManagerBase
from cmdb.search.query import Query, Pipeline
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

M: TypeVar = TypeVar('M', bound=CmdbManagerBase)

#TODO: fix this
class Search(Generic[M], ABC):
    """TODO: document"""
    DEFAULT_SKIP: int = 0
    DEFAULT_LIMIT: int = 10
    DEFAULT_REGEX: str = ''

    def __init__(self, manager: M):
        self.__manager: M = manager


    @property
    def manager(self) -> M:
        """TODO: document"""
        return self.__manager


    @manager.setter
    def manager(self, manager: M):
        self.__manager: M = manager


    @abstractmethod
    def aggregate(self, pipeline: Pipeline, *args, **kwargs) -> List:
        """TODO: document"""
        raise NotImplementedError


    @abstractmethod
    def search(self, query: Query, *args, **kwargs) -> List:
        """TODO: document"""
        raise NotImplementedError
