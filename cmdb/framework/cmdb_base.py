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
from cmdb.utils.error import CMDBError

try:
    from cmdb.data_storage import DatabaseManagerMongo
except ImportError:
    DatabaseManagerMongo = object


class CmdbManagerBase:
    """Represents the base class for object managers. A respective implementation is always adapted to the
       respective database manager :class:`cmdb.data_storage.DatabaseManager` or the used functionalities.
       But should always use at least the super functions listed here.
    """

    def __init__(self, database_manager: DatabaseManagerMongo):
        """Example:
            Depending on the condition or whether a fork process is used, the database manager can also be seen
            directly in the declaration of the object manager

        Args:
            database_manager (DatabaseManager): initialisation of an database manager

        """
        if database_manager:
            self.dbm: DatabaseManagerMongo = database_manager

    def _get(self, collection: str, public_id: int) -> dict:
        """get document from the database by their public id

        Args:
            collection (str): name of the database collection
            public_id (int): public id of the document/entry

        Returns:
            str: founded document in json format
        """
        return self.dbm.find_one(
            collection=collection,
            public_id=public_id
        )

    def _get_all(self, collection: str, sort='public_id', limit=0, **requirements: dict) -> list:
        """get all documents from the database which have the passing requirements

        Args:
            collection (str): name of the database collection
            sort (str): sort by given key - default public_id
            **requirements (dict): dictionary of key value requirement

        Returns:
            list: list of all documents

        """
        requirements_filter = {}
        formatted_sort = [(sort, self.dbm.DESCENDING)]
        for k, req in requirements.items():
            requirements_filter.update({k: req})
        return self.dbm.find_all(collection=collection, limit=limit, filter=requirements_filter, sort=formatted_sort)

    def _insert(self, collection: str, data: dict) -> (int, None):
        """insert document/object into database

        Args:
            collection (str): name of the database collection
            data (dict): dictionary of object or the data

        Returns:
            int: new public_id of inserted document
            None: if anything goes wrong

        """
        return self.dbm.insert(
            collection=collection,
            data=data
        )

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
        return self.dbm.update(
            collection=collection,
            public_id=public_id,
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
            public_id=public_id
        ).acknowledged

    def _delete_many(self, collection: str, filter_query: dict):
        """
        removes all documents that match the filter from a collection.
        Args:
            collection (str): name of the database collection
            filter (dict): Specifies deletion criteria using query operators.

        Returns:
            acknowledgment of database
        """
        return self.dbm.delete_many(
            collection=collection,
            **filter_query
        )

    def _search(self, collection: str, requirements, limit=0):
        return self._get_all(collection, limit=limit, **requirements)


class ManagerGetError(CMDBError):

    def __init__(self, err):
        self.message = f'Error while GET operation - E: ${err}'


class ManagerInsertError(CMDBError):

    def __init__(self, err):
        self.message = f'Error while INSERT operation - E: ${err}'


class ManagerUpdateError(CMDBError):

    def __init__(self, err):
        self.message = f'Error while UPDATE operation - E: ${err}'


class ManagerDeleteError(CMDBError):

    def __init__(self, err):
        self.message = f'Error while DELETE operation - E: ${err}'