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
"""
This module contains the implementation of QueryBuilder and
LocationManager which are responsible to interact with the Database 
regarding locations.
"""
from typing import Union
from queue import Queue

from cmdb.framework import CmdbSectionTemplate
from cmdb.event_management.event import Event
from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.manager.managers import ManagerBase
from cmdb.framework.managers.query_builders.default_query_builder import DefaultQueryBuilder
# -------------------------------------------------------------------------------------------------------------------- #

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

