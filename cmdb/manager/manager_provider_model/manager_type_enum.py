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
"""TODO. document"""
from enum import Enum
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
    TYPES_MANAGER = 'TypesManager'
    LOCATIONS_MANAGER = 'LocationsManager'
    SECTION_TEMPLATES_MANAGER = 'SectionTemplatesManager'
    OBJECT_LINKS_MANAGER = 'ObjectLinksManager'
    SYSTEM_SETTINGS_READER = 'SystemSettingsReader'
    SYSTEM_SETTINGS_WRITER = 'SystemSettingsWriter'
    SECURITY_MANAGER = 'SecurityManager'
