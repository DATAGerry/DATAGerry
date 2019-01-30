from cmdb.object_framework import CmdbObjectManager
from cmdb.user_management.user_manager import UserManagement
from cmdb.data_storage import DatabaseManagerMongo
from cmdb.utils import SecurityManager
from cmdb.event_management.event_manager import EventManager
from cmdb.utils import SystemSettingsReader, SystemSettingsWriter


class CmdbManagerHolder:

    def __init__(self):
        self.database_manager = None
        self.object_manager = None
        self.user_manager = None
        self.event_queue = None
        self.security_manager = None
        self.system_settings_reader = None
        self.system_settings_writer = None

    def set_database_manager(self, database_manager: DatabaseManagerMongo):
        self.database_manager = database_manager

    def set_object_manager(self, object_manager: CmdbObjectManager):
        self.object_manager = object_manager

    def set_user_manager(self, user_manager: UserManagement):
        self.user_manager = user_manager

    def set_security_manager(self, security_manager: SecurityManager):
        self.security_manager = security_manager

    def set_event_queue(self, event_queue):
        self.event_queue = event_queue

    def set_system_settings_reader(self, system_settings_reader: SystemSettingsReader):
        self.system_settings_reader = system_settings_reader

    def set_system_settings_writer(self, system_settings_writer: SystemSettingsWriter):
        self.system_settings_writer = system_settings_writer

    def get_database_manager(self) ->DatabaseManagerMongo:
        return self.database_manager

    def get_object_manager(self) ->CmdbObjectManager:
        return self.object_manager

    def get_user_manager(self) ->UserManagement:
        return self.user_manager

    def get_security_manager(self) ->SecurityManager:
        return self.security_manager

    def get_event_queue(self):
        return self.event_queue

    def get_system_settings_reader(self) ->SystemSettingsReader:
        return self.system_settings_reader

    def get_system_settings_writer(self) ->SystemSettingsWriter:
        return self.system_settings_writer

    def init_app(self, app):
        app.manager_holder = self
