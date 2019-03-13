from cmdb.user_management.user_right import BaseRight


class SystemRight(BaseRight):
    MIN_LEVEL = BaseRight.SECURE
    PREFIX = '{}.{}'.format(BaseRight.PREFIX, 'system')

    def __init__(self, name: str, level: int = 50, description: str = None):
        super(SystemRight, self).__init__(level, name, description=description)


class UserManagementRights(SystemRight):
    MIN_LEVEL = BaseRight.SECURE
    MAX_LEVEL = BaseRight.DANGER
    PREFIX = '{}.{}'.format(SystemRight.PREFIX, 'user')

    def __init__(self, name: str, level: int = MIN_LEVEL, description: str = None):
        super(UserManagementRights, self).__init__(name, level, description=description)
