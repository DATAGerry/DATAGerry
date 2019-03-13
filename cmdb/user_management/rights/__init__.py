from cmdb.user_management.user_right import GLOBAL_IDENTIFIER, BaseRight
from cmdb.user_management.rights.system_rights import SystemRight, UserManagementRights
from cmdb.user_management.rights.framework_rights import FrameworkRight, ObjectRight, TypeRight, CategoryRight

SYSTEM_RIGHTS = [
    SystemRight(GLOBAL_IDENTIFIER, description='system settings rights'),
    SystemRight('security', BaseRight.CRITICAL, description="security features"),
    [
        UserManagementRights(GLOBAL_IDENTIFIER),
        UserManagementRights('manage_users', BaseRight.SECURE, description="manage users"),
        UserManagementRights('manage_groups', BaseRight.SECURE, description="manage groups"),
        UserManagementRights('manage_rights', BaseRight.DANGER, description="manage_rights")
    ]
]

FRAMEWORK_RIGHTS = [
    FrameworkRight(GLOBAL_IDENTIFIER, description="all rights which handling with the object framework"),

    [
        ObjectRight(GLOBAL_IDENTIFIER),
        ObjectRight('view', description="view objects"),
        ObjectRight('edit', BaseRight.PROTECTED, description="edit objects"),
        ObjectRight('delete', BaseRight.SECURE, description="delete objects")
    ],
    [
        TypeRight(GLOBAL_IDENTIFIER),
        TypeRight('view', BaseRight.PROTECTED, description="view types"),
        TypeRight('edit', BaseRight.PROTECTED, description="edit types"),
        TypeRight('delete', BaseRight.SECURE, description="delete types")
    ],
    [
        CategoryRight(GLOBAL_IDENTIFIER),
        CategoryRight('view', description="view category"),
        CategoryRight('edit', BaseRight.PROTECTED, description="edit category"),
        CategoryRight('delete', BaseRight.SECURE, description="delete category")
    ]
]

__all__ = [
    SYSTEM_RIGHTS,
    FRAMEWORK_RIGHTS
]
