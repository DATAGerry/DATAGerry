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
"""This class provides the different managers for the API routes"""
import logging
from enum import Enum
from flask import current_app

from cmdb.user_management.models.user import UserModel

from cmdb.manager.categories_manager import CategoriesManager
from cmdb.manager.objects_manager import ObjectsManager
from cmdb.manager.logs_manager import LogsManager
from cmdb.manager.docapi_templates_manager import DocapiTemplatesManager
from cmdb.manager.users_manager import UsersManager
from cmdb.manager.users_settings_manager import UsersSettingsManager
from cmdb.manager.groups_manager import GroupsManager
from cmdb.manager.media_files_manager import MediaFilesManager
from cmdb.manager.exportd_logs_manager import ExportdLogsManager
from cmdb.manager.exportd_jobs_manager import ExportdJobsManager
from cmdb.manager.types_manager import TypesManager
from cmdb.manager.locations_manager import LocationsManager
from cmdb.manager.section_templates_manager import SectionTemplatesManager
from cmdb.manager.object_links_manager import ObjectLinksManager

from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils.system_writer import SystemSettingsWriter
from cmdb.security.security import SecurityManager
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
class ManagerType(Enum):
    """Enum of the different Managers which are used by the API routes"""
    CATEGORIES_MANAGER = 'CategoriesManager'
    OBJECTS_MANAGER = 'ObjectsManager'
    LOGS_MANAGER = 'LogsManager'
    DOCAPI_TEMPLATES_MANAGER = 'DocapiTemplatesManager'
    USERS_MANAGER = 'UsersManager'
    USERS_SETTINGS_MANAGER = 'UsersSettingsManager'
    GROUPS_MANAGER = 'GroupsManager'
    MEDIA_FILES_MANAGER = 'MediaFilesManager'
    EXPORTD_LOGS_MANAGER = 'ExportdLogsManager'
    EXPORTD_JOBS_MANAGER = 'ExportdJobsManager'
    TYPES_MANAGER = 'TypesManager'
    LOCATIONS_MANAGER = 'LocationsManager'
    SECTION_TEMPLATES_MANAGER = 'SectionTemplatesManager'
    OBJECT_LINKS_MANAGER = 'ObjectLinksManager'
    SYSTEM_SETTINGS_READER = 'SystemSettingsReader'
    SYSTEM_SETTINGS_WRITER = 'SystemSettingsWriter'
    SECURITY_MANAGER = 'SecurityManager'


class ManagerProvider:
    """Provides Managers for stateless API route requests"""

    @staticmethod
    def __get_manager_class(manager_type: ManagerType):
        """
        Returns the appropriate manager class based on the provided ManagerType

        Args:
            manager_type (ManagerType): Enum of possible Managers

        Returns:
            type: The manager class corresponding to the given ManagerType
        """
        manager_classes = {
            ManagerType.CATEGORIES_MANAGER: CategoriesManager,
            ManagerType.OBJECTS_MANAGER: ObjectsManager,
            ManagerType.LOGS_MANAGER: LogsManager,
            ManagerType.DOCAPI_TEMPLATES_MANAGER: DocapiTemplatesManager,
            ManagerType.USERS_MANAGER: UsersManager,
            ManagerType.USERS_SETTINGS_MANAGER: UsersSettingsManager,
            ManagerType.GROUPS_MANAGER: GroupsManager,
            ManagerType.MEDIA_FILES_MANAGER: MediaFilesManager,
            ManagerType.EXPORTD_LOGS_MANAGER: ExportdLogsManager,
            ManagerType.TYPES_MANAGER: TypesManager,
            ManagerType.LOCATIONS_MANAGER: LocationsManager,
            ManagerType.SECTION_TEMPLATES_MANAGER: SectionTemplatesManager,
            ManagerType.OBJECT_LINKS_MANAGER: ObjectLinksManager,
            ManagerType.EXPORTD_JOBS_MANAGER: ExportdJobsManager,
            ManagerType.SYSTEM_SETTINGS_READER: SystemSettingsReader,
            ManagerType.SYSTEM_SETTINGS_WRITER: SystemSettingsWriter,
            ManagerType.SECURITY_MANAGER: SecurityManager
        }

        return manager_classes.get(manager_type)


    @staticmethod
    def __get_manager_args(manager_type: ManagerType, request_user: UserModel):
        """
        Returns the appropriate arguments for the manager class based on the provided
        ManagerType and 'cloud_mode' flag.

        Args:
            manager_type (ManagerType): Enum of possible Managers
            request_user (UserModel): The user which is making the API call
        Returns:
            tuple: Arguments for the manager class initialization
        """
        common_args = (current_app.database_manager,)

        if current_app.cloud_mode:
            if manager_type in [
                ManagerType.CATEGORIES_MANAGER,
                ManagerType.OBJECTS_MANAGER,
                ManagerType.LOGS_MANAGER,
                ManagerType.DOCAPI_TEMPLATES_MANAGER,
                ManagerType.LOCATIONS_MANAGER,
                ManagerType.SECTION_TEMPLATES_MANAGER,
                ManagerType.OBJECT_LINKS_MANAGER,
                ManagerType.EXPORTD_JOBS_MANAGER,
            ]:
                return common_args + (current_app.event_queue, request_user.database)


            if manager_type in [
                ManagerType.GROUPS_MANAGER,
                ManagerType.USERS_MANAGER,
                ManagerType.USERS_SETTINGS_MANAGER,
                ManagerType.MEDIA_FILES_MANAGER,
                ManagerType.EXPORTD_LOGS_MANAGER,
                ManagerType.TYPES_MANAGER,
                ManagerType.SYSTEM_SETTINGS_READER,
                ManagerType.SYSTEM_SETTINGS_WRITER,
                ManagerType.SECURITY_MANAGER
            ]:
                return common_args + (request_user.database,)
        else:
            if manager_type in [
                ManagerType.CATEGORIES_MANAGER,
                ManagerType.OBJECTS_MANAGER,
                ManagerType.LOGS_MANAGER,
                ManagerType.DOCAPI_TEMPLATES_MANAGER,
                ManagerType.LOCATIONS_MANAGER,
                ManagerType.SECTION_TEMPLATES_MANAGER,
                ManagerType.OBJECT_LINKS_MANAGER,
                ManagerType.EXPORTD_JOBS_MANAGER,
            ]:
                return common_args + (current_app.event_queue,)

        # Default route where just the dbm is returned
        return common_args


    @classmethod
    def get_manager(cls, manager_type: ManagerType, request_user: UserModel):
        """Retrieves a manager based on the provided ManagerType and 'cloud_mode' app flag

        Args:
            manager_type (ManagerType): Enum of possible Managers
            request_user (UserModel): The user which is making the API call

        Returns:
            Manager: Returns the manager of the provided ManagerType
        """
        manager_class = cls.__get_manager_class(manager_type)

        if not manager_class:
            LOGGER.error("No manager found for type: %s", manager_type)
            return None

        manager_args = cls.__get_manager_args(manager_type, request_user)

        return manager_class(*manager_args)
