from cmdb.user_management.user_base import UserManagementBase


class UserGroup(UserManagementBase):

    COLLECTION = 'management.groups'

    INDEX_KEYS = [
        {'keys': [('name', UserManagementBase.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, name: str, label: str, rights: list=None, **kwargs):
        self.name = name
        self.label = label
        self.rights = rights or []
        super(UserGroup, self).__init__(**kwargs)

    def get_name(self):
        return self.name

    def get_label(self):
        return self.label

    def get_rights(self):
        return self.rights
