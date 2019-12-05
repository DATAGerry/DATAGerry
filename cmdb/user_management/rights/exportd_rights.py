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


class ExportdRight(BaseRight):
    MIN_LEVEL = BaseRight.PROTECTED
    PREFIX = '{}.{}'.format(BaseRight.PREFIX, 'exportd')

    def __init__(self, name: str, level: int = 50, description: str = None):
        super(ExportdRight, self).__init__(level, name, description=description)


class ExportdJobRight(ExportdRight):
    MIN_LEVEL = BaseRight.PROTECTED
    PREFIX = '{}.{}'.format(ExportdRight.PREFIX, 'job')

    def __init__(self, name: str, level: int = 50, description: str = None):
        super(ExportdJobRight, self).__init__(name, level, description=description)


class ExportdLogRight(ExportdRight):
    MIN_LEVEL = BaseRight.PROTECTED
    MAX_LEVEL = BaseRight.DANGER
    PREFIX = '{}.{}'.format(ExportdRight.PREFIX, 'log')

    def __init__(self, name: str, level: int = BaseRight.PROTECTED, description: str = None):
        super(ExportdLogRight, self).__init__(name, level, description=description)
