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

from cmdb.database.database_manager_mongo import DatabaseManagerMongo
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                    CmdbManagerBase                                                   #
# -------------------------------------------------------------------------------------------------------------------- #

class CmdbManagerBase:
    """
    Represents the base class for cmdb managers. A respective implementation is always adapted to the
    respective database manager :class:`cmdb.database.DatabaseManager`.
    """

    def __init__(self, database_manager: DatabaseManagerMongo):
        """Example:
            Depending on the condition or whether a fork process is used, the database managers can also be seen
            directly in the declaration of the object managers

        Args:
            database_manager (DatabaseManagerMongo): Instance of DatabaseManagerMongo
        """
        self.dbm: DatabaseManagerMongo = database_manager


    def _count(self, collection: str) -> int:
        """Get the number of objects in given collection

        Args:
            collection: Collection name
        Returns:
            (int): number of found objects
        """
        return self.dbm.count(collection=collection)


    def _aggregate(self, collection: str, pipeline, **kwargs):
        """search after query requirements

        Args:
            collection: collection to search
            query: query or aggregate pipe
            *args:
            **kwargs:

        Returns:
            list of found documents
        """
        return self.dbm.aggregate(collection, pipeline=pipeline, **kwargs)


    def _get(self, collection: str, public_id: int) -> dict:
        """get document from the database by their public id

        Args:
            collection (str): name of the database collection
            public_id (int): public id of the document/entry

        Returns:
            str: founded document in json format
        """
        return self.dbm.find_one(collection=collection, public_id=public_id)


    def _get_location(self, collection: str, object_id: int) -> dict:
        """get location document from the database by their object id

        Args:
            collection (str): name of the database collection
            object_id (int): object id of the location document

        Returns:
            str: location document in json format
        """
        return self.dbm.find_one(collection=collection, object_id=object_id)


    def get_location_by_object(self, collection: str, object_id: int) -> dict:
        """get location document from the database by their object id

        Args:
            collection (str): name of the database collection
            object_id (int): object id of the location document

        Returns:
            str: location document in json format
        """
        return self.dbm.find_one_by_object(
            collection=collection,
            object_id=object_id
        )


    def _get_by(self, collection: str, **requirements: dict) -> dict:
        """get document from the database by requirements

        Args:
            collection:
            **requirements:

        Returns:
        """
        requirements_filter = {}

        for k, req in requirements.items():
            requirements_filter.update({k: req})

        return self.dbm.find_one_by(collection=collection, filter=requirements_filter)


    def _get_many(self,
                  collection: str,
                  sort='public_id',
                  direction: int = -1,
                  limit=0,
                  **requirements: dict) -> list[dict]:
        """
        Get all documents from the database which have the passing requirements

        Args:
            collection (str): name of the database collection
            sort (str): sort by given key - default public_id
            **requirements (dict): dictionary of key value requirement
        Returns:
            (list): list of all documents
        """
        requirements_filter = {}
        formatted_sort = [(sort, direction)]

        for k, req in requirements.items():
            requirements_filter.update({k: req})

        return self.dbm.find_all(collection=collection, limit=limit, filter=requirements_filter, sort=formatted_sort)


    def _insert(self, collection: str, data: dict) -> int:
        """insert document/object into database

        Args:
            collection (str): name of the database collection
            data (dict): dictionary of object or the data

        Returns:
            int: new public_id of inserted document
            None: if anything goes wrong
        """
        return self.dbm.insert(collection=collection, data=data)


    def _update(self, collection: str, public_id: int, data: dict) -> object:
        """
        update document/object in database
        Args:
            collection (str): name of the database collection
            public_id (int): public id of object
            data: changed data/object

        Returns:
            acknowledgment of database
        """
        return self.dbm.update(collection=collection, filter={'public_id': public_id}, data=data)


    def _update_for_object(self, collection: str, object_id: int, data: dict) -> object:
        """
        update document/object in database
        Args:
            collection (str): name of the database collection
            public_id (int): public id of object
            data: changed data/object

        Returns:
            acknowledgment of database
        """
        return self.dbm.update(
            collection=collection,
            filter={'object_id': object_id},
            data=data
        )


    def _unset_update_many(self, collection: str, data: str) -> object:
        """
        update document/object in database
        Args:
            collection (str): name of the database collection
            public_id (int): public id of object
            data: field to be deleted

        Returns:
            acknowledgment of database
        """
        return self.dbm.unset_update_many(
            collection=collection,
            filter={},
            data=data
        )


    def _update_many(self, collection: str, query: dict, update: dict):
        """
        update all documents that match the filter from a collection.
        Args:
            collection (str): name of the database collection
            query (dict): A query that matches the documents to update.
            update (dict): The modifications to apply.

        Returns:
            acknowledgment of database
        """
        return self.dbm.update_many(
            collection=collection,
            query=query,
            update=update
        )


    def _delete(self, collection: str, public_id: int):
        """
        delete document/object inside database
        Args:
            collection (str): name of the database collection
            public_id (int): public id of object

        Returns:
            acknowledgment of database
        """
        return self.dbm.delete(
            collection=collection,
            filter={'public_id': public_id}
        ).acknowledged


    def delete_many(self, collection: str, filter_query: dict):
        """
        Removes all documents that match the filter from a collection.
        Args:
            collection (str): name of the database collection
            filter (dict): Specifies deletion criteria using query operators.

        Returns:
            acknowledgment of database
        """
        return self.dbm.delete_many(collection=collection, **filter_query)
