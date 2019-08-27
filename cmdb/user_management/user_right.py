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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from cmdb.utils.error import CMDBError

LOGGER = logging.getLogger(__name__)

GLOBAL_IDENTIFIER = '*'


class BaseRight:

    CRITICAL = 100
    DANGER = 80
    SECURE = 50
    PROTECTED = 30
    PERMISSION = 10
    NOTSET = 0

    MIN_LEVEL = NOTSET
    MAX_LEVEL = CRITICAL

    _MASTER = False

    PREFIX = 'base'

    _levelToName = {
        CRITICAL: 'CRITICAL',
        DANGER: 'DANGER',
        SECURE: 'SECURE',
        PROTECTED: 'PROTECTED',
        PERMISSION: 'PERMISSION',
        NOTSET: 'NOTSET',
    }

    _nameToLevel = {
        'CRITICAL': CRITICAL,
        'DANGER': DANGER,
        'SECURE': SECURE,
        'PROTECTED': PROTECTED,
        'PERMISSION': PERMISSION,
        'NOTSET': NOTSET,
    }

    def __init__(self, level: int, name: str, label: str = None, description: str = None):
        self.level = level
        self.name = '{}.{}'.format(self.PREFIX, name)
        self.label = label or f'{self.get_prefix()}.{self.name.split(".")[-1]}'
        self.description = description or "No description"
        if name == GLOBAL_IDENTIFIER:
            self._MASTER = True

    def __new__(cls, *args, **kwargs):
        cls._MASTER = cls._MASTER
        return super(BaseRight, cls).__new__(cls)

    def get_prefix(self):
        return self.PREFIX.split('.')[-1]

    def get_name(self):
        return self.name

    def get_label(self):
        return self.label or f'{self.get_prefix()}.{self.name.split(".")[-1]}'

    def get_description(self):
        return self.description

    def is_master(self):
        return self._MASTER

    @classmethod
    def get_levels(cls):
        return cls._levelToName

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if value not in BaseRight._levelToName:
            raise InvalidLevelRightError(value)
        if value < self.MIN_LEVEL:
            raise PoorlyLevelRightError(value, self.MIN_LEVEL)
        if value > self.MAX_LEVEL:
            raise MaxLevelRightError(value, self.MAX_LEVEL)
        self._level = value

    def get_level(self):
        return self.level

    def get_level_name(self):
        return BaseRight._levelToName[self.level]

    def __repr__(self):
        from cmdb.utils.helpers import debug_print
        return debug_print(self)


class InvalidLevelRightError(CMDBError):
    def __init__(self, level):
        super().__init__()
        self.message = 'Invalid right level - Level {} does not exist.'.format(level)


class PoorlyLevelRightError(CMDBError):
    def __init__(self, level, min_level):
        super().__init__()
        self.message = 'The minimum level for the right has been violated. Level was {0}, expected at least {1}'.format(
            level, min_level)


class MaxLevelRightError(CMDBError):
    def __init__(self, level, max_level):
        super().__init__()
        self.message = 'The maximum level for the right has been violated. Level was {0}, expected at most {1}'.format(
            level, max_level)


class NoParentPrefixError(CMDBError):
    def __init__(self):
        super().__init__()
        self.message = 'Right dont has a parent prefix.'
