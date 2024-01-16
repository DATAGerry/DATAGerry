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
"""TODO: document"""
from cmdb.user_management.models.right import BaseRight, Levels
# -------------------------------------------------------------------------------------------------------------------- #

class FrameworkRight(BaseRight):
    """TODO: document"""
    MIN_LEVEL = Levels.PERMISSION
    PREFIX = f'{BaseRight.PREFIX}.framework'

    def __init__(self, name: str, level: Levels = MIN_LEVEL, description: str = None):
        super().__init__(level, name, description=description)


class ObjectRight(FrameworkRight):
    """TODO: document"""
    MIN_LEVEL = Levels.PERMISSION
    MAX_LEVEL = Levels.SECURE
    PREFIX = f'{FrameworkRight.PREFIX}.object'

    def __init__(self, name: str, level: Levels = MIN_LEVEL, description: str = None):
        super().__init__(name, level, description=description)


class SectionTemplateRight(FrameworkRight):
    """TODO: document"""
    MIN_LEVEL = Levels.PERMISSION
    MAX_LEVEL = Levels.SECURE
    PREFIX = f'{FrameworkRight.PREFIX}.sectionTemplate'

    def __init__(self, name: str, level: Levels = MIN_LEVEL, description: str = None):
        super().__init__(name, level, description=description)

class TypeRight(FrameworkRight):
    """TODO: document"""
    MIN_LEVEL = Levels.PROTECTED
    MAX_LEVEL = Levels.CRITICAL
    PREFIX = f'{FrameworkRight.PREFIX}.type'

    def __init__(self, name: str, level: Levels = Levels.SECURE, description: str = None):
        super().__init__(name, level, description=description)


class CategoryRight(FrameworkRight):
    """TODO: document"""
    MIN_LEVEL = Levels.PROTECTED
    MAX_LEVEL = Levels.SECURE
    PREFIX = f'{FrameworkRight.PREFIX}.category'

    def __init__(self, name: str, level: Levels = Levels.PROTECTED, description: str = None):
        super().__init__(name, level, description=description)


class LogRight(FrameworkRight):
    """TODO: document"""
    MIN_LEVEL = Levels.PROTECTED
    MAX_LEVEL = Levels.DANGER
    PREFIX = f'{FrameworkRight.PREFIX}.log'

    def __init__(self, name: str, level: Levels = Levels.PROTECTED, description: str = None):
        super().__init__(name, level, description=description)
