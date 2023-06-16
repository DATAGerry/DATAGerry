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

"""Basic identifiers for the identification of the corresponding importers based on the file type.
The Content-Type entity header is used to indicate the media type of the resource.
"""


class BASEContent:
    """Empty general content type
    Notes:
        Should not be used
    """
    ICON = ''
    CONTENT_TYPE = ''
    FILE_TYPE = ''


class JSONContent(BASEContent):
    """Identifier for JavaScript Object Notation files"""
    ICON = 'fas fa-file-code'
    CONTENT_TYPE = 'application/json'
    FILE_TYPE = 'json'


class CSVContent(BASEContent):
    """Identifier for Comma-Separated Values files"""
    ICON = 'fas fa-file-csv'
    CONTENT_TYPE = 'text/csv'
    FILE_TYPE = 'csv'


class XLSXContent(BASEContent):
    """Identifier for Excel files"""
    ICON = 'fas fa-file-excel'
    CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    FILE_TYPE = 'xlsx'
