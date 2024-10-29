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
# -------------------------------------------------------------------------------------------------------------------- #

class BaseImporterResponse:
    """Base response after import action"""

    def __init__(self, message: str):
        self.message: str = message

#CLASS-FIX
class ImporterObjectResponse(BaseImporterResponse):
    """Response of an bulk object import"""

    def __init__(self, message: str, success_imports: list = None, failed_imports: list = None):
        self.success_imports: list[ImportSuccessMessage] = success_imports or []
        self.failed_imports: list[ImportFailedMessage] = failed_imports or []
        super().__init__(message=message)

#CLASS-FIX
class ImportMessage:
    """Simple class wrapper for json encoding"""

    def __init__(self, obj: dict = None):
        self.obj = obj


class ImportSuccessMessage(ImportMessage):
    """Message wrapper for successfully imported objects"""

    def __init__(self, public_id: int, obj: dict = None):
        """Init message
        Args:
            public_id: ID of the new object
            obj (optional): cmdb object instance
        """
        self.public_id = public_id
        super().__init__(obj=obj)


class ImportFailedMessage(ImportMessage):
    """Message wrapper for failed imported objects"""

    def __init__(self, error_message: str, obj: dict = None):
        """Init message
        Args:
            error_message: reason why it failed - exception error or something
            obj (optional): failed dict
        """
        self.error_message = error_message
        super().__init__(obj=obj)
