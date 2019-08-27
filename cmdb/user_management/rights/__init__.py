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

from cmdb.user_management.user_right import GLOBAL_IDENTIFIER, BaseRight
from cmdb.user_management.rights.system_rights import SystemRight, ManagementRight, UserRight, GroupRight
from cmdb.user_management.rights.framework_rights import FrameworkRight, ObjectRight, TypeRight, CategoryRight
from cmdb.user_management.rights.export_rights import ExportRight

SYSTEM_RIGHTS = (
    SystemRight(GLOBAL_IDENTIFIER, description='system settings rights'),
    SystemRight('security', BaseRight.CRITICAL, description="security features"),
    (
        ManagementRight(GLOBAL_IDENTIFIER, description='User management rights'),
        (
            UserRight('view', BaseRight.SECURE),
            UserRight('add', BaseRight.SECURE),
            UserRight('update', BaseRight.SECURE),
            UserRight('delete', BaseRight.SECURE),

            GroupRight('view', BaseRight.SECURE),
            GroupRight('add', BaseRight.SECURE),
            GroupRight('update', BaseRight.SECURE),
            GroupRight('delete', BaseRight.DANGER),
        )
    )
)

FRAMEWORK_RIGHTS = (
    FrameworkRight(GLOBAL_IDENTIFIER, description="all rights which handling with the object framework"),

    (
        ObjectRight(GLOBAL_IDENTIFIER),
        (
            ObjectRight('view', description="view objects"),
            ObjectRight('add', description="add objects"),
            ObjectRight('edit', BaseRight.PROTECTED, description="edit objects"),
            ObjectRight('delete', BaseRight.SECURE, description="delete objects")
        )
    ),
    (
        TypeRight(GLOBAL_IDENTIFIER),
        (
            TypeRight('view', BaseRight.PROTECTED, description="view types"),
            TypeRight('add', description="add types"),
            TypeRight('edit', BaseRight.PROTECTED, description="edit types"),
            TypeRight('delete', BaseRight.SECURE, description="delete types")
        )
    ),
    (
        CategoryRight(GLOBAL_IDENTIFIER),
        (
            CategoryRight('view', description="view category"),
            CategoryRight('add', description="add category"),
            CategoryRight('edit', BaseRight.PROTECTED, description="edit category"),
            CategoryRight('delete', BaseRight.SECURE, description="delete category")
        )
    )
)

EXPORT_RIGHTS = (
    ExportRight(GLOBAL_IDENTIFIER, description='export rights'),
)

__all__ = (
    SYSTEM_RIGHTS,
    FRAMEWORK_RIGHTS,
    EXPORT_RIGHTS
)
