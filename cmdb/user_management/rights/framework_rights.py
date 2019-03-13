from cmdb.user_management.user_right import BaseRight


class FrameworkRight(BaseRight):
    MIN_LEVEL = BaseRight.PERMISSION
    PREFIX = '{}.{}'.format(BaseRight.PREFIX, 'framework')

    def __init__(self, name: str, level: int = MIN_LEVEL, description: str = None):
        super(FrameworkRight, self).__init__(level, name, description=description)


class ObjectRight(FrameworkRight):
    MIN_LEVEL = BaseRight.PERMISSION
    MAX_LEVEL = BaseRight.SECURE
    PREFIX = '{}.{}'.format(FrameworkRight.PREFIX, 'object')

    def __init__(self, name: str, level: int = MIN_LEVEL, description: str = None):
        super(ObjectRight, self).__init__(name, level, description=description)


class TypeRight(FrameworkRight):
    MIN_LEVEL = BaseRight.PROTECTED
    MAX_LEVEL = BaseRight.CRITICAL
    PREFIX = '{}.{}'.format(FrameworkRight.PREFIX, 'type')

    def __init__(self, name: str, level: int = 50, description: str = None):
        super(TypeRight, self).__init__(name, level, description=description)


class CategoryRight(FrameworkRight):
    MIN_LEVEL = BaseRight.PROTECTED
    MAX_LEVEL = BaseRight.SECURE
    PREFIX = '{}.{}'.format(FrameworkRight.PREFIX, 'category')

    def __init__(self, name: str, level: int = BaseRight.PROTECTED, description: str = None):
        super(CategoryRight, self).__init__(name, level, description=description)
