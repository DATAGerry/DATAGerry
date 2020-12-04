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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from typing import Any

from cmdb.database.database_manager import DatabaseManagerMongo
from cmdb.framework.utils import Collection, PublicID

from .errors import ManagerGetError, ManagerInsertError, ManagerUpdateError, ManagerDeleteError, ManagerIterationError


class ManagerBase:
    """
    Manager base class for all core CRUD function.
    Will be replacing `CmdbManagerBase` in the future.
    """

    def __init__(self, database_manager: DatabaseManagerMongo):
        """
        Init/Open the database connection.

        Args:
            database_manager: Database managers instance
        """
        self._database_manager: DatabaseManagerMongo = database_manager

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Auto disconnect the database connection when the Manager get destroyed."""
        self._database_manager.connector.disconnect()

    def _aggregate(self, collection: Collection, *args, **kwargs):
        """
        Calls mongodb aggregation
        Args:
            collection: Name of the collection
            *args:
            **kwargs:

        Returns:
            - A :class:`~pymongo.command_cursor.CommandCursor` over the result set.
        """
        try:
            return self._database_manager.aggregate(collection, *args, **kwargs)
        except Exception as err:
            raise ManagerIterationError(err)

    def _get(self, collection: Collection, filter=None, *args, **kwargs):
        """
        Calls mongodb find operation
        Args:
            collection: Name of the collection
            filter: Match dictionary
            *args:
            **kwargs:

        Returns:
            - A :class:`~pymongo.command_cursor.CommandCursor` over the result set.
        """
        try:
            return self._database_manager.find(collection, filter=filter, *args, **kwargs)
        except Exception as err:
            raise ManagerGetError(err)

    def _insert(self, collection: Collection, resource: Any, skip_public: bool = False):
        """
        Calls mongodb insert operation
        Args:
            collection (Collection): Name of the collection
            resource (Any): Insert data (normally a dict)
            skip_public (bool): Skip the public id creation and counter increment.
        """
        try:
            return self._database_manager.insert(collection, data=resource, skip_public=skip_public)
        except Exception as err:
            raise ManagerInsertError(err)

    def _update(self, collection: Collection, filter: dict, resource: Any, *args, **kwargs):
        """
        Calls a mongodb update operation
        Args:
            collection (Collection): Name of the collection
            filter (dict): Match dictionary
            resource: Update data (normally a dict)

        Returns:
            - An instance of :class:`~pymongo.results.UpdateResult`.
        """
        try:
            return self._database_manager.update(collection, filter=filter, data=resource, *args, **kwargs)
        except Exception as err:
            raise ManagerUpdateError(err)

    def _delete(self, collection: Collection, filter: dict, *args, **kwargs):
        """
        Calls a mongodb delete operation
        Args:
            collection: Name of the collection
            filter: Matching resource dict.
        """
        try:
            return self._database_manager.delete(collection, filter=filter, *args, **kwargs)
        except Exception as err:
            raise ManagerDeleteError(err)
