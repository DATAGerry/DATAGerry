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
Contains DATAerry Assistant Error Classes
"""
# -------------------------------------------------------------------------------------------------------------------- #

class AssistantError(Exception):
    """Base DocAPI Error"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# --------------------------------------------------- DOCAPI ERRORS -------------------------------------------------- #

class ProfileCreationError(AssistantError):
    """
    Error raised when a profile could not be created
    """
    def __init__(self, err: str):
        self.message = f"ProfileCreationError: {err}"
        super().__init__(self.message)
