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
Contains Config File Error Classes
"""
from ..cmdb_error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class ConfigFileError(CMDBError):
    """
    Base ConfigFile Error
    """
    def __init__(self, message: str):
        super().__init__(message)

# ------------------------------------------------ CONFIG FILE ERRORS ------------------------------------------------ #

#ERROR-FIX (not used)
class ConfigFileSetError(ConfigFileError):
    """
    Error if code tries to set values or sections while a config file is loaded
    """
    def __init__(self, filename: str):
        self.message = f"Config file: {filename} was loaded. No manual editing of values are allowed!"
        super().__init__(self.message)


class ConfigFileNotFound(ConfigFileError):
    """
    Error if local file could not be loaded
    """
    def __init__(self, filename: str):
        self.message = f"Config file: {filename} was not found!"
        super().__init__(self.message)


class ConfigNotLoaded(ConfigFileError):
    """
    Error if reader is not loaded
    """
    def __init__(self, filename: str):
        self.message = f"Config file: {filename} was not loaded correctly!"
        super().__init__(self.message)


class SectionError(ConfigFileError):
    """
    Error if section does not exist
    """
    def __init__(self, name: str):
        self.message = f"The section '{name}' does not exist!"
        super().__init__(self.message)


#ERROR-FIX (not used)
class KeySectionError(ConfigFileError):
    """
    Error if key does not exist in section
    """
    def __init__(self, name: str):
        self.message = f"The key '{name}' was not found!"
        super().__init__(self.message)
