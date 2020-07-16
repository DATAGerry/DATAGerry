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

from cmdb.user_management.rights.import_rights import ImportRight, ImportObjectRight, ImportTypeRight
from cmdb.user_management.user_right import GLOBAL_RIGHT_IDENTIFIER, BaseRight
from cmdb.user_management.rights.system_rights import SystemRight
from cmdb.user_management.rights.user_management_rights import UserManagementRight, UserRight, GroupRight
from cmdb.user_management.rights.framework_rights import FrameworkRight, ObjectRight, TypeRight, CategoryRight, \
    LogRight, CollectionRight
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
            ObjectRight('edit', BaseRight.PROTECTED, description='Edit objects'),
            ObjectRight('delete', BaseRight.SECURE, description='Delete objects'),
            ObjectRight('activation', BaseRight.SECURE, description='Activate/Deactivate objects')
        )
    ),
    (
        TypeRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage types from framework'),
        (
            TypeRight('view', BaseRight.PROTECTED, description='View types'),
            TypeRight('add', BaseRight.PROTECTED, description='Add types'),
            TypeRight('edit', BaseRight.SECURE, description='Edit types'),
            TypeRight('delete', BaseRight.SECURE, description='Delete types'),
            TypeRight('activation', BaseRight.SECURE, description='Activate/Deactivate types'),
            TypeRight('clean', BaseRight.SECURE, description='Clean type fields')
        )
    ),
    (
        CategoryRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage categories from framework'),
        (
            CategoryRight('view', description='View category'),
            CategoryRight('add', description='Add category'),
            CategoryRight('edit', BaseRight.PROTECTED, description='Edit category'),
            CategoryRight('delete', BaseRight.SECURE, description='Delete category'),
            CategoryRight('tree', BaseRight.PROTECTED, description='View the complete category tree with types')
        )
    ),
    (
        CollectionRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage collections'),
        (
            CollectionRight('view', BaseRight.PERMISSION, description='View collections'),
            CollectionRight('add', BaseRight.PERMISSION, description='View collections'),
            CollectionRight('edit', BaseRight.PERMISSION, description='View collections'),
            CollectionRight('delete', BaseRight.PROTECTED, description='View collections'),
        )
    ),
    (
        LogRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage framework logs'),
        (
            LogRight('view', description='View logs'),
            LogRight('reload', BaseRight.SECURE, description='Reload logs'),
            LogRight('delete', BaseRight.DANGER, description='Delete logs')
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
    UserManagementRight(GLOBAL_RIGHT_IDENTIFIER, description='User management'),
    (
        UserRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage users'),
        (
            UserRight('view', description='View user'),
            UserRight('add', description='Add user'),
            UserRight('edit', BaseRight.SECURE, description='Edit user'),
            UserRight('delete', BaseRight.SECURE, description='Delete user')
        ),
        GroupRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage groups'),
        (
            GroupRight('view', description='View group'),
            GroupRight('add', BaseRight.DANGER, description='Add group'),
            GroupRight('edit', BaseRight.DANGER, description='Edit group'),
            GroupRight('delete', BaseRight.SECURE, description='Delete group')
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
            ExportdJobRight('edit', BaseRight.SECURE, description='Edit job'),
            ExportdJobRight('delete', BaseRight.SECURE, description='Delete job'),
            ExportdJobRight('run', BaseRight.SECURE, description='Run job manual')
        ),
    ),
    (
        ExportdLogRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage exportd logs'),
        (
            ExportdLogRight('view', description='View exportd logs'),
            ExportdLogRight('reload', BaseRight.SECURE, description='Reload exportd logs'),
            ExportdLogRight('delete', BaseRight.DANGER, description='Delete exportd logs')
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
            DocapiTemplateRight('edit', BaseRight.SECURE, description='Edit template'),
            DocapiTemplateRight('delete', BaseRight.SECURE, description='Delete template'),
        ),
    )
)
__all__ = (
    BaseRight(
        BaseRight.NOTSET, GLOBAL_RIGHT_IDENTIFIER, description='Base application right'
    ),
    SYSTEM_RIGHTS,
    FRAMEWORK_RIGHTS,
    EXPORT_RIGHTS,
    IMPORT_RIGHTS,
    USER_MANAGEMENT_RIGHTS,
    EXPORTD_RIGHTS,
    DOCAPI_RIGHTS
)
