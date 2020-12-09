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

from abc import abstractmethod
from cmdb.framework.cmdb_base import CmdbManagerBase
from cmdb.database.managers import DatabaseManagerMongo
from cmdb.exportd.exportd_logs.exportd_log_manager import ExportdLogManager
from cmdb.utils.error import CMDBError
from cmdb.utils.system_config import SystemConfigReader
from cmdb.framework.cmdb_object_manager import CmdbObjectManager

from cmdb.updater.updater_settings import UpdateSettings
from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils.system_writer import SystemSettingsWriter

LOGGER = logging.getLogger(__name__)


class Updater(CmdbManagerBase):

    def __init__(self):
        scr = SystemConfigReader()
        self.database_manager = DatabaseManagerMongo(
            **scr.get_all_values_from_section('Database')
        )
        self.object_manager = CmdbObjectManager(
            database_manager=self.database_manager
        )
        self.log_manager = ExportdLogManager(
            database_manager=self.database_manager)
        super().__init__(self.database_manager)

    @property
    @abstractmethod
    def author(self):
        """
        Name of the creator
        Returns: name

        """
        return NotImplementedError

    @property
    @abstractmethod
    def creation_date(self):
        """
        When was the file created
        Returns: date

        """
        return NotImplementedError

    @property
    @abstractmethod
    def description(self):
        """
        What does the update
        Returns: name

        """
        return NotImplementedError

    @abstractmethod
    def start_update(self):
        pass

    @abstractmethod
    def increase_updater_version(self, value: int):
        ssr = SystemSettingsReader(self.database_manager)
        system_setting_writer: SystemSettingsWriter = SystemSettingsWriter(self.database_manager)
        updater_settings_values = ssr.get_all_values_from_section('updater')
        updater_setting_instance = UpdateSettings(**updater_settings_values)
        updater_setting_instance.version = value
        system_setting_writer.write(_id='updater', data=updater_setting_instance.__dict__)

    def error(self, msg):
        raise UpdaterException(msg)


class UpdaterException(CMDBError):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
