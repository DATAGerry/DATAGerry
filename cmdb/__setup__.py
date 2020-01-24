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

        # check database collection
        if not self.__check_database_collection_valid() and not self.__is_database_empty():
            raise Exception(
                'The current database version does not match the valid database version.'
            )

        if self.__is_database_empty():
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

            try:
                self.init_keys()
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

    def init_keys(self):
        from cmdb.security.key.generator import KeyGenerator
        kg = KeyGenerator()
        LOGGER.info('KEY ROUTINE: Generate RSA keypair')
        kg.generate_rsa_keypair()
        LOGGER.info('KEY ROUTINE: Generate aes key')
        kg.generate_symmetric_aes_key()

        self.__check_database()

        from cmdb.user_management.user_manager import UserManager
        from cmdb.utils.security import SecurityManager
        scm = SecurityManager(self.setup_database_manager)
        usm = UserManager(self.setup_database_manager)

        try:
            admin_user = usm.get_user(1)
            LOGGER.warning('KEY ROUTINE: Admin user detected')
            LOGGER.info(f'KEY ROUTINE: Enter new password for user: {admin_user.get_username()}')
            admin_pass = str(input('New admin password: '))
            new_password = scm.generate_hmac(admin_pass)
            admin_user.password = new_password
            usm.update_user(admin_user.get_public_id(), admin_user.__dict__)
            LOGGER.info(f'KEY ROUTINE: Password was updated for user: {admin_user.get_username()}')
        except Exception as ex:
            LOGGER.info(f'KEY ROUTINE: Password was updated for user failed: {ex}')
        LOGGER.info('KEY ROUTINE: FINISHED')

    def update_database_collection(self):
        LOGGER.info('UPDATE ROUTINE: Update database collection')
        from cmdb.framework import __COLLECTIONS__ as FRAMEWORK_CLASSES
        from cmdb.user_management import __COLLECTIONS__ as USER_MANAGEMENT_COLLECTION
        from cmdb.exportd import __COLLECTIONS__ as JOB_MANAGEMENT_COLLECTION
        self.status = SetupRoutine.SetupStatus.RUNNING

        # check database
        if not self.__check_database():
            self.status = SetupRoutine.SetupStatus.ERROR
            raise RuntimeError(
                'The database manager could not be initialized. Perhaps the database cannot be reached, \
                or the database was already initialized.'
            )

        if not self.__is_database_empty():
            try:
                detected_database = self.setup_database_manager.connector.database

                # update collections
                # framework collections
                for collection in FRAMEWORK_CLASSES:
                    try:
                        detected_database.validate_collection(collection.COLLECTION)['valid']
                    except:
                        self.setup_database_manager.create_collection(collection.COLLECTION)
                        # set unique indexes
                        self.setup_database_manager.create_indexes(collection.COLLECTION, collection.get_index_keys())
                        LOGGER.info(f'UPDATE ROUTINE: Database collection {collection.COLLECTION} was created.')

                # user management collections
                for collection in USER_MANAGEMENT_COLLECTION:
                    try:
                        detected_database.validate_collection(collection.COLLECTION)['valid']
                    except:
                        self.setup_database_manager.create_collection(collection.COLLECTION)
                        # set unique indexes
                        self.setup_database_manager.create_indexes(collection.COLLECTION, collection.get_index_keys())
                        LOGGER.info(f'UPDATE ROUTINE: Database collection {collection.COLLECTION} was created.')

                # exportdJob management collections
                for collection in JOB_MANAGEMENT_COLLECTION:
                    try:
                        detected_database.validate_collection(collection.COLLECTION)['valid']
                    except:
                        self.setup_database_manager.create_collection(collection.COLLECTION)
                        # set unique indexes
                        self.setup_database_manager.create_indexes(collection.COLLECTION,
                                                                   collection.get_index_keys())
                        LOGGER.info(f'UPDATE ROUTINE: Database collection {collection.COLLECTION} was created.')
            except Exception as ex:
                LOGGER.info(f'UPDATE ROUTINE: Database collection validation failed: {ex}')
        else:
            LOGGER.info('UPDATE ROUTINE: The update is faulty because no collection was detected.')

        LOGGER.info('UPDATE ROUTINE: Update database collection finished.')
        self.status = SetupRoutine.SetupStatus.FINISHED
        LOGGER.info('SETUP ROUTINE: FINISHED!')
        return self.status

    def __create_user_management(self):
        from cmdb.user_management.user_manager import UserManager, User
        from cmdb.user_management import __FIXED_GROUPS__
        from cmdb.utils.security import SecurityManager
        scm = SecurityManager(self.setup_database_manager)
        usm = UserManager(self.setup_database_manager)

        for group in __FIXED_GROUPS__:
            usm.insert_group(group)

        # setting the initial user to admin/admin as default
        admin_name = 'admin'
        admin_pass = 'admin'

        import datetime
        admin_user = User(
            public_id=1,
            user_name=admin_name,
            password=scm.generate_hmac(admin_pass),
            group_id=__FIXED_GROUPS__[0].get_public_id(),
            registration_time=datetime.datetime.utcnow()
        )
        usm.insert_user(admin_user)
        return True

    def __check_database(self):
        LOGGER.info('SETUP ROUTINE: Checking database connection')
        from cmdb.data_storage.database_manager import DatabaseManagerMongo
        from cmdb.data_storage.database_connection import ServerTimeoutError
        try:
            self.setup_database_manager = DatabaseManagerMongo(
                **self.setup_system_config_reader.get_all_values_from_section('Database')
            )

            connection_test = self.setup_database_manager.connector.is_connected()
        except ServerTimeoutError:
            connection_test = False
        LOGGER.info(f'SETUP ROUTINE: Database connection status {connection_test}')
        return connection_test

    def __is_database_empty(self) -> bool:
        return not self.setup_database_manager.connector.database.list_collection_names()

    def __check_database_collection_valid(self) -> bool:
        LOGGER.info('SETUP ROUTINE: Checking database collection validation')
        from cmdb.framework import __COLLECTIONS__ as FRAMEWORK_CLASSES
        from cmdb.user_management import __COLLECTIONS__ as USER_MANAGEMENT_COLLECTION
        from cmdb.exportd import __COLLECTIONS__ as JOB_MANAGEMENT_COLLECTION
        detected_database = self.setup_database_manager.connector.database
        collection_test = False

        try:
            # framework collections
            for collection in FRAMEWORK_CLASSES:
                collection_test = detected_database.validate_collection(collection.COLLECTION, scandata=True)['valid']
            # user management collections
            for collection in USER_MANAGEMENT_COLLECTION:
                collection_test = detected_database.validate_collection(collection.COLLECTION, scandata=True)['valid']
            # exportdJob management collections
            for collection in JOB_MANAGEMENT_COLLECTION:
                collection_test = detected_database.validate_collection(collection.COLLECTION, scandata=True)[
                    'valid']
        except Exception as ex:
            LOGGER.info(f'SETUP ROUTINE: Database collection validation for "{collection.COLLECTION}" failed. '
                        f'msgerror: {ex}')
            collection_test = False

        LOGGER.info(f'SETUP ROUTINE: Database collection validation status {collection_test}')
        return collection_test

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

        # ExportdJob management collections
        from cmdb.exportd import __COLLECTIONS__ as JOB_MANAGEMENT_COLLECTION
        for collection in JOB_MANAGEMENT_COLLECTION:
            self.setup_database_manager.create_collection(collection.COLLECTION)
            # set unique indexes
            self.setup_database_manager.create_indexes(collection.COLLECTION, collection.get_index_keys())

        LOGGER.info('SETUP ROUTINE: initialize finished')
