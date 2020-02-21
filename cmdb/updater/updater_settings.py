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


import logging

from cmdb.utils.helpers import process_bar, load_class
from cmdb.utils import SystemSettingsReader

LOGGER = logging.getLogger(__name__)


class UpdateSettings:
    """Update data object"""

    __DOCUMENT_IDENTIFIER = 'updater'

    def __init__(self, version: int, *args, **kwargs):
        self._id: str = UpdateSettings.__DOCUMENT_IDENTIFIER
        self.version = version

    def get_id(self) -> str:
        """Get the database document identifier"""
        return self._id

    def get_version(self) -> int:
        """Get the current version"""
        return self.version

    def run_updates(self, version: int, ssr: SystemSettingsReader):
        from cmdb.updater import UpdaterModule
        ssr.get_all_values_from_section('updater')
        updater_instance = UpdaterModule(ssr)
        versions = updater_instance.__UPDATER_VERSIONS_POOL__
        current_version = updater_instance.get_last_version()['version']

        for num, file in enumerate(sorted(versions)):
            if current_version > version:
                process_bar('Process', len(versions), num + 1)
                updater_class = load_class(f'cmdb.updater.versions.updater_{current_version}.Update{current_version}')
                updater_instance = updater_class()
                updater_instance.start_update()
