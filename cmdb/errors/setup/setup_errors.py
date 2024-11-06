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
"""
Contains Setup Error Classes
"""
# -------------------------------------------------------------------------------------------------------------------- #

class SetupError(Exception):
    """
    Base Setup Error
    """
    def __init__(self, message: str):
        super().__init__(message)

# --------------------------------------------------- SETUP ERRORS --------------------------------------------------- #

class CollectionInitError(SetupError):
    """
    Raised when Datagerry could not initialise the database collection
    """
    def __init__(self, err: str):
        self.message = f"CollectionInitError: {err}"
        super().__init__(self.message)
