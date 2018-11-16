from cmdb.user_management.user_base import UserManagementBase


class UserRight(UserManagementBase):

    COLLECTION = 'management.rights'

    IGNORED_INIT_KEYS = [
        'public_id'
    ]
    INDEX_KEYS = [
        {'keys': [('name', UserManagementBase.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    CRITICAL = 100
    SECURE = 50
    PERMISSION = 10
    NOTSET = 0

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

    def __init__(self, name, level, **kwargs):
        self.name = name
        self.level = level
        super(UserRight, self).__init__(**kwargs)

    def get_name(self):
        return self.name

    def get_level_name(self):
        return UserRight._levelToName[self.level]

    def get_level(self):
        return self.level

