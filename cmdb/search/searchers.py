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

from cmdb.framework.cmdb_object import CmdbObject
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.search import Search
from cmdb.search.query import Query, Pipeline
from cmdb.search.search_result import SearchResults
from cmdb.user_management import User

LOGGER = logging.getLogger(__name__)


class SearcherFramework(Search[CmdbObjectManager]):

    def __init__(self, manager: CmdbObjectManager):
        super(SearcherFramework, self).__init__(manager=manager)

    def aggregate(self, pipeline: Pipeline, request_user: User = None, limit: int = Search.DEFAULT_LIMIT,
                  skip: int = Search.DEFAULT_SKIP, *args, **kwargs) -> SearchResults:
        LOGGER.debug(pipeline)
        search_result = self.manager.search(collection=CmdbObject.COLLECTION, pipeline=pipeline)
        LOGGER.debug(search_result)
        return None

    def search(self, query: Query, request_user: User = None, limit: int = Search.DEFAULT_LIMIT,
               skip: int = Search.DEFAULT_SKIP) -> SearchResults:
        raw_search_result = self.manager.search(collection=CmdbObject.COLLECTION, query=query, limit=limit, skip=skip)
        raw_result_list = list(raw_search_result)

        return raw_search_result
