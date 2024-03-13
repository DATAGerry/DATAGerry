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
"""Contains implementation of BaseManager"""
import logging

from cmdb.database.mongo_database_manager import MongoDatabaseManager

from cmdb.framework.utils import Collection
from cmdb.errors.manager import ManagerInsertError,\
                                ManagerGetError,\
                                ManagerUpdateError,\
                                ManagerDeleteError,\
                                ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

class BaseManager:
    """This is the base for every FrameworkManager"""

    def __init__(self, collection: Collection, dbm: MongoDatabaseManager):
        self.collection: Collection = collection
        self.dbm: MongoDatabaseManager = dbm


    def __exit__(self, exc_type, exc_val, exc_tb):
        """Auto disconnect the database connection when the Manager get destroyed."""
        self.dbm.connector.disconnect()

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert(self, data: dict, skip_public: bool = False) -> int:
        """
        Insert document/object into database

        Args:
            data (dict): Data which should be inserted
            skip_public (bool): Skip the public id creation and counter increment
        Returns:
            int: New public_id of inserted document
            None: If anything goes wrong
        """
        try:
            return self.dbm.insert(self.collection, data, skip_public)
        except Exception as err:
            raise ManagerInsertError(err) from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_one(self, *args, **kwargs):
        """
        Calls MongoDB find operation with *args for a single document

        Returns:
            Cursor over the result set
        """
        try:
            return self.dbm.find_one(self.collection, *args, **kwargs)
        except Exception as err:
            raise ManagerGetError(err) from err


    def get(self, *args, **kwargs):
        """
        General find function

        Raises:
            ManagerGetError: When something goes wrong while retrieving the documents

        Returns:
            Cursor: Result of the 'find'-Operation as Cursor
        """
        try:
            return self.dbm.find(self.collection, *args, **kwargs)
        except Exception as err:
            raise ManagerGetError(err) from err


    def get_one_by(self, criteria: dict):
        """
        Retrieves a single document defined by a filter

        Args:
            criteria (dict): Filter for the document
        """
        try:
            return self.dbm.find_one_by(self.collection, criteria)
        except Exception as err:
            raise ManagerGetError(err) from err


    def get_many(self,
                 sort: str = 'public_id',
                 direction: int = -1,
                 limit=0,
                 **requirements: dict) -> list[dict]:
        """Get all documents from the database which have the passing requirements

        Args:
            sort (str): sort by given key - default public_id
            **requirements (dict): dictionary of key value pairs

        Returns:
            list: list of all documents
        """
        requirements_filter = {}
        formatted_sort = [(sort, direction)]

        for k, req in requirements.items():
            requirements_filter.update({k: req})

        return self.dbm.find_all(collection=self.collection,
                                 limit=limit,
                                 filter=requirements_filter,
                                 sort=formatted_sort)


    def aggregate(self, *args, **kwargs):
        """
        Calls MongoDB aggregation with *args
        Args:
        Returns:
            - A :class:`~pymongo.command_cursor.CommandCursor` over the result set
        """
        try:
            return self.dbm.aggregate(self.collection, *args, **kwargs)
        except Exception as err:
            raise ManagerIterationError(err) from err


    def get_next_public_id(self):
        """
        Retrieves next public_id for the collection

        Returns:
            int: New highest public_id of the collection
        """
        return self.dbm.get_next_public_id(self.collection)

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update(self, criteria: dict, data: dict, *args, **kwargs):
        """
        Calls MongoDB update operation
        Args:
            criteria (dict): Filter to match dictionary
            data: Update data (normally a dict)

        Returns:
            UpdateResult
        """
        try:
            return self.dbm.update(self.collection, criteria, data, *args, **kwargs)
        except Exception as err:
            raise ManagerUpdateError(err) from err


    def update_many(self, criteria: dict, update: dict, add_to_set: bool = False):
        """
        Update all documents that match the filter from a collection

        Args:
            criteria (dict): Filter that matches the documents to update
            update (dict): The modifications to apply
        Returns:
            Acknowledgment of database
        """
        try:
            return self.dbm.update_many(self.collection, criteria, update, add_to_set)
        except Exception as err:
            raise ManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete(self, criteria: dict) -> bool:
        """
        Calls MongoDB delete operation

        Args:
            criteria (dict): Filter to match document
        Raises:
            ManagerDeleteError: Something went wrong while trying to delete document

        Returns:
            bool: True if deletion is successful
        """
        try:
            return self.dbm.delete(self.collection, criteria).acknowledged
        except Exception as err:
            raise ManagerDeleteError(err) from err
