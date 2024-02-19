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
This module contains the implementation of the SectionTemplatesManager
"""
import logging
from queue import Queue
from typing import Union

from cmdb.event_management.event import Event
from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.framework import CmdbSectionTemplate
from cmdb.framework.results import IterationResult
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel

from cmdb.errors.manager import ManagerGetError, ManagerIterationError

from .base_manager import BaseManager
from .query_builder.base_query_builder import BaseQueryBuilder
from .query_builder.builder_parameters import BuilderParameters
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class SectionTemplatesManager(BaseManager):
    """The SectionTemplatesManager handles the interaction between the SectionTemplates-API and the Database"""

    def __init__(self, dbm: MongoDatabaseManager, event_queue: Union[Queue, Event] = None):
        """
        Set the database connection and the queue for sending events

        Args:
            database_manager (DatabaseManagerMongo): Active database managers instance.
            event_queue (Queue, Event): The queue for sending events or the created event to send
        """
        self.event_queue = event_queue
        self.query_builder = BaseQueryBuilder()
        super().__init__(CmdbSectionTemplate.COLLECTION, dbm)


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def iterate(self,
                builder_params: BuilderParameters,
                user: UserModel = None,
                permission: AccessControlPermission = None) -> IterationResult[CmdbSectionTemplate]:
        """
        Performs an aggregation on the database
        Args:
            builder_params (BuilderParameters): Contains input to identify the target of action
            user (UserModel, optional): User requesting this action
            permission (AccessControlPermission, optional): Permission which should be checked for the user

        Raises:
            ManagerIterationError: Raised when something goes wrong during the aggregate part
            ManagerIterationError: Raised when something goes wrong during the building of the IterationResult

        Returns:
            IterationResult[CmdbSectionTemplate]: Result which matches the Builderparameters
        """
        try:
            query: list[dict] = self.query_builder.build(builder_params,user, permission)
            count_query: list[dict] = self.query_builder.count(builder_params.get_criteria())

            aggregation_result = list(self.aggregate(query))
            total_cursor = self.aggregate(count_query)

            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']

        except ManagerGetError as err:
            raise ManagerIterationError(err) from err

        try:
            iteration_result: IterationResult[CmdbSectionTemplate] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbSectionTemplate)
        except Exception as err:
            raise ManagerIterationError(err) from err

        return iteration_result
