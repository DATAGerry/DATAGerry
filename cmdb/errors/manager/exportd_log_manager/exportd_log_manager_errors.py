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
"""
This module contains the classes of all ExportdLogManager errors
"""
from cmdb.errors.cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class ExportdLogManagerError(CMDBError):
    """
    Base ExportdLogManager error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# ----------------------------------------------- ObjectManager Errors ----------------------------------------------- #

class ExportdLogManagerDeleteError(ExportdLogManagerError):
    """
    Raised when ExportdLogManager could not delete a ExportdLog
    """
    def __init__(self, err: str):
        self.message = f"ExportdLog could not be deleted. Error: {err}"
        super().__init__(self.message)


class ExportdLogManagerInsertError(ExportdLogManagerError):
    """
    Raised when ExportdLogManager could not create a ExportdLog
    """
    def __init__(self, err: str):
        self.message = f"ExportdLog could not be created. Error: {err}"
        super().__init__(self.message)

#TODO: ERROR-FIX (never used)
class ExportdLogManagerGetError(ExportdLogManagerError):
    """
    Raised when ExportdLogManager could not retrieve a ExportdLog
    """
    def __init__(self, err: str):
        self.message = f"ExportdLog could not be retrieved. Error: {err}"
        super().__init__(self.message)
