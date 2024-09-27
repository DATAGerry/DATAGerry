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
from enum import IntEnum

from cmdb.errors.security import InvalidLevelRightError, MinLevelRightError, MaxLevelRightError
# -------------------------------------------------------------------------------------------------------------------- #

GLOBAL_RIGHT_IDENTIFIER = '*'

class Levels(IntEnum):
    """
    Class wrapper for different security levels
    """
    CRITICAL = 100
    DANGER = 80
    SECURE = 50
    PROTECTED = 30
    PERMISSION = 10
    NOTSET = 0


_levelToName = {
    Levels.CRITICAL: 'CRITICAL',
    Levels.DANGER: 'DANGER',
    Levels.SECURE: 'SECURE',
    Levels.PROTECTED: 'PROTECTED',
    Levels.PERMISSION: 'PERMISSION',
    Levels.NOTSET: 'NOTSET',
}

_nameToLevel = {
    'CRITICAL': Levels.CRITICAL,
    'DANGER': Levels.DANGER,
    'SECURE': Levels.SECURE,
    'PROTECTED': Levels.PROTECTED,
    'PERMISSION': Levels.PERMISSION,
    'NOTSET': Levels.NOTSET,
}


class BaseRight:
    """TODO: document"""
    MIN_LEVEL = Levels.NOTSET
    MAX_LEVEL = Levels.CRITICAL

    DEFAULT_MASTER: bool = False
    PREFIX: str = 'base'

    __slots__ = '_level', 'name', 'label', 'description', 'is_master'

    def __init__(self, level: Levels, name: str, label: str = None, description: str = None):
        self.level = level
        self.name = f'{self.PREFIX}.{name}'
        self.label = label or f'{self.get_prefix()}.{self.name.split(".")[-1]}'
        self.description = description
        self.is_master = name == GLOBAL_RIGHT_IDENTIFIER


    def get_prefix(self):
        """TODO: document"""
        return self.PREFIX.rsplit('.', maxsplit=1)[-1]


    def get_label(self):
        """TODO: document"""
        return self.label or f'{self.get_prefix()}.{self.name.split(".")[-1]}'


    def __getitem__(self, item):
        return self.__getattribute__(item)


    @classmethod
    def get_levels(cls):
        """TODO: document"""
        return _levelToName


    @property
    def level(self):
        """TODO: document"""
        return self._level


    @level.setter
    def level(self, level):
        if level not in Levels:
            raise InvalidLevelRightError(level)

        if level.value < self.MIN_LEVEL.value:
            raise MinLevelRightError(f"Level was {level}, expected at least {self.MIN_LEVEL}")

        if level.value > self.MAX_LEVEL.value:
            raise MaxLevelRightError(f"Level was {level}, expected at most {self.MAX_LEVEL}")

        self._level = level


    @classmethod
    def to_dict(cls, instance: "BaseRight") -> dict:
        """TODO: document"""
        return {
            'level': instance.level,
            'name': instance.name,
            'label': instance.label,
            'description': instance.description,
            'is_master': instance.is_master
        }
