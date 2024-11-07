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
from abc import abstractmethod

from cmdb.manager.base_manager import BaseManager
from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.types_manager import TypesManager
from cmdb.utils.system_config import SystemConfigReader
from cmdb.manager.categories_manager import CategoriesManager
from cmdb.manager.objects_manager import ObjectsManager
from cmdb.manager.settings_writer_manager import SettingsWriterManager
from cmdb.manager.settings_reader_manager import SettingsReaderManager

from cmdb.updater.updater_settings import UpdateSettings
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                    Updater - CLASS                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
class Updater(BaseManager):
    """TODO: document"""

    def __init__(self):
        scr = SystemConfigReader()
        self.dbm = MongoDatabaseManager(**scr.get_all_values_from_section('Database'))
        self.categories_manager = CategoriesManager(self.dbm)
        self.objects_manager = ObjectsManager(self.dbm)
        self.types_manager = TypesManager(self.dbm)

        #REFACTOR-FIX (get the correct database)
        super().__init__(scr.get_value('database_name', 'Database'), self.dbm)


    @abstractmethod
    def creation_date(self):
        """
        When was the file created
        Returns: date
        """
        return NotImplementedError


    @abstractmethod
    def description(self):
        """
        What does the update
        Returns: name
        """
        return NotImplementedError


    @abstractmethod
    def start_update(self):
        """TODO: document"""
        return NotImplementedError


    def increase_updater_version(self, value: int):
        """TODO: document"""
        settings_reader = SettingsReaderManager(self.dbm)
        settings_writer = SettingsWriterManager(self.dbm)
        updater_settings_values = settings_reader.get_all_values_from_section('updater')
        updater_setting_instance = UpdateSettings(**updater_settings_values)
        updater_setting_instance.version = value
        settings_writer.write(_id='updater', data=updater_setting_instance.__dict__)


    def error(self, msg):
        """TODO: document"""
        raise UpdaterException(msg)

#TODO: REFACTOR-FIX
class UpdaterException(Exception):
    """TODO: document"""
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
