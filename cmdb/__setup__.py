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
"""TODO: document"""
import logging
from datetime import datetime, timezone
from enum import Enum

from cmdb.database.errors.connection_errors import ServerTimeoutError
from cmdb.database.errors.database_errors import DatabaseNotExists
from cmdb.database.database_manager_mongo import DatabaseManagerMongo

from cmdb.utils.system_config import SystemConfigReader
from cmdb.utils.system_writer import SystemSettingsWriter

from cmdb.updater import UpdaterModule
from cmdb.updater.updater_settings import UpdateSettings

from cmdb.security.key.generator import KeyGenerator
from cmdb.security.security import SecurityManager

from cmdb.user_management import __FIXED_GROUPS__
from cmdb.user_management import __COLLECTIONS__ as USER_MANAGEMENT_COLLECTION
from cmdb.user_management.managers.user_manager import UserManager, UserModel
from cmdb.user_management.managers.group_manager import GroupManager

from cmdb.framework import __COLLECTIONS__ as FRAMEWORK_CLASSES

from cmdb.exportd import __COLLECTIONS__ as JOB_MANAGEMENT_COLLECTION
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class SetupRoutine:
    """TODO: document"""


    class SetupStatus(Enum):
        """TODO: document"""
        NOT = 0
        RUNNING = 1
        ERROR = 2
        FINISHED = 3


    def __init__(self, dbm: DatabaseManagerMongo):
        self.status = SetupRoutine.SetupStatus.NOT
        # check if settings are loaded

        self.setup_system_config_reader: SystemConfigReader = SystemConfigReader()
        self.setup_database_manager: DatabaseManagerMongo = dbm
        system_config_reader_status: bool = self.setup_system_config_reader.status()

        if system_config_reader_status is not True:
            self.status = SetupRoutine.SetupStatus.ERROR
            raise RuntimeError(
                f'The system configuration files were loaded incorrectly or nothing has been loaded at all. - \
                    system config reader status: {system_config_reader_status}')



    def get_setup_status(self):
        """TODO: document"""
        return self.status



    def setup(self) -> SetupStatus:
        """TODO: document"""
        LOGGER.info('SETUP ROUTINE: STARTED...')
        self.status = SetupRoutine.SetupStatus.RUNNING

        # check database
        if not self.__check_database():
            self.status = SetupRoutine.SetupStatus.ERROR
            raise RuntimeError(
                'The database managers could not be initialized. Perhaps the database cannot be reached, \
                or the database was already initialized.'
            )

        if self.__is_database_empty():
            # init database
            try:
                self.__init_database()

            except Exception as err:
                self.status = SetupRoutine.SetupStatus.ERROR
                raise RuntimeError(
                    f'Something went wrong during the initialization of the database. \n Error: {err}'
                ) from err

            # generate keys
            LOGGER.info('SETUP ROUTINE: Generate rsa key pair')

            try:
                self.init_keys()
            except Exception as err:
                self.status = SetupRoutine.SetupStatus.ERROR
                raise RuntimeError(
                    f'Something went wrong during the generation of the rsa keypair. \n Error: {err}'
                ) from err

            # create user management
            LOGGER.info('SETUP ROUTINE: UserModel management')
            try:
                self.__create_user_management()
            except Exception as err:
                self.status = SetupRoutine.SetupStatus.ERROR
                raise RuntimeError(
                    f'Something went wrong during the generation of the user management. \n Error: {err}'
                ) from err

            # create version updater settings
            try:
                system_setting_writer: SystemSettingsWriter = SystemSettingsWriter(self.setup_database_manager)
                updater_setting_instance = UpdateSettings(**UpdaterModule.get_last_version())
                system_setting_writer.write(_id='updater', data=updater_setting_instance.__dict__)

            except Exception as err:
                self.status = SetupRoutine.SetupStatus.ERROR
                raise RuntimeError(
                    f'Something went wrong during the generation of the updater module. \n Error: {err}'
                ) from err

        self.status = SetupRoutine.SetupStatus.FINISHED
        LOGGER.info('SETUP ROUTINE: FINISHED!')
        return self.status



    def init_keys(self):
        """TODO: document"""
        kg = KeyGenerator(self.setup_database_manager)
        LOGGER.info('KEY ROUTINE: Generate RSA keypair')
        kg.generate_rsa_keypair()
        LOGGER.info('KEY ROUTINE: Generate aes key')
        kg.generate_symmetric_aes_key()

        self.__check_database()
        scm = SecurityManager(self.setup_database_manager)
        usm = UserManager(self.setup_database_manager)

        try:
            admin_user: UserModel = usm.get(1)
            LOGGER.warning('KEY ROUTINE: Admin user detected')
            LOGGER.info('KEY ROUTINE: Enter new password for user: %s', admin_user.user_name)

            admin_pass = str(input('New admin password: '))
            new_password = scm.generate_hmac(admin_pass)
            admin_user.password = new_password
            usm.update(admin_user.get_public_id(), admin_user)

            LOGGER.info('KEY ROUTINE: Password was updated for user: %s', admin_user.user_name)
        except Exception as ex:
            LOGGER.info('KEY ROUTINE: Password was updated for user failed: %s', ex)

        LOGGER.info('KEY ROUTINE: FINISHED')



    def __create_user_management(self):
        """TODO: document"""
        scm = SecurityManager(self.setup_database_manager)
        group_manager = GroupManager(self.setup_database_manager)
        user_manager = UserManager(self.setup_database_manager)

        for group in __FIXED_GROUPS__:
            group_manager.insert(group)

        # setting the initial user to admin/admin as default
        admin_name = 'admin'
        admin_pass = 'admin'
        admin_user = UserModel(
            public_id=1,
            user_name=admin_name,
            active=True,
            group_id=__FIXED_GROUPS__[0].get_public_id(),
            registration_time=datetime.now(timezone.utc),
            password=scm.generate_hmac(admin_pass),
        )
        user_manager.insert(admin_user)

        return True



    def __check_database(self):
        """TODO: document"""
        LOGGER.info('SETUP ROUTINE: Checking database connection')

        try:
            connection_test = self.setup_database_manager.connector.is_connected()
        except ServerTimeoutError:
            connection_test = False
        LOGGER.info('SETUP ROUTINE: Database connection status %s', connection_test)

        return connection_test



    def __is_database_empty(self) -> bool:
        return not self.setup_database_manager.connector.database.list_collection_names()



    def __init_database(self):
        """TODO: document"""
        database_name = self.setup_system_config_reader.get_value('database_name', 'Database')
        LOGGER.info('SETUP ROUTINE: initialize database %s', database_name)

        # delete database
        try:
            self.setup_database_manager.drop_database(database_name)
        except DatabaseNotExists as err:
            LOGGER.error(err.message)

        # create new database
        self.setup_database_manager.create_database(database_name)


        #generate framework collections
        for collection in FRAMEWORK_CLASSES:
            self.setup_database_manager.create_collection(collection.COLLECTION)
            # set unique indexes
            self.setup_database_manager.create_indexes(collection.COLLECTION, collection.get_index_keys())

        #generate user management collections
        for collection in USER_MANAGEMENT_COLLECTION:
            self.setup_database_manager.create_collection(collection.COLLECTION)
            # set unique indexes
            self.setup_database_manager.create_indexes(collection.COLLECTION, collection.get_index_keys())

        #generate ExportdJob management collections
        for collection in JOB_MANAGEMENT_COLLECTION:
            self.setup_database_manager.create_collection(collection.COLLECTION)
            # set unique indexes
            self.setup_database_manager.create_indexes(collection.COLLECTION, collection.get_index_keys())

        LOGGER.info('SETUP ROUTINE: initialize finished')
