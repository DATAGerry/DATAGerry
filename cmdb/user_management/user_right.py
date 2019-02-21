from cmdb.utils.error import CMDBError
from cmdb.utils.logger import get_logger

LOGGER = get_logger()

GLOBAL_IDENTIFIER = 'global'


class BaseRight:
    MIN_LEVEL = 0
    MAX_LEVEL = 100

    CRITICAL = 100
    SECURE = 50
    PERMISSION = 10
    NOTSET = 0

    PREFIX = 'base'

    _levelToName = {
        CRITICAL: 'CRITICAL',
        SECURE: 'SECURE',
        PERMISSION: 'PERMISSION',
        NOTSET: 'NOTSET',
    }
    _nameToLevel = {
        'CRITICAL': CRITICAL,
        'SECURE': SECURE,
        'PERMISSION': PERMISSION,
        'NOTSET': NOTSET,
    }

    def __init__(self, level: int, name: str, label: str = None, description: str = None):
        self.level = level
        self.name = '{}.{}'.format(self.PREFIX, name)
        self.label = label or None
        self.description = description or "No description"

    def get_prefix(self):
        return self.PREFIX.split('.')[-1]

    def get_name(self):
        return self.name

    def get_label(self):
        return self.label or "{}.{}".format(self.get_prefix(), self.name.split('.')[-1])

    def get_description(self):
        return self.description

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if value not in BaseRight._levelToName:
            raise InvalidLevelRightError(value)
        if value < self.MIN_LEVEL:
            raise PoorlyLevelRightError(value, self.MIN_LEVEL)
        if value > self.MAX_LEVEL:
            raise MaxLevelRightError(value, self.MAX_LEVEL)
        self._level = value

    def get_level(self):
        return self.level

    def get_level_name(self):
        return BaseRight._levelToName[self.level]

    def __repr__(self):
        from cmdb.utils.helpers import debug_print
        return debug_print(self)


class InvalidLevelRightError(CMDBError):
    def __init__(self, level):
        self.message = 'Invalid right level - Level {} does not exist.'.format(level)
        super().__init__()


class PoorlyLevelRightError(CMDBError):
    def __init__(self, level, min_level):
        self.message = 'The minimum level for the right has been violated. Level was {0}, expected at least {1}'.format(
            level, min_level)


class MaxLevelRightError(CMDBError):
    def __init__(self, level, max_level):
        self.message = 'The maximum level for the right has been violated. Level was {0}, expected at most {1}'.format(
            level, max_level)
