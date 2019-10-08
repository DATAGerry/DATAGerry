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

from cmdb.framework import CmdbType


class BaseImporterConfig:

    def __init__(self, mapping: dict):
        self.mapping: dict = mapping


class ObjectImporterConfig(BaseImporterConfig):

    def __init__(self, type_instance: CmdbType, mapping: dict, start_element: int = 0, max_elements: int = 0,
                 overwrite_public: bool = True):
        self.type_instance: CmdbType = type_instance
        self.start_element: int = start_element
        self.max_elements: int = max_elements
        self.overwrite_public: bool = overwrite_public
        super(ObjectImporterConfig, self).__init__(mapping=mapping)
