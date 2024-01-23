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
"""TODO: comment"""
from cmdb.database.errors import DataBaseError
# -------------------------------------------------------------------------------------------------------------------- #

class DatabaseConnectionError(DataBaseError):
    """
    Error if connection to database broke up
    """
    def __init__(self, message):
        super().__init__(f'Connection error - No connection with the database: {message}')


class ServerTimeoutError(DataBaseError):
    """
    Server timeout error if connection is lost
    """
    def __init__(self, host):
        super().__init__(f'Server Timeout - No connection to database at {host}')
