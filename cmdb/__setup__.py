# dataGerry - OpenSource Enterprise CMDB
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
from enum import Enum

LOGGER = logging.getLogger(__name__)


class SetupRoutine:
    class SetupStatus(Enum):
        NOT = 0
        RUNNING = 1
        ERROR = 2
        FINISHED = 3

    def __init__(self):
        self.status = SetupRoutine.SetupStatus.NOT
        # check if settings are loaded
        from cmdb.utils.system_reader import SystemConfigReader
        self.setup_system_config_reader = SystemConfigReader()
        system_config_reader_status = self.setup_system_config_reader.status()
        if system_config_reader_status is not True:
            self.status = SetupRoutine.SetupStatus.ERROR
            raise RuntimeError(
                f'The system configuration files were loaded incorrectly or nothing has been loaded at all. - \
                    system config reader status: {system_config_reader_status}')

    def get_setup_status(self):
        return self.status

    def setup(self) -> SetupStatus:
        LOGGER.info('SETUP ROUTINE: STARTED...')
        self.status = SetupRoutine.SetupStatus.RUNNING
        # check database
        if not self.__check_database():
            self.status = SetupRoutine.SetupStatus.ERROR
            raise RuntimeError(
                'The database manager could not be initialized. Perhaps the database cannot be reached, \
                or the database was already initialized.'
            )
        # init database
        try:
            self.__init_database()
        except Exception as err:
            self.status = SetupRoutine.SetupStatus.ERROR
            raise RuntimeError(
                f'Something went wrong during the initialization of the database. \n Error: {err}'
            )

        # generate keys
        LOGGER.info('SETUP ROUTINE: Generate rsa key pair')
        from cmdb.security.key.generator import KeyGenerator
        try:
            KeyGenerator().generate_rsa_keypair()
        except Exception as err:
            self.status = SetupRoutine.SetupStatus.ERROR
            raise RuntimeError(
                f'Something went wrong during the generation of the rsa keypair. \n Error: {err}'
            )

        # create user management
        LOGGER.info('SETUP ROUTINE: User management')
        try:
            self.__create_user_management()
        except Exception as err:
            self.status = SetupRoutine.SetupStatus.ERROR
            raise RuntimeError(
                f'Something went wrong during the generation of the user management. \n Error: {err}'
            )

        self.status = SetupRoutine.SetupStatus.FINISHED
        LOGGER.info('SETUP ROUTINE: FINISHED!')
        return self.status

    def __create_user_management(self):
        from cmdb.user_management.user_manager import UserManagement, User, UserGroup
        from cmdb.utils.security import SecurityManager
        scm = SecurityManager(self.setup_database_manager)
        usm = UserManagement(self.setup_database_manager, scm)
        admin_group = UserGroup(
            public_id=1,
            name='admin',
            label='admin',
            rights=[
                'base.system.*'
                'base.framework.*'
            ]
        )
        usm.insert_group(admin_group)
        admin_name = str(input('Admin name: '))
        admin_pass = str(input('Admin password: '))
        import datetime
        admin_user = User(
            user_name=admin_name,
            password=scm.generate_hmac(admin_pass),
            group_id=1,
            registration_time=datetime.datetime.utcnow()
        )
        usm.insert_user(admin_user)
        return True

    def __check_database(self):
        LOGGER.info('SETUP ROUTINE: Checking database connection')
        from cmdb.data_storage.database_manager import DatabaseManagerMongo
        from cmdb.data_storage.database_connection import MongoConnector, ServerSelectionTimeoutError
        try:
            self.setup_database_manager = DatabaseManagerMongo(
                connector=MongoConnector(
                    host=self.setup_system_config_reader.get_value('host', 'Database'),
                    port=int(self.setup_system_config_reader.get_value('port', 'Database')),
                    database_name=self.setup_system_config_reader.get_value('database_name', 'Database'),
                    timeout=MongoConnector.DEFAULT_CONNECTION_TIMEOUT
                )
            )

            connection_test = self.setup_database_manager.database_connector.is_connected()
        except ServerSelectionTimeoutError:
            connection_test = False
        LOGGER.info(f'SETUP ROUTINE: Database connection status {connection_test}')
        return connection_test

    def __init_database(self):
        database_name = self.setup_system_config_reader.get_value('database_name', 'Database')
        LOGGER.info(f'SETUP ROUTINE: initialize database {database_name}')
        # delete database
        self.setup_database_manager.drop(database_name)
        # create new database
        self.setup_database_manager.create(database_name)

        # generate collections
        # framework collections
        from cmdb.framework import __COLLECTIONS__ as FRAMEWORK_CLASSES
        for collection in FRAMEWORK_CLASSES:
            self.setup_database_manager.create_collection(collection.COLLECTION)
            # set unique indexes
            self.setup_database_manager.create_indexes(collection.COLLECTION, collection.get_index_keys())
        # user management collections
        from cmdb.user_management import __COLLECTIONS__ as USER_MANAGEMENT_COLLECTION
        for collection in USER_MANAGEMENT_COLLECTION:
            self.setup_database_manager.create_collection(collection.COLLECTION)
            # set unique indexes
            self.setup_database_manager.create_indexes(collection.COLLECTION, collection.get_index_keys())

        LOGGER.info('SETUP ROUTINE: initialize finished')