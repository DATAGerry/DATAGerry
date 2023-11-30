# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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


class DateSettingsDAO:
    """Regional Date Settings"""

    __DOCUMENT_IDENTIFIER = 'date'
    __DEFAULT_SETTINGS__ = {
            'date_format': 'YYYY-MM-DDThh:mm:ssZ',
            'timezone': 'UTC',
        }

    def __init__(self, date_format: str, timezone: str):
        self._id: str = DateSettingsDAO.__DOCUMENT_IDENTIFIER
        self.date_format = date_format
        self.timezone = timezone



    def get_id(self) -> str:
        """Get the database document identifier"""
        return self._id



    def get_format(self) -> str:
        """Get the current date format"""
        return self.date_format



    def get_timezone(self) -> str:
        """ Get the current timezone"""
        return self.timezone
