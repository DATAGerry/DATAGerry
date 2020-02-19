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


from cmdb.utils import SystemSettingsReader
from cmdb.updater.updater_settings import UpdateSettings


class UpdaterModule:
    """Updater module class"""

    __DEFAULT_SETTINGS__ = {
        '_id': 'updater',
        'version': 0,
    }

    def __init__(self, system_settings_reader: SystemSettingsReader):
        auth_settings_values = system_settings_reader.\
            get_all_values_from_section('updater', default=UpdaterModule.get_last_version())
        self.__settings: UpdateSettings = self.__init_settings(auth_settings_values)

    def __init_settings(self, auth_settings_values: dict) -> UpdateSettings:
        """Merge default values with database entries"""
        return UpdateSettings(**auth_settings_values)

    @property
    def settings(self) -> UpdateSettings:
        """Get the current auth settings"""
        return self.__settings

    @staticmethod
    def get_last_version() -> dict:
        import os
        files = sorted(os.listdir("./updater/versions"))
        return {'_id': 'updater',
                'version': int(os.path.splitext(files[len(files) - 1])[0].replace('updater_', ''))}

