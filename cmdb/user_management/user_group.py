from cmdb.user_management.user_base import UserManagementBase
from cmdb.utils.error import CMDBError


class UserGroup(UserManagementBase):
    COLLECTION = 'management.groups'

    INDEX_KEYS = [
        {'keys': [('name', UserManagementBase.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, name: str, label: str = None, rights: list = None, **kwargs):
        self.name = name
        self.label = label or name.title()
        self.rights = rights or []
        super(UserGroup, self).__init__(**kwargs)

    def get_name(self):
        return self.name

    def get_label(self):
        return self.label

    def set_rights(self, rights: list):
        self.rights = rights

    def get_rights(self):
        return self.rights

    def get_right(self, name):
        try:
            return self.rights[self.rights.index(name)]
        except (IndexError, TypeError, ValueError):
            raise RightNotFoundError(self.name, name)

    def has_right(self, name):
        try:
            self.get_right(name)
        except RightNotFoundError:
            return False
        return True


class RightNotFoundError(CMDBError):
    def __init__(self, group, right):
        super().__init__()
        self.message = "Right was not found inside this group Groupname: {} | Rightname: {}".format(group, right)
