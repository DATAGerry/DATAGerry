from cmdb.object_framework import CmdbObjectManager
from cmdb.user_management import UserManagement
from cmdb.data_storage import DatabaseManagerMongo
from cmdb.utils import SecurityManager


class CmdbManagerHolder:

    def __init__(self):
        self.database_manager = None
        self.object_manager = None
        self.user_manager = None
        self.security_manager = None

    def set_database_manager(self, database_manager: DatabaseManagerMongo):
        self.database_manager = database_manager

    def set_object_manager(self, object_manager: CmdbObjectManager):
        self.object_manager = object_manager

    def set_user_manager(self, user_manager: UserManagement):
        self.user_manager = user_manager

    def set_security_manager(self, security_manager: SecurityManager):
        self.security_manager = security_manager

    def get_database_manager(self) ->DatabaseManagerMongo:
        return self.database_manager

    def get_object_manager(self) ->CmdbObjectManager:
        return self.object_manager

    def get_user_manager(self) ->UserManagement:
        return self.user_manager

    def get_security_manager(self) ->SecurityManager:
        return self.security_manager

    def init_app(self, app):
        app.manager_holder = self
