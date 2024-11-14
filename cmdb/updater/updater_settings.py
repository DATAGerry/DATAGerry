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

from cmdb.manager.settings_reader_manager import SettingsReaderManager

from cmdb.utils.helpers import process_bar, load_class
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                UpdateSettings - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class UpdateSettings:
    """Update data object"""

    def __init__(self, version: int):
        self._id: str = 'updater'
        self.version = version


    def get_id(self) -> str:
        """Get the database document identifier"""
        return self._id


    def get_version(self) -> int:
        """Get the current version"""
        return self.version


    def run_updates(self, version: int, settings_reader: SettingsReaderManager):
        """TODO: document"""
        #TODO: IMPORT-FIX
        from cmdb.updater.updater_module import UpdaterModule
        settings_reader.get_all_values_from_section('updater')
        updater_instance = UpdaterModule(settings_reader)
        versions = updater_instance.__UPDATER_VERSIONS_POOL__
        current_version = updater_instance.get_last_version()['version']

        for num, file in enumerate(sorted(versions)):
            if current_version > version and (version < file):
                process_bar('Process', len(versions), num + 1)
                updater_class = load_class(f'cmdb.updater.versions.updater_{current_version}.Update{current_version}')
                updater_instance = updater_class()
                updater_instance.start_update()
