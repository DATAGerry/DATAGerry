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
Contains Importer Error Classes
"""
# -------------------------------------------------------------------------------------------------------------------- #

class ImporterError(Exception):
    """
    Base Importer Error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# --------------------------------------------------- RENDER ERRORS -------------------------------------------------- #

class ImportRuntimeError(ImporterError):
    """
    Raised when an errors occurs during import
    """
    def __init__(self, err: str):
        self.message = f"An error occured during import. Error: {err}"
        super().__init__(self.message)


class ParserRuntimeError(ImporterError):
    """
    Raised when an errors occures during parsing files
    """
    def __init__(self, err: str):
        self.message = f"Error while parsing. Error: {err}"
        super().__init__(self.message)


class ImporterLoadError(ImporterError):
    """
    Raised when an error occurs loading the importer
    """
    def __init__(self, err: str):
        self.message = f"Could not load importer. Error: {err}"
        super().__init__(self.message)


class ParserLoadError(ImporterError):
    """
    Raised when an error occurs loading the parser
    """
    def __init__(self, err: str):
        self.message = f"Could not load parser. Error: {err}"
        super().__init__(self.message)
