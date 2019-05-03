# Net|CMDB - OpenSource Enterprise CMDB
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from cmdb.user_management.user_right import BaseRight


class SystemRight(BaseRight):
    MIN_LEVEL = BaseRight.SECURE
    PREFIX = '{}.{}'.format(BaseRight.PREFIX, 'system')

    def __init__(self, name: str, level: int = 50, description: str = None):
        super(SystemRight, self).__init__(level, name, description=description)


class ManagementRight(SystemRight):
    MIN_LEVEL = BaseRight.SECURE
    MAX_LEVEL = BaseRight.DANGER
    PREFIX = '{}.{}'.format(SystemRight.PREFIX, 'management')

    def __init__(self, name: str, level: int = MIN_LEVEL, description: str = None):
        super(ManagementRight, self).__init__(name, level, description=description)


class UserRight(ManagementRight):
    MIN_LEVEL = BaseRight.SECURE
    MAX_LEVEL = BaseRight.DANGER
    PREFIX = '{}.{}'.format(ManagementRight.PREFIX, 'user')

    def __init__(self, name: str, level: int = MIN_LEVEL, description: str = None):
        super(UserRight, self).__init__(name, level, description=description)


class GroupRight(ManagementRight):
    MIN_LEVEL = BaseRight.SECURE
    MAX_LEVEL = BaseRight.DANGER
    PREFIX = '{}.{}'.format(ManagementRight.PREFIX, 'group')

    def __init__(self, name: str, level: int = MIN_LEVEL, description: str = None):
        super(GroupRight, self).__init__(name, level, description=description)
