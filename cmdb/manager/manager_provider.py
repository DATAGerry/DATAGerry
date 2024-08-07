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

from cmdb.user_management import UserModel
from cmdb.user_management.rights import __all__ as rights
from cmdb.user_management.managers.right_manager import RightManager

from cmdb.manager.categories_manager import CategoriesManager
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.managers.object_manager import ObjectManager
from cmdb.manager.logs_manager import LogsManager
from cmdb.docapi.docapi_template.docapi_template_manager import DocapiTemplateManager
from cmdb.user_management.managers.user_manager import UserManager
from cmdb.user_management.managers.setting_manager import UserSettingsManager
from cmdb.user_management.managers.group_manager import GroupManager
from cmdb.media_library.media_file_manager import MediaFileManager
from cmdb.exportd.exportd_logs.exportd_log_manager import ExportdLogManager
from cmdb.framework.managers.type_manager import TypeManager
from cmdb.manager.locations_manager import LocationsManager
from cmdb.manager.section_templates_manager import SectionTemplatesManager
from cmdb.manager.object_links_manager import ObjectLinksManager
from cmdb.exportd.exportd_job.exportd_job_manager import ExportdJobManager
from cmdb.exportd.managers.exportd_log_manager import ExportDLogManager
from cmdb.exportd.managers.exportd_job_manager import ExportDJobManager

from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils.system_writer import SystemSettingsWriter
# -------------------------------------------------------------------------------------------------------------------- #
LOGGER = logging.getLogger(__name__)


class ManagerType(Enum):
    """Enum of the different Managers which are used by the API routes"""
    CATEGORIES_MANAGER = 'CategoriesManager'
    CMDB_OBJECT_MANAGER = 'CmdbObjectManager'
    OBJECT_MANAGER = 'ObjectManager'
    LOGS_MANAGER = 'LogsManager'
    DOCAPI_TEMPLATE_MANAGER = 'DocapiTemplateManager'
    USER_MANAGER = 'UserManager'
    USER_SETTINGS_MANAGER = 'UserSettingsManager'
    GROUP_MANAGER = 'GroupManager'
    MEDIA_FILE_MANAGER = 'MediaFileManager'
    EXPORTD_LOG_MANAGER = 'ExportdLogManager'
    TYPE_MANAGER = 'TypeManager'
    LOCATIONS_MANAGER = 'LocationsManager'
    SECTION_TEMPLATES_MANAGER = 'SectionTemplatesManager'
    OBJECT_LINKS_MANAGER = 'ObjectLinksManager'
    EXPORTD_JOB_MANAGER = 'ExportdJobManager'
    EXPORT_D_LOG_MANAGER = 'ExportDLogManager'
    EXPORT_D_JOB_MANAGER = 'ExportDJobManager'
    SYSTEM_SETTINGS_READER = 'SystemSettingsReader'
    SYSTEM_SETTINGS_WRITER = 'SystemSettingsWriter'


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
            ManagerType.CMDB_OBJECT_MANAGER: CmdbObjectManager,
            ManagerType.OBJECT_MANAGER: ObjectManager,
            ManagerType.LOGS_MANAGER: LogsManager,
            ManagerType.DOCAPI_TEMPLATE_MANAGER: DocapiTemplateManager,
            ManagerType.USER_MANAGER: UserManager,
            ManagerType.USER_SETTINGS_MANAGER: UserSettingsManager,
            ManagerType.GROUP_MANAGER: GroupManager,
            ManagerType.MEDIA_FILE_MANAGER: MediaFileManager,
            ManagerType.EXPORTD_LOG_MANAGER: ExportdLogManager,
            ManagerType.TYPE_MANAGER: TypeManager,
            ManagerType.LOCATIONS_MANAGER: LocationsManager,
            ManagerType.SECTION_TEMPLATES_MANAGER: SectionTemplatesManager,
            ManagerType.OBJECT_LINKS_MANAGER: ObjectLinksManager,
            ManagerType.EXPORTD_JOB_MANAGER: ExportdJobManager,
            ManagerType.EXPORT_D_LOG_MANAGER: ExportDLogManager,
            ManagerType.EXPORT_D_JOB_MANAGER: ExportDJobManager,
            ManagerType.SYSTEM_SETTINGS_READER: SystemSettingsReader,
            ManagerType.SYSTEM_SETTINGS_WRITER: SystemSettingsWriter
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
                ManagerType.CMDB_OBJECT_MANAGER,
                ManagerType.OBJECT_MANAGER,
                ManagerType.LOGS_MANAGER,
                ManagerType.DOCAPI_TEMPLATE_MANAGER,
                ManagerType.LOCATIONS_MANAGER,
                ManagerType.SECTION_TEMPLATES_MANAGER,
                ManagerType.OBJECT_LINKS_MANAGER,
                ManagerType.EXPORTD_JOB_MANAGER,
            ]:
                return common_args + (current_app.event_queue, request_user.database)

            if manager_type == ManagerType.GROUP_MANAGER:
                right_manager = RightManager(rights)
                return common_args + (right_manager, request_user.database)

            if manager_type in [
                ManagerType.USER_MANAGER,
                ManagerType.USER_SETTINGS_MANAGER,
                ManagerType.MEDIA_FILE_MANAGER,
                ManagerType.EXPORTD_LOG_MANAGER,
                ManagerType.TYPE_MANAGER,
                ManagerType.EXPORT_D_LOG_MANAGER,
                ManagerType.EXPORT_D_JOB_MANAGER,
                ManagerType.SYSTEM_SETTINGS_READER,
                ManagerType.SYSTEM_SETTINGS_WRITER
            ]:
                return common_args + (request_user.database,)
        else:
            if manager_type in [
                ManagerType.CATEGORIES_MANAGER,
                ManagerType.CMDB_OBJECT_MANAGER,
                ManagerType.OBJECT_MANAGER,
                ManagerType.LOGS_MANAGER,
                ManagerType.DOCAPI_TEMPLATE_MANAGER,
                ManagerType.LOCATIONS_MANAGER,
                ManagerType.SECTION_TEMPLATES_MANAGER,
                ManagerType.OBJECT_LINKS_MANAGER,
                ManagerType.EXPORTD_JOB_MANAGER,
            ]:
                return common_args + (current_app.event_queue,)

            if manager_type == ManagerType.GROUP_MANAGER:
                right_manager = RightManager(rights)

                return common_args + (right_manager,)

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
