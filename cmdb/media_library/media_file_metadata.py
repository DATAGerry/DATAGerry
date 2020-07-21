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

from bson import objectid


class FileMetadata:
    def __init__(self, author_id, permissions=None, reference=None, reference_type=None,
                 folder: bool = False, mime_type="application/json"):
        self.reference = reference
        self.reference_type = reference_type
        self.mime_type = mime_type
        self.author_id = author_id
        self.folder = folder
        self.permission = permissions

    def get_ref_to(self) -> objectid:
        if self.reference is None:
            return None
        return self.reference

    def get_ref_to_type(self) -> str:
        if self.reference_type is None:
            return ""
        return self.reference_type

    def get_mime_type(self) -> str:
        if self.mime_type is None:
            return "application/json"
        return self.mime_type

    def get_permission(self):
        # TODO implement this method later
        #  The action of officially allowing someone to do a particular thing

        if self.permission is None:
            return None
        return self.permission
