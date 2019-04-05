"""
Init module for rest routes
"""
import logging
from flask_cors import CORS

from cmdb.interface.cmdb_app import CmdbManagerHolder, BaseCmdbApp
from cmdb.interface.config import app_config
from cmdb.user_management.user_manager import UserManagement
from cmdb.utils import SecurityManager, SystemSettingsReader, SystemSettingsWriter
from cmdb.utils.system_reader import SystemConfigReader

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
MANAGER_HOLDER = CmdbManagerHolder()
app = BaseCmdbApp(__name__, MANAGER_HOLDER)
CORS(app)
system_config_reader = SystemConfigReader()


def create_app(event_queue):
    import cmdb
    from cmdb.object_framework import CmdbObjectManager
    from cmdb.data_storage.database_manager import DatabaseManagerMongo
    from cmdb.data_storage.database_connection import MongoConnector

    database_manager = DatabaseManagerMongo(
        MongoConnector(
            host=system_config_reader.get_value('host', 'Database'),
            port=int(system_config_reader.get_value('port', 'Database')),
            database_name=system_config_reader.get_value('database_name', 'Database')
        )
    )

    object_manager = CmdbObjectManager(
        database_manager=database_manager,
        event_queue=event_queue
    )

    security_manager = SecurityManager(database_manager)

    user_manager = UserManagement(
        database_manager=database_manager,
        security_manager=security_manager
    )

    system_settings_reader = SystemSettingsReader(
        database_manager=database_manager
    )

    system_settings_writer = SystemSettingsWriter(
        database_manager=database_manager
    )

    if cmdb.__MODE__ == 'DEBUG':
        app.config.from_object(app_config['rest_development'])
        LOGGER.info('NetAPP starting with config mode {}'.format(app.config.get("ENV")))
    elif cmdb.__MODE__ == 'TESTING':
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['rest'])
        LOGGER.info('NetAPP starting with config mode {}'.format(app.config.get("ENV")))

    MANAGER_HOLDER.set_database_manager(database_manager)
    MANAGER_HOLDER.set_security_manager(security_manager)
    MANAGER_HOLDER.set_object_manager(object_manager)
    MANAGER_HOLDER.set_user_manager(user_manager)
    MANAGER_HOLDER.set_event_queue(event_queue)
    MANAGER_HOLDER.set_system_settings_reader(system_settings_reader)
    MANAGER_HOLDER.set_system_settings_writer(system_settings_writer)
    MANAGER_HOLDER.init_app(app)

    return app



