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
"""Manages database connection status"""

# -------------------------------------------------------------------------------------------------------------------- #

class ConnectionStatus:
    """Class representing the status of connection to database"""

    def __init__(self, connected: bool, message: str = 'No message given'):
        self.connected: bool = connected
        self.message: str = message


    def get_status(self) -> bool:
        """Returns the connected status"""
        return self.connected
