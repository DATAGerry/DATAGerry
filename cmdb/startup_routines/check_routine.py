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
"""
This module contains logics for database validation and setup
"""
import logging
from datetime import datetime, timezone
from pymongo.errors import OperationFailure

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.users_manager import UsersManager
from cmdb.manager.groups_manager import GroupsManager
from cmdb.manager.security_manager import SecurityManager
from cmdb.manager.settings_reader_manager import SettingsReaderManager

from cmdb.startup_routines.check_status_enum import CheckStatus
from cmdb.updater.updater_module import UpdaterModule
from cmdb.models.user_model.user import UserModel
from cmdb.models.location_model.cmdb_location import CmdbLocation
from cmdb.models.section_template_model.cmdb_section_template import CmdbSectionTemplate
from cmdb.models.reports_model.cmdb_report_category import CmdbReportCategory
from cmdb.models.user_management_constants import (
    __FIXED_GROUPS__,
    __COLLECTIONS__ as USER_MANAGEMENT_COLLECTION
)
from cmdb.framework.constants import __COLLECTIONS__ as FRAMEWORK_CLASSES

from cmdb.errors.system_config import SectionError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 CheckRoutine - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class CheckRoutine:
    """
    This class holds checks for the database check routines
    """
    def __init__(self, dbm: MongoDatabaseManager):
        self.status: int = CheckStatus.NOT
        self.dbm = dbm


    def get_check_status(self) -> int:
        """
        Returns the CheckStatus of the current CheckRoutine

        Returns:
            (int): Current CheckStatus
        """
        return self.status


    def checker(self):
        """TODO: document"""
        LOGGER.info('STARTING Checks...')
        self.status = CheckStatus.FINISHED

        try:
            # check database
            if not self.__is_database_empty():
                if not (self.__check_database_collection_valid() and self.has_updates()):
                    LOGGER.warning("""
                                The current database collections are not valid!
                                An update is avaiable which will be installed automatically.
                                """)
                    self.status = CheckStatus.HAS_UPDATES
            LOGGER.info('FINISHED Checks!')

            return self.status
        except Exception as err:
            raise RuntimeError(err) from err


    def __is_database_empty(self) -> bool:
        """
        Checks if there are any collections in the initialised database

        Returns:
            (bool): Returns bool if there are any collection in the initialised database
        """
        return not self.dbm.connector.database.list_collection_names()


    def __check_database_collection_valid(self) -> bool:
        LOGGER.info('CHECK: Checking database collection validation')
        detected_database = self.dbm.connector.database
        collection_test = True

        all_collections = detected_database.list_collection_names()

        try:
            # framework collections
            for collection in FRAMEWORK_CLASSES:
                #first check if collection exists, else create it
                if collection.COLLECTION not in all_collections:
                    created_collection = self.dbm.create_collection(collection.COLLECTION)
                    self.dbm.create_indexes(collection.COLLECTION, collection.get_index_keys())
                    LOGGER.info("CHECK: Created missing Collection => %s", created_collection)

                collection_test = detected_database.validate_collection(collection.COLLECTION, scandata=True)['valid']

                # setup locations if valid test
                if collection == CmdbLocation and collection_test:
                    root_location: CmdbLocation = self.dbm.find_one(collection.COLLECTION, 1)

                    if root_location:
                        if self.dbm.validate_root_location(CmdbLocation.to_data(root_location)):
                            LOGGER.info("CHECK: Root Location valid")
                        else:
                            LOGGER.info("CHECK: Root Location invalalid => Fixing the Issue!")
                            self.dbm.set_root_location(collection.COLLECTION, create=False)
                    else:
                        LOGGER.info("CHECK: No Root Location => Creating a new Root Location!")
                        self.dbm.set_root_location(collection.COLLECTION, create=True)

                #Setup section templates if valid test
                if collection == CmdbSectionTemplate and collection_test:
                    # Add predefined templates if they don't exist
                    self.dbm.init_predefined_templates(collection.COLLECTION)

                #Setup general category
                if collection == CmdbReportCategory and collection_test:
                    # Add predefined templates if they don't exist
                    self.dbm.create_general_report_category(collection.COLLECTION)

            # user management collections
            for collection in USER_MANAGEMENT_COLLECTION:
                collection_test = detected_database.validate_collection(collection.COLLECTION, scandata=True)['valid']

            # if there are no groups create groups and admin user
            if self.dbm.count('management.groups') < 2:
                self.init_user_management()
        except OperationFailure as err:
            LOGGER.info('CHECK: Database collection validation for "%s" failed, error: %s', collection.COLLECTION, err)
            collection_test = False

        LOGGER.info('CHECK: Database collection validation status %s',collection_test)
        return collection_test


    def init_user_management(self):
        """Creates intital groups and admin user"""
        scm = SecurityManager(self.dbm)
        groups_manager = GroupsManager(self.dbm)
        users_manager = UsersManager(self.dbm)

        for group in __FIXED_GROUPS__:
            groups_manager.insert_group(group)

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

        users_manager.insert_user(admin_user)


    def has_updates(self) -> bool:
        """
        Check if updates are available

        Returns:
            (bool): True if updates are available else raises an error
        """
        try:
            settings_reader = SettingsReaderManager(self.dbm)
            settings_reader.get_all_values_from_section('updater')

            upd_module = UpdaterModule(settings_reader)
            new_version = upd_module.get_last_version()['version']
            current_version = upd_module.settings.version

            if new_version > current_version:
                LOGGER.info(
                    """
                    There are new updates available. Updating initialised...
                    Current Updater Version: %s
                    Newest Update Version: %s
                    """,current_version, new_version)

                return False

        except SectionError as err:
            LOGGER.error(err)
            return False

        return True
