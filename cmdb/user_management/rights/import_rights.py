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

class ImportRight(BaseRight):
    """TODO: document"""
    MIN_LEVEL = Levels.PROTECTED
    PREFIX = f'{BaseRight.PREFIX}.import'

    def __init__(self, name: str, level: Levels = Levels.SECURE, description: str = None):
        super().__init__(level, name, description=description)



class ImportObjectRight(ImportRight):
    """TODO: document"""
    MIN_LEVEL = Levels.PROTECTED
    PREFIX = f'{ImportRight.PREFIX}.object'

    def __init__(self, name: str, level: Levels = Levels.SECURE, description: str = None):
        super().__init__(name, level, description=description)



class ImportTypeRight(ImportRight):
    """TODO: document"""
    MIN_LEVEL = Levels.SECURE
    PREFIX = f'{ImportRight.PREFIX}.type'

    def __init__(self, name: str, level: Levels = Levels.SECURE, description: str = None):
        super().__init__(name, level, description=description)
