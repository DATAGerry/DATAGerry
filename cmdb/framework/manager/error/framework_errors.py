# DATAGERRY - OpenSource Enterprise CMDB
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from cmdb.framework.manager import ManagerGetError, ManagerInsertError, ManagerUpdateError, ManagerDeleteError


class FrameworkGetError(ManagerGetError):
    """Generic or basic framework error for manager get operations."""

    def __init__(self, err: Exception = None):
        super(FrameworkGetError, self).__init__(err=err)


class FrameworkInsertError(ManagerInsertError):
    """Generic or basic framework error for manager insert operations."""

    def __init__(self, err: Exception = None):
        super(FrameworkInsertError, self).__init__(err=err)


class FrameworkUpdateError(ManagerUpdateError):
    """Generic or basic framework error for manager update operations."""

    def __init__(self, err: Exception = None):
        super(FrameworkUpdateError, self).__init__(err=err)


class FrameworkDeleteError(ManagerDeleteError):
    """Generic or basic framework error for manager delete operations."""

    def __init__(self, err: Exception = None):
        super(FrameworkDeleteError, self).__init__(err=err)


class FrameworkNotFoundError(FrameworkGetError):
    """Framework error if no resource was found."""

    def __init__(self, message):
        self.message = message
        super(FrameworkNotFoundError, self).__init__()


class FrameworkQueryEmptyError(FrameworkGetError):
    """Error if a requested query has no results."""

    def __init__(self, message):
        self.message = message
        super(FrameworkQueryEmptyError, self).__init__()


class FrameworkIterationError(FrameworkGetError):
    """Framework error if the iteration over the collection throws an error"""

    def __init__(self, err: Exception = None):
        super(FrameworkIterationError, self).__init__(err=err)


class FrameworkIterationOutOfBoundsError(FrameworkGetError):
    """Framework error if a skip bigger than the total number of elements was called"""

    def __init__(self, message: str = '', err: Exception = None):
        self.message = message
        super(FrameworkIterationOutOfBoundsError, self).__init__(err=err)
