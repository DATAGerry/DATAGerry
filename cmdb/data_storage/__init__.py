# Net|CMDB - OpenSource Enterprise CMDB
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

from cmdb.data_storage.database_connection import MongoConnector, Connector
from cmdb.data_storage.database_manager import DatabaseManagerMongo, DatabaseManager
from cmdb.data_storage.database_manager import NoDocumentFound


def get_pre_init_database() -> (DatabaseManager, DatabaseManagerMongo):
    """
    Get a database manager with parameters from system config reader
    Returns: DatabaseManager

    """
    from cmdb.data_storage import DatabaseManagerMongo, MongoConnector
    from cmdb.utils.system_reader import SystemConfigReader
    system_config_reader = SystemConfigReader()
    try:
        timeout = system_config_reader.get_value('connection_timeout', 'Database')
    except KeyError:
        timeout = MongoConnector.DEFAULT_CONNECTION_TIMEOUT
    return DatabaseManagerMongo(
        connector=MongoConnector(
            host=system_config_reader.get_value('host', 'Database'),
            port=int(system_config_reader.get_value('port', 'Database')),
            database_name=system_config_reader.get_value('database_name', 'Database'),
            timeout=timeout
        )
    )
