from cmdb.object_framework.cmdb_dao import CmdbDAO


class UserManagementBase(CmdbDAO):

    COLLECTION = 'management.*'

    def __init__(self, **kwargs):
        super(UserManagementBase, self).__init__(**kwargs)
