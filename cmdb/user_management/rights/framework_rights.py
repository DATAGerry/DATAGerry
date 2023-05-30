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

from cmdb.user_management.models.right import BaseRight, Levels


class FrameworkRight(BaseRight):
    MIN_LEVEL = Levels.PERMISSION
    PREFIX = '{}.{}'.format(BaseRight.PREFIX, 'framework')

    def __init__(self, name: str, level: Levels = MIN_LEVEL, description: str = None):
        super(FrameworkRight, self).__init__(level, name, description=description)


class ObjectRight(FrameworkRight):
    MIN_LEVEL = Levels.PERMISSION
    MAX_LEVEL = Levels.SECURE
    PREFIX = '{}.{}'.format(FrameworkRight.PREFIX, 'object')

    def __init__(self, name: str, level: Levels = MIN_LEVEL, description: str = None):
        super(ObjectRight, self).__init__(name, level, description=description)


class TypeRight(FrameworkRight):
    MIN_LEVEL = Levels.PROTECTED
    MAX_LEVEL = Levels.CRITICAL
    PREFIX = '{}.{}'.format(FrameworkRight.PREFIX, 'type')

    def __init__(self, name: str, level: Levels = Levels.SECURE, description: str = None):
        super(TypeRight, self).__init__(name, level, description=description)


class CategoryRight(FrameworkRight):
    MIN_LEVEL = Levels.PROTECTED
    MAX_LEVEL = Levels.SECURE
    PREFIX = '{}.{}'.format(FrameworkRight.PREFIX, 'category')

    def __init__(self, name: str, level: Levels = Levels.PROTECTED, description: str = None):
        super(CategoryRight, self).__init__(name, level, description=description)


class LogRight(FrameworkRight):
    MIN_LEVEL = Levels.PROTECTED
    MAX_LEVEL = Levels.DANGER
    PREFIX = '{}.{}'.format(FrameworkRight.PREFIX, 'log')

    def __init__(self, name: str, level: Levels = Levels.PROTECTED, description: str = None):
        super(LogRight, self).__init__(name, level, description=description)
