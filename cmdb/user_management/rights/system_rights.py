from cmdb.user_management.user_right import BaseRight


class SystemRight(BaseRight):
    MIN_LEVEL = 50
    PREFIX = '{}.{}'.format(BaseRight.PREFIX, 'system')

    def __init__(self, name: str, level: int = 50, description: str = None):
        super(SystemRight, self).__init__(level, name, description=description)
