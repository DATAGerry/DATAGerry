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


from cmdb.user_management.user_right import BaseRight


class ImportRight(BaseRight):
    MIN_LEVEL = BaseRight.PROTECTED
    PREFIX = '{}.{}'.format(BaseRight.PREFIX, 'import')

    def __init__(self, name: str, level: int = 50, description: str = None):
        super(ImportRight, self).__init__(level, name, description=description)


class ImportObjectRight(ImportRight):
    MIN_LEVEL = BaseRight.PROTECTED
    PREFIX = '{}.{}'.format(ImportRight.PREFIX, 'object')

    def __init__(self, name: str, level: int = 50, description: str = None):
        super(ImportObjectRight, self).__init__(name, level, description=description)


class ImportTypeRight(ImportRight):
    MIN_LEVEL = BaseRight.SECURE
    PREFIX = '{}.{}'.format(ImportRight.PREFIX, 'type')

    def __init__(self, name: str, level: int = 50, description: str = None):
        super(ImportTypeRight, self).__init__(name, level, description=description)
