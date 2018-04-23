from cmdb.user_management.user_dao import UserManagementSetup, UserManagementBase


class UserRightSetup(UserManagementSetup):

    def setup(self):
        for right in UserRightSetup.get_setup_data():
            self.dbm.insert(right.to_mongo(), UserRight.COLLECTION)

    @staticmethod
    def get_setup_data():
        default_rights = [
            UserRight('view_object', UserRight.NOTSET),
            UserRight('create_object', UserRight.PERMISSION),
            UserRight('edit_object', UserRight.PERMISSION),
            UserRight('delete_object', UserRight.SECURE),
            UserRight('see_secret', UserRight.CRITICAL),
            UserRight('export_object', UserRight.SECURE),
            UserRight('admin_config', UserRight.CRITICAL),
            UserRight('rest_connection', UserRight.PERMISSION)
        ]
        return default_rights


class UserRight(UserManagementBase):

    COLLECTION = 'management.rights'
    SETUP_CLASS = UserRightSetup

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

    def __init__(self, name, level, _id=None):
        """
        Args:
            name: right name
            level: right security level
            _id: database id
        """
        self._id = _id
        self.name = name
        self.level = level

    def get_name(self):
        """
        Returns: right name

        """
        return self.name

    def get_level_name(self):
        """
        Returns: level as name

        """
        return UserRight._levelToName[self.level]

    def get_level(self):
        """
        Returns: level as number

        """
        return self.level

