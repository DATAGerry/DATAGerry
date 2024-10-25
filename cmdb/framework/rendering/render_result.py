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
from datetime import datetime, timezone
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 RenderResult - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class RenderResult:
    """TODO: document"""

    def __init__(self):
        self.current_render_time = datetime.now(timezone.utc)
        self.object_information: dict = {}
        self.type_information: dict = {}
        self.fields: list = []
        self.sections: list = []
        self.summaries: list = []
        self.summary_line: str = ''
        self.externals: list = []
        self.multi_data_sections: list = []


    def get_object_information(self, idx):
        """TODO: document"""
        return self.object_information[idx]


    def get_type_information(self, idx):
        """TODO: document"""
        return self.type_information[idx]
