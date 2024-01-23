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
"""
This module contains the implementation of QueryBuilder and
LocationManager which are responsible to interact with the Database 
regarding locations.
"""
import logging
from queue import Queue
from typing import Union, List

from cmdb.search import Pipeline
from cmdb.framework import CmdbSectionTemplate
from cmdb.event_management.event import Event
from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.manager.managers import ManagerBase
from cmdb.framework.managers.query_builders.default_query_builder import DefaultQueryBuilder
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel
from cmdb.framework.results import IterationResult
from cmdb.manager import ManagerGetError, ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                            SectionTemplateManager - CLASS                                            #
# -------------------------------------------------------------------------------------------------------------------- #

class SectionTemplateManager(ManagerBase):
    """
    The Locationmanager interacts between API functions and database
    """

    def __init__(self, database_manager: DatabaseManagerMongo, event_queue: Union[Queue, Event] = None):
        """
        Set the database connection and the queue for sending events.

        Args:
            database_manager (DatabaseManagerMongo): Active database managers instance.
            event_queue (Queue, Event): The queue for sending events or the created event to send
        """
        self.event_queue = event_queue
        self.query_builder = DefaultQueryBuilder()
        super().__init__(CmdbSectionTemplate.COLLECTION, database_manager)


    def iterate(self, filter: Union[List[dict], dict], limit: int, skip: int, sort: str, order: int,
                user: UserModel = None, permission: AccessControlPermission = None, *args, **kwargs) \
            -> IterationResult[CmdbSectionTemplate]:
        """TODO: document"""
        try:
            query: Pipeline = self.query_builder.build(filter_=filter, limit=limit, skip=skip, sort=sort, order=order,
                                                        user=user, permission=permission)
            count_query: Pipeline = self.query_builder.count(filter_=filter)
            aggregation_result = list(self._aggregate(CmdbSectionTemplate.COLLECTION, query))
            total_cursor = self._aggregate(CmdbSectionTemplate.COLLECTION, count_query)
            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']
        except ManagerGetError as err:
            raise ManagerIterationError(err=err) from err

        iteration_result: IterationResult[CmdbSectionTemplate] = IterationResult(aggregation_result, total)
        iteration_result.convert_to(CmdbSectionTemplate)
        return iteration_result
