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


class BaseImporterResponse:
    """Base response after import action"""

    def __init__(self, message: str):
        self.message: str = message


class ImporterObjectResponse(BaseImporterResponse):
    """Response of an bulk object import"""

    def __init__(self, message: str, success_imports: list = None, failed_imports: list = None):
        self.success_imports: list = success_imports or []
        self.failed_imports: list = failed_imports or []
        super(ImporterObjectResponse, self).__init__(message=message)
