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
from queue import Queue
from flask import Flask

from cmdb.database.database_manager_mongo import DatabaseManagerMongo
# -------------------------------------------------------------------------------------------------------------------- #

class BaseCmdbApp(Flask):
    """TODO: document"""

    def __init__(self, import_name: str,
                 database_manager: DatabaseManagerMongo = None,
                 event_queue: Queue = None):
        self.database_manager: DatabaseManagerMongo = database_manager
        self.event_queue: Queue = event_queue
        self.temp_folder: str = '/tmp/'

        super().__init__(import_name)
