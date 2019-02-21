from cmdb.user_management.user_right import BaseRight


class FrameworkRight(BaseRight):
    PREFIX = '{}.{}'.format(BaseRight.PREFIX, 'framework')

    def __init__(self, name: str, level: int = 10, description: str = None):
        super(FrameworkRight, self).__init__(level, name, description=description)


class ObjectRight(FrameworkRight):
    MIN_LEVEL = 10
    MAX_LEVEL = 50
    PREFIX = '{}.{}'.format(FrameworkRight.PREFIX, 'object')

    def __init__(self, name: str, level: int = 10, description: str = None):
        super(ObjectRight, self).__init__(name, level, description=description)


class TypeRight(FrameworkRight):
    MIN_LEVEL = 50
    MAX_LEVEL = 100
    PREFIX = '{}.{}'.format(FrameworkRight.PREFIX, 'type')

    def __init__(self, name: str, level: int = 50, description: str = None):
        super(TypeRight, self).__init__(name, level, description=description)
