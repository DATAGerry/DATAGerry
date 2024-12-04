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
from cmdb.framework.importer.configs.base_importer_config import BaseImporterConfig
# -------------------------------------------------------------------------------------------------------------------- #

class ObjectImporterConfig(BaseImporterConfig):
    """TODO: document"""

    def __init__(self, type_id: int, mapping: list = None, start_element: int = 0, max_elements: int = 0,
                 overwrite_public: bool = True, *args, **kwargs):
        self.type_id: int = type_id
        self.start_element: int = start_element
        self.max_elements: int = max_elements
        self.overwrite_public: bool = overwrite_public
        super().__init__(mapping=mapping)


    def get_type_id(self):
        """TODO: document"""
        return self.type_id
