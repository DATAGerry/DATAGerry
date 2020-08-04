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

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.framework.utils import Collection, PublicID


class ManagerBase:
    """New manager base class"""

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.__database_manager: DatabaseManagerMongo = database_manager

    def __aggregate(self, collection: Collection, *args, **kwargs):
        return self.__database_manager.aggregate(collection, *args, **kwargs)

    def _get(self, collection: Collection, filter=None, *args, **kwargs):
        return self.__database_manager.find(collection, filter=filter, *args, **kwargs)

    def _insert(self, collection: Collection, data):
        return self.__database_manager.insert(collection, data=data)

    def _update(self, collection: Collection, filter, data, *args, **kwargs):
        return self.__database_manager.update(collection, filter=filter, data=data, *args, **kwargs)

    def _delete(self, collection: Collection, public_id: PublicID):
        return self.__database_manager.delete(collection, public_id=public_id)
