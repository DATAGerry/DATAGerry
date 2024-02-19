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
"""TODO: document"""
from typing import Union

from cmdb.errors.manager import ManagerGetError, ManagerDeleteError
# -------------------------------------------------------------------------------------------------------------------- #

class FrameworkGetError(ManagerGetError):
    """Generic or basic framework error for managers get operations."""

    def __init__(self, err: Union[Exception, str] = None):
        super().__init__(err=err)


class FrameworkDeleteError(ManagerDeleteError):
    """Generic or basic framework error for managers delete operations."""

    def __init__(self, err: Union[Exception, str] = None):
        super().__init__(err=err)


class FrameworkIterationError(FrameworkGetError):
    """Framework error if the iteration over the collection throws an error"""

    def __init__(self, err: Union[Exception, str] = None):
        super().__init__(err=err)
