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
"""TODO: document"""
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.exporter.config.config_base import BaseExporterConfig, ExporterConfigType
# -------------------------------------------------------------------------------------------------------------------- #

class ExporterConfig(BaseExporterConfig):
    """TODO: document"""
    def __init__(self, parameters: CollectionParameters, options: dict = None):
        """
        Args:
            parameters: Rest API class for parameters passed by a http request on a collection route
            options: dict of optional parameters for given route function.
        """
        self.parameters = parameters
        self.options = options or None
        super().__init__(config_type=ExporterConfigType.native)
