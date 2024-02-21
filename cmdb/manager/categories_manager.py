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
from cmdb.framework.managers.type_manager import TypeManager

from cmdb.framework import CategoryModel

from cmdb.errors.manager import ManagerInsertError

from .base_manager import BaseManager
from .query_builder.base_query_builder import BaseQueryBuilder
# -------------------------------------------------------------------------------------------------------------------- #
LOGGER = logging.getLogger(__name__)


class CategoriesManager(BaseManager):
    """
    The CategoriesManager handles the interaction between the Categories-API and the Database
    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, event_queue: Union[Queue, Event] = None):
        """
        Set the database connection and the queue for sending events

        Args:
            database_manager (DatabaseManagerMongo): Active database managers instance.
            event_queue (Queue, Event): The queue for sending events or the created event to send
        """
        self.event_queue = event_queue
        self.query_builder = BaseQueryBuilder()
        self.type_manager = TypeManager(dbm)
        super().__init__(CategoryModel.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_category(self, category: dict) -> int:
        """
        Insert a single category into the system.

        Args:
            category (dict): Raw data of the category.

        Notes:
            If no public id was given, the database manager will auto insert the next available ID.

        Returns:
            int: The Public ID of the new inserted category
        """
        if isinstance(category, CategoryModel):
            category = CategoryModel.to_json(category)

        try:
            ack = self.insert(category)
        except Exception as error:
            raise ManagerInsertError(error) from error

        return ack
