from cmdb.user_management.user_right import GLOBAL_IDENTIFIER, BaseRight
from cmdb.user_management.rights.system_rights import SystemRight
from cmdb.user_management.rights.framework_rights import FrameworkRight, ObjectRight, TypeRight

SYSTEM_RIGHTS = [
    SystemRight(GLOBAL_IDENTIFIER),
    SystemRight('security', BaseRight.CRITICAL)
]

FRAMEWORK_RIGHTS = [
    FrameworkRight(GLOBAL_IDENTIFIER),
    ObjectRight('view'),
    ObjectRight('edit', BaseRight.SECURE),
    ObjectRight('delete', BaseRight.SECURE),
    TypeRight('view'),
    TypeRight('edit'),
    TypeRight('delete'),
]

__all__ = [
    SYSTEM_RIGHTS,
    FRAMEWORK_RIGHTS
]
