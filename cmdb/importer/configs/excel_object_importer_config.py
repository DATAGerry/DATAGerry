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
import logging

from cmdb.importer.content_types import XLSXContent
from cmdb.importer.configs.object_importer_config import ObjectImporterConfig
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                           ExcelObjectImporterConfig - CLASS                                          #
# -------------------------------------------------------------------------------------------------------------------- #
class ExcelObjectImporterConfig(ObjectImporterConfig, XLSXContent):
    """TODO: document"""
    MANUALLY_MAPPING = True

    def __init__(self, type_id: int, mapping: list = None, start_element: int = 0, max_elements: int = 0,
                 overwrite_public: bool = True, *args, **kwargs):
        super().__init__(type_id=type_id, mapping=mapping, start_element=start_element,
                                                        max_elements=max_elements, overwrite_public=overwrite_public)
