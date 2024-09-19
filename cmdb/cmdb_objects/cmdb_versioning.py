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
"""Module for versioning objects and types"""
import logging

from cmdb.errors.cmdb_object import VersionTypeError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  Versioning - CLASS                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
class Versioning:
    """Helper class for object/type versioning"""

    def __init__(self, major: int = 1, minor: int = 0, patch: int = 0):
        """
        Args:
            major: core changes with no compatibility
            minor: code changes
            patch: little fixes
        """
        self.major = major
        self.minor = minor
        self.patch = patch


    @property
    def major(self):
        """TODO: document"""
        return self._major


    @property
    def minor(self):
        """TODO: document"""
        return self._minor


    @property
    def patch(self):
        """TODO: document"""
        return self._patch


    @major.setter
    def major(self, value):
        if not isinstance(value, int):
            raise VersionTypeError('major', str(value))
        self._major = value


    @minor.setter
    def minor(self, value):
        if not isinstance(value, int):
            raise VersionTypeError('major', str(value))
        self._minor = value


    @patch.setter
    def patch(self, value):
        if not isinstance(value, int):
            raise VersionTypeError('major', str(value))
        self._patch = value


    def update_major(self) -> int:
        """TODO: document"""
        self.major += 1
        return self.major


    def update_minor(self) -> int:
        """TODO: document"""
        self.minor += 1
        return self.minor


    def update_patch(self) -> int:
        """TODO: document"""
        self.patch += 1
        return self.patch


    def __repr__(self):
        return f'{self.major}.{self.minor}.{self.patch}'
