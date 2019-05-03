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

from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils.system_writer import SystemSettingsWriter
from cmdb.utils.security import SecurityManager


def get_security_manager(database_manager) -> SecurityManager:
    """
    get a instance of the security manager
    Args:
        database_manager (DatabaseManager): instance of the database manager

    Returns:
        (SecurityManager): instance of SecurityManager
    """
    return SecurityManager(database_manager)


def get_system_settings_writer(database_manager) -> SystemSettingsWriter:
    """
    get a instance of the database settings writer
    Args:
        database_manager (DatabaseManager): instance of the database manager

    Returns:
        (SystemSettingsWriter): instance of SystemSettingsWriter
    """
    return SystemSettingsWriter(
        database_manager=database_manager
    )


def get_system_settings_reader(database_manager) -> SystemSettingsReader:
    """
    get a instance of the database settings reader
    Args:
        database_manager (DatabaseManager): instance of the database manager

    Returns:
        (SystemSettingsReader): instance of SystemSettingsReader
    """
    return SystemSettingsReader(
        database_manager=database_manager
    )
