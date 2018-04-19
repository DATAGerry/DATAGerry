from cmdb.user_management.user_dao import UserManagementSetup, UserManagementBase


class UserGroupSetup(UserManagementSetup):

    def setup(self):
        for group in UserGroupSetup.get_setup_data():
            self.dbm.insert(group.to_mongo(), UserGroup.COLLECTION)

    @staticmethod
    def get_setup_data():
        default_groups = [
            UserGroup('admin', [
                'view_object',
                'create_object',
                'edit_object',
                'delete_object',
                'see_secret',
                'export_object',
                'admin_config',
                'rest_connection'
            ]),
            UserGroup('user', [
                'view_object',
                'create_object',
                'edit_object',
                'delete_object',
                'export_object',
            ]),
            UserGroup('rest', [
                'view_object',
                'export_object',
                'rest_connection'
            ])
        ]
        return default_groups


class UserGroup(UserManagementBase):

    COLLECTION = 'management.groups'
    SETUP_CLASS = UserGroupSetup

    def __init__(self, name, rights, _id=None):
        self._id = _id
        self.name = name
        self.rights = rights

    def add_right(self, right_name):
        self.rights.append(right_name)

