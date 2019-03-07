from cmdb.user_management.user_right import GLOBAL_IDENTIFIER, BaseRight
from cmdb.user_management.rights.system_rights import SystemRight
from cmdb.user_management.rights.framework_rights import FrameworkRight, ObjectRight, TypeRight

SYSTEM_RIGHTS = [
    SystemRight(GLOBAL_IDENTIFIER, description='system settings rights'),
    SystemRight('security', BaseRight.CRITICAL, description="security features"),
    SystemRight('user_management', BaseRight.CRITICAL, description="user management"),
]

FRAMEWORK_RIGHTS = [
    FrameworkRight(GLOBAL_IDENTIFIER, description="all rights which handling with the object framework"),
    ObjectRight('view', description="view objects"),
    ObjectRight('edit', BaseRight.SECURE, description="edit objects"),
    ObjectRight('delete', BaseRight.SECURE, description="delete objects"),
    TypeRight('view', description="view types"),
    TypeRight('edit', description="edit types"),
    TypeRight('delete', description="delete types"),
]

__all__ = [
    SYSTEM_RIGHTS,
    FRAMEWORK_RIGHTS
]
