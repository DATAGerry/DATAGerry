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
from cmdb.framework.importer.mapper.mapping import Mapping
# -------------------------------------------------------------------------------------------------------------------- #

class BaseImporterConfig:
    """TODO: document"""

    DEFAULT_MAPPING: Mapping = Mapping()
    MANUALLY_MAPPING: bool = True

    def __init__(self, mapping: list = None):
        if mapping:
            mapping = Mapping.generate_mapping_from_list(mapping)
        self.mapping: Mapping = mapping or self.DEFAULT_MAPPING


    def get_mapping(self) -> Mapping:
        """TODO: document"""
        return self.mapping
