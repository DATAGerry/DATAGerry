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
from enum import Enum
from pymongo.errors import CollectionInvalid

from cmdb.database.mongo_database_manager import MongoDatabaseManager

from cmdb.updater.updater_module import UpdaterModule
from cmdb.updater.updater_settings import UpdateSettings
from cmdb.manager.settings_reader_manager import SettingsReaderManager
from cmdb.manager.settings_writer_manager import SettingsWriterManager
from cmdb.utils.system_config import SystemConfigReader
from cmdb.framework.constants import __COLLECTIONS__ as FRAMEWORK_CLASSES
from cmdb.user_management.constants import __COLLECTIONS__ as USER_MANAGEMENT_COLLECTION

from cmdb.errors.database import ServerTimeoutError
from cmdb.errors.setup import CollectionInitError
from cmdb.errors.system_config import SectionError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 UpdateRoutine - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class UpdateRoutine:
    """TODO: document"""

    #TODO: CLASS-FIX
    class UpateStatus(Enum):
        """TODO: document"""
        NOT = 0
        RUNNING = 1
        ERROR = 2
        FINISHED = 3


    def __init__(self, dbm: MongoDatabaseManager):
        self.status = UpdateRoutine.UpateStatus.NOT
        # check if settings are loaded

        self.setup_system_config_reader = SystemConfigReader()
        system_config_reader_status = self.setup_system_config_reader.status()
        self.dbm = dbm

        if system_config_reader_status is not True:
            self.status = UpdateRoutine.UpateStatus.ERROR
            raise RuntimeError(
                f'The system configuration files were loaded incorrectly or nothing has been loaded at all. - \
                    system config reader status: {system_config_reader_status}')


    def get_updater_status(self):
        """TODO: document"""
        return self.status


    def __check_database(self):
        """TODO: document"""
        LOGGER.info('SETUP ROUTINE: Checking database connection')
        #REFACTOR-FIX
        try:
            connection_test = self.dbm.connector.is_connected()
        except ServerTimeoutError:
            connection_test = False
        LOGGER.info('SETUP ROUTINE: Database connection status %s',connection_test)

        return connection_test


    def __is_database_empty(self) -> bool:
        """TODO: document"""
        return not self.dbm.connector.database.list_collection_names()


    def start_update(self):
        """TODO: document"""
        LOGGER.info('UPDATE ROUTINE: Update database collection')
        self.status = UpdateRoutine.UpateStatus.RUNNING

        # check database
        if not self.__check_database():
            self.status = UpdateRoutine.UpateStatus.ERROR
            raise RuntimeError(
                'The database managers could not be initialized. Perhaps the database cannot be reached, \
                or the database was already initialized.'
            )

        if not self.__is_database_empty():
            try:
                self.update_database_collection()
            except CollectionInitError as err:
                LOGGER.debug("[update_database_collection] Error: %s", err)

            self.update_db_version()
        else:
            LOGGER.info('UPDATE ROUTINE: The update is faulty because no collection was detected.')

        LOGGER.info('UPDATE ROUTINE: Update database collection finished.')
        self.status = UpdateRoutine.UpateStatus.FINISHED
        LOGGER.info('UPDATE ROUTINE: FINISHED!')

        return self.status


    def update_database_collection(self):
        """TODO: document"""
        try:
            detected_database = self.dbm.connector.database

            # update framework collections
            for collection in FRAMEWORK_CLASSES:
                try:
                    detected_database.validate_collection(collection.COLLECTION)['valid']
                except CollectionInvalid:
                    self.dbm.create_collection(collection.COLLECTION)
                    # set unique indexes
                    self.dbm.create_indexes(collection.COLLECTION, collection.get_index_keys())
                    LOGGER.info('UPDATE ROUTINE: Database collection %s was created.', collection.COLLECTION)

            # update user management collections
            for collection in USER_MANAGEMENT_COLLECTION:
                try:
                    detected_database.validate_collection(collection.COLLECTION)['valid']
                except CollectionInvalid:
                    self.dbm.create_collection(collection.COLLECTION)
                    # set unique indexes
                    self.dbm.create_indexes(collection.COLLECTION, collection.get_index_keys())
                    LOGGER.info('UPDATE ROUTINE: Database collection %s was created.', collection.COLLECTION)
        except Exception as err:
            LOGGER.info('UPDATE ROUTINE: Database collection validation failed: %s', err)
            raise CollectionInitError(str(err)) from err


    def update_db_version(self):
        """TODO: document"""
        # update version updater settings
        try:
            updater_settings_values = UpdaterModule.__DEFAULT_SETTINGS__
            settings_reader = SettingsReaderManager(self.dbm)

            try:
                updater_settings_values = settings_reader.get_all_values_from_section('updater')
                updater_setting_instance = UpdateSettings(**updater_settings_values)
            except SectionError: #ERROR-FIX (UpdateSettings initialisation is not covered)
                # create updater section if not exist
                settings_writer = SettingsWriterManager(self.dbm)
                updater_setting_instance = UpdateSettings(updater_settings_values['version'])
                settings_writer.write(_id='updater', data=updater_setting_instance.__dict__)

            # start running update files
            updater_setting_instance.run_updates(updater_settings_values.get('version'), settings_reader)

        except Exception as err:
            self.status = UpdateRoutine.UpateStatus.ERROR
            raise RuntimeError(
                f'Something went wrong during the generation of the updater module. \n Error: {err}'
            ) from err
