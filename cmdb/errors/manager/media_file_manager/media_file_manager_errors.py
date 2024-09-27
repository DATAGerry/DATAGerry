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
This module contains the classes of all MediaFileManager errors
"""
from cmdb.errors.cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class MediaFileManagerError(CMDBError):
    """
    Base MediaFileManagerError error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# ----------------------------------------------- ObjectManager Errors ----------------------------------------------- #

class MediaFileManagerGetError(MediaFileManagerError):
    """
    Raised when MediaFileManager could not retrieve a file
    """
    def __init__(self, err: str):
        self.message = f"File could not be retrieved. Error: {err}"
        super().__init__(self.message)


class MediaFileManagerInsertError(MediaFileManagerError):
    """
    Raised when MediaFileManager could not create a file
    """
    def __init__(self, err: str):
        self.message = f"File could not be created. Error: {err}"
        super().__init__(self.message)


class MediaFileManagerUpdateError(MediaFileManagerError):
    """
    Raised when MediaFileManager could not update a file
    """
    def __init__(self, err: str):
        self.message = f"File could not be updated. Error: {err}"
        super().__init__(self.message)


class MediaFileManagerDeleteError(MediaFileManagerError):
    """
    Raised when MediaFileManager could not delete a file
    """
    def __init__(self, err: str):
        self.message = f"File could not be deleted. Error: {err}"
        super().__init__(self.message)
