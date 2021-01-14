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


from enum import Enum


class ExporterConfigType(Enum):
    """
        Type of exported data (TYPE = CmdbType, OBJECT = CmdbObject, RENDER = RenderResult)
    """
    TYPE = 1
    OBJECT = 2
    RENDER = 3

    def __str__(self):
        return self.name


class BaseExporterConfig:

    def __init__(self, config_type: ExporterConfigType):
        """
        Args:
            config_type: Type of exported data (CmdbType = type, CmdbObject = object, RenderResult = render)
        """
        self.config_type = config_type
