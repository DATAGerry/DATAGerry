from cmdb.user_management.user_right import BaseRight


class SystemRight(BaseRight):

    MIN_LEVEL = 50
    PREFIX = 'system'

    def __init__(self, name: str, level: int = 50):
        super(SystemRight, self).__init__(level, name)
