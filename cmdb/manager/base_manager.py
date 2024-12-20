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
from pymongo.results import DeleteResult

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.query_builder.base_query_builder import BaseQueryBuilder
from cmdb.manager.query_builder.builder_parameters import BuilderParameters

from cmdb.models.user_model.user import UserModel
from cmdb.security.acl.permission import AccessControlPermission

from cmdb.errors.manager import ManagerInsertError,\
                                ManagerGetError,\
                                ManagerUpdateError,\
                                ManagerDeleteError,\
                                ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  BaseManager - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class BaseManager:
    """This is the base class for every FrameworkManager"""

    def __init__(self, collection: str, dbm: MongoDatabaseManager):
        self.collection = collection
        self.query_builder = BaseQueryBuilder()
        self.dbm: MongoDatabaseManager = dbm


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Auto disconnect the database connection when the Manager get destroyed
        """
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

    def iterate_query(self,
                      builder_params: BuilderParameters,
                      user: UserModel = None,
                      permission: AccessControlPermission = None):
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
            IterationResult[CmdbObject]: Result which matches the Builderparameters
        """
        try:
            query: list[dict] = self.query_builder.build(builder_params, user, permission)
            count_query: list[dict] = self.query_builder.count(builder_params.get_criteria())

            aggregation_result = list(self.aggregate(query))
            total_cursor = self.aggregate(count_query)

            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']

            return aggregation_result , total
        #TODO: ERROR-FIX
        except ManagerGetError as err:
            raise ManagerIterationError(err) from err


    def get_one(self, *args, **kwargs):
        """
        Calls MongoDB find operation for a single document

        Returns:
            Cursor over the result set
        """
        try:
            return self.dbm.find_one(self.collection, *args, **kwargs)
        except Exception as err:
            raise ManagerGetError(err) from err


    def get_one_from_other_collection(self, collection: str, public_id: int):
        """
        Calls MongoDB find operation for a single document from another collection

        Returns:
            Cursor over the result set
        """
        try:
            return self.dbm.find_one(collection, public_id)
        except Exception as err:
            raise ManagerGetError(err) from err


    def get_many_from_other_collection(self,
                                       collection: str,
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

        return self.dbm.find_all(collection=collection,
                                 limit=limit,
                                 filter=requirements_filter,
                                 sort=formatted_sort)


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
            LOGGER.debug("[get] Error: %s , Type: %s", err, type(err))
            raise ManagerGetError(err) from err


    def find_all(self, *args, **kwargs):
        """calls find with all returns

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            list: list of found documents
        """
        found_documents = self.find(collection=self.collection, *args, **kwargs)

        return list(found_documents)


    def find(self, *args, criteria=None, **kwargs):
        """TODO: document"""
        try:
            return self.dbm.find(self.collection, filter=criteria, *args, **kwargs)
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


    def aggregate_from_other_collection(self, collection: str, *args, **kwargs):
        """
        Calls MongoDB aggregation with *args
        Args:
        Returns:
            - A :class:`~pymongo.command_cursor.CommandCursor` over the result set
        """
        try:
            return self.dbm.aggregate(collection, *args, **kwargs)
        except Exception as err:
            raise ManagerIterationError(err) from err


    def get_next_public_id(self):
        """
        Retrieves next public_id for the collection

        Returns:
            int: New highest public_id of the collection
        """
        return self.dbm.get_next_public_id(self.collection)


    def count_documents(self, collection: str, *args, **kwargs):
        """
        Calls mongodb count operation
        Args:
            collection: Name of the collection

        Raises:
            ManagerGetError: If an error occures during the 'count' operation

        Returns:
            int: Number of found documents with given filter 
        """
        try:
            return self.dbm.count(collection, *args, **kwargs)
        except Exception as err:
            LOGGER.debug("[count_documents] Error: %s , Type: %s", err, type(err))
            raise ManagerGetError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update(self, criteria: dict, data: dict, add_to_set: bool = True, *args, **kwargs):
        """
        Calls MongoDB update operation
        Args:
            criteria (dict): Filter to match dictionary
            data: Update data (normally a dict)

        Returns:
            UpdateResult
        """
        try:
            return self.dbm.update(self.collection, criteria, data, add_to_set, *args, **kwargs)
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


    def delete_many(self, filter_query: dict) -> DeleteResult:
        """
        Removes all documents that match the filter from a collection

        Args:
            filter (dict): Specifies deletion criteria using query operators

        Raises:
            ManagerDeleteError: If something goes wrong

        Returns:
            Acknowledgment of database
        """
        try:
            delete_result = self.dbm.delete_many(collection=self.collection, **filter_query)
        except Exception as err:
            raise ManagerDeleteError(str(err)) from err

        return delete_result
