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
"""
This managers represents the core functionalities for the use of CMDB section templates.
All communication with the section templates is controlled by this manager.
The implementation of the manager used is always realized using the respective superclass.

"""
import logging
from queue import Queue

from cmdb.framework.cmdb_base import CmdbManagerBase
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class CmdbSectionTemplateManager(CmdbManagerBase):
    """
    class CmdbSectionTemplateManager
    """
    def __init__(self, database_manager=None, event_queue: Queue = None):
        self._event_queue = event_queue
        super().__init__(database_manager)
