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
"""Example service"""
import logging
import time
import cmdb.process_management.service
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class ExampleService(cmdb.process_management.service.AbstractCmdbService):
    """Example implementation of AbstractCmdbService"""

    def __init__(self):
        super().__init__()
        self._name = "service1"
        self._eventtypes = ["cmdb.core.#", "cmdb.service1.#"]



    def _run(self):
        LOGGER.info("%s: start run", self._name)
        while not self._event_shutdown.is_set():
            time.sleep(10)
        LOGGER.info("%s: end run", self._name)



    def _handle_event(self, event):
        LOGGER.info("%s: event received: %s",self._name, event)
