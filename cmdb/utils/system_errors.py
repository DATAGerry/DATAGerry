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

from cmdb.utils.error import CMDBError


class ConfigFileSetError(CMDBError):
    """
    Error if code tries to set values or sections while a config file is loaded
    """

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.message = 'Configurations file: ' + self.filename + ' was loaded. No manual editing of values are allowed!'


class ConfigFileNotFound(CMDBError):
    """
    Error if local file could not be loaded
    """

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.message = 'Configurations file: ' + self.filename + ' was not found!'


class ConfigNotLoaded(CMDBError):
    """
    Error if reader is not loaded
    """

    def __init__(self, filename):
        super().__init__()
        self.message = 'Configurations file: ' + filename + ' was not loaded correctly!'


class SectionError(CMDBError):
    """
    Error if section not exists
    """

    def __init__(self, name):
        super().__init__()
        self.message = 'The section ' + name + ' does not exist!'


class KeySectionError(CMDBError):
    """
    Error if key not exists in section
    """

    def __init__(self, name):
        super().__init__()
        self.message = 'The key ' + name + ' was not found!'