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

"""Manager error collections"""

from cmdb.utils.error import CMDBError


class ManagerGetError(CMDBError):
    """Manager exception for get operations"""

    def __init__(self, err=None):
        self.message = f'Error while GET operation - E: {err}'


class ManagerInsertError(CMDBError):
    """Manager exception for insert operations"""

    def __init__(self, err=None):
        self.message = f'Error while INSERT operation - E: {err}'


class ManagerUpdateError(CMDBError):
    """Manager exception for update operations"""

    def __init__(self, err=None):
        self.message = f'Error while UPDATE operation - E: {err}'


class ManagerDeleteError(CMDBError):
    """Manager exception for delete operations"""

    def __init__(self, err=None):
        self.message = f'Error while DELETE operation - E: {err}'
