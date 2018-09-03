from cmdb.user_management.user_manager import UserManagement
from cmdb.user_management.user_groups import UserGroup
from cmdb.user_management.user import User
from cmdb.user_management.user_authentication import AuthenticationProvider

__COLLECTIONS__ = [
    UserGroup
]


def get_user_manager():
    from cmdb.data_storage import get_pre_init_database
    from cmdb.utils import get_security_manager
    db_man = get_pre_init_database()
    return UserManagement(
        database_manager=db_man,
        security_manager=get_security_manager(
            database_manager=db_man
        )
    )
