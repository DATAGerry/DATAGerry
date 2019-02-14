from cmdb.user_management.user_right import BaseRight


class FrameworkRight(BaseRight):

    def __init__(self, name: str, level: int = 10):
        super(FrameworkRight, self).__init__(level, name)


class ObjectRight(FrameworkRight):

    MIN_LEVEL = 10
    MAX_LEVEL = 50
    PREFIX = 'object'

    def __init__(self, name: str, level: int = 10):
        super(ObjectRight, self).__init__(name, level)


class TypeRight(FrameworkRight):

    MIN_LEVEL = 50
    MAX_LEVEL = 100
    PREFIX = 'type'

    def __init__(self, name: str, level: int = 50):
        super(TypeRight, self).__init__(name, level)

