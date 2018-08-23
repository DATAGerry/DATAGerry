from cmdb.user_management.user_base import UserManagementBase


class UserGroup(UserManagementBase):

    COLLECTION = 'management.groups'

    def __init__(self, name: str, label: str, rights: list, **kwargs):
        self.name = name
        self.label = label
        self.rights = rights
        super(UserGroup, self).__init__(**kwargs)
