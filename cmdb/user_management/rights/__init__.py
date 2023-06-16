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

from cmdb.user_management.rights.import_rights import ImportRight, ImportObjectRight, ImportTypeRight
from cmdb.user_management.models.right import GLOBAL_RIGHT_IDENTIFIER, BaseRight, Levels
from cmdb.user_management.rights.system_rights import SystemRight
from cmdb.user_management.rights.user_management_rights import UserManagementRight, UserRight, GroupRight
from cmdb.user_management.rights.framework_rights import FrameworkRight, ObjectRight, TypeRight, CategoryRight, \
    LogRight
from cmdb.user_management.rights.export_rights import ExportRight, ExportObjectRight, ExportTypeRight
from cmdb.user_management.rights.exportd_rights import ExportdRight, ExportdJobRight, ExportdLogRight
from cmdb.user_management.rights.docapi_rights import DocapiRight, DocapiTemplateRight

SYSTEM_RIGHTS = (
    SystemRight(GLOBAL_RIGHT_IDENTIFIER, description='System and settings'),
    (
        SystemRight('view', description='View system configurations and settings'),
        SystemRight('edit', description='Edit system configurations and settings'),
        SystemRight('reload', description='Reload system configurations')
    )
)

FRAMEWORK_RIGHTS = (
    FrameworkRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage the core framework'),

    (
        ObjectRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage objects from framework'),
        (
            ObjectRight('view', description='View objects'),
            ObjectRight('add', description='Add objects'),
            ObjectRight('edit', Levels.PROTECTED, description='Edit objects'),
            ObjectRight('delete', Levels.SECURE, description='Delete objects'),
            ObjectRight('activation', Levels.SECURE, description='Activate/Deactivate objects')
        )
    ),
    (
        TypeRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage types from framework'),
        (
            TypeRight('view', Levels.PROTECTED, description='View types'),
            TypeRight('add', Levels.PROTECTED, description='Add types'),
            TypeRight('edit', Levels.SECURE, description='Edit types'),
            TypeRight('delete', Levels.SECURE, description='Delete types'),
            TypeRight('activation', Levels.SECURE, description='Activate/Deactivate types'),
            TypeRight('clean', Levels.SECURE, description='Clean type fields')
        )
    ),
    (
        CategoryRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage categories from framework'),
        (
            CategoryRight('view', description='View category'),
            CategoryRight('add', description='Add category'),
            CategoryRight('edit', Levels.PROTECTED, description='Edit category'),
            CategoryRight('delete', Levels.SECURE, description='Delete category')
        )
    ),
    (
        LogRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage framework logs'),
        (
            LogRight('view', description='View logs'),
            LogRight('reload', Levels.SECURE, description='Reload logs'),
            LogRight('delete', Levels.DANGER, description='Delete logs')
        )
    )
)

EXPORT_RIGHTS = (
    ExportRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage exports'),
    (
        ExportObjectRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage object exports')
    ),
    (
        ExportTypeRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage type exports')
    )
)

IMPORT_RIGHTS = (
    ImportRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage imports'),
    (
        ImportObjectRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage object imports')
    ),
    (
        ImportTypeRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage type imports')
    )
)

USER_MANAGEMENT_RIGHTS = (
    UserManagementRight(GLOBAL_RIGHT_IDENTIFIER, description='UserModel management'),
    (
        UserRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage users'),
        (
            UserRight('view', description='View user'),
            UserRight('add', description='Add user'),
            UserRight('edit', Levels.SECURE, description='Edit user'),
            UserRight('delete', Levels.SECURE, description='Delete user')
        ),
        GroupRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage groups'),
        (
            GroupRight('view', description='View group'),
            GroupRight('add', Levels.DANGER, description='Add group'),
            GroupRight('edit', Levels.DANGER, description='Edit group'),
            GroupRight('delete', Levels.SECURE, description='Delete group')
        )
    )
)

EXPORTD_RIGHTS = (
    ExportdRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage exportd'),
    (
        ExportdJobRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage jobs'),
        (
            ExportdJobRight('view', description='View job'),
            ExportdJobRight('add', description='Add job'),
            ExportdJobRight('edit', Levels.SECURE, description='Edit job'),
            ExportdJobRight('delete', Levels.SECURE, description='Delete job'),
            ExportdJobRight('run', Levels.SECURE, description='Run job manual')
        ),
    ),
    (
        ExportdLogRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage exportd logs'),
        (
            ExportdLogRight('view', description='View exportd logs'),
            ExportdLogRight('reload', Levels.SECURE, description='Reload exportd logs'),
            ExportdLogRight('delete', Levels.DANGER, description='Delete exportd logs')
        )
    )
)

DOCAPI_RIGHTS = (
    DocapiRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage DocAPI'),
    (
        DocapiTemplateRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage DocAPI templates'),
        (
            DocapiTemplateRight('view', description='View template'),
            DocapiTemplateRight('add', description='Add template'),
            DocapiTemplateRight('edit', Levels.SECURE, description='Edit template'),
            DocapiTemplateRight('delete', Levels.SECURE, description='Delete template'),
        ),
    )
)
__all__ = (
    BaseRight(
        Levels.NOTSET, GLOBAL_RIGHT_IDENTIFIER, description='Base application right'
    ),
    SYSTEM_RIGHTS,
    FRAMEWORK_RIGHTS,
    EXPORT_RIGHTS,
    IMPORT_RIGHTS,
    USER_MANAGEMENT_RIGHTS,
    EXPORTD_RIGHTS,
    DOCAPI_RIGHTS
)
