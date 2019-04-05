from cmdb.user_management.user_right import BaseRight


class SystemRight(BaseRight):
    MIN_LEVEL = BaseRight.SECURE
    PREFIX = '{}.{}'.format(BaseRight.PREFIX, 'system')

    def __init__(self, name: str, level: int = 50, description: str = None):
        super(SystemRight, self).__init__(level, name, description=description)


class ManagementRight(SystemRight):
    MIN_LEVEL = BaseRight.SECURE
    MAX_LEVEL = BaseRight.DANGER
    PREFIX = '{}.{}'.format(SystemRight.PREFIX, 'management')

    def __init__(self, name: str, level: int = MIN_LEVEL, description: str = None):
        super(ManagementRight, self).__init__(name, level, description=description)


class UserRight(ManagementRight):
    MIN_LEVEL = BaseRight.SECURE
    MAX_LEVEL = BaseRight.DANGER
    PREFIX = '{}.{}'.format(ManagementRight.PREFIX, 'user')

    def __init__(self, name: str, level: int = MIN_LEVEL, description: str = None):
        super(UserRight, self).__init__(name, level, description=description)


class GroupRight(ManagementRight):
    MIN_LEVEL = BaseRight.SECURE
    MAX_LEVEL = BaseRight.DANGER
    PREFIX = '{}.{}'.format(ManagementRight.PREFIX, 'group')

    def __init__(self, name: str, level: int = MIN_LEVEL, description: str = None):
        super(GroupRight, self).__init__(name, level, description=description)
