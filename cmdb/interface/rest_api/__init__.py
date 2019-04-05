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
try:

    system_config_reader = SystemConfigReader()

    cache_config = {
        'DEBUG': True,
        'CACHE_TYPE': system_config_reader.get_value('name', 'Cache'),
        'CACHE_REDIS_HOST': system_config_reader.get_value('host', 'Cache'),
        'CACHE_REDIS_PORT': system_config_reader.get_value('port', 'Cache'),
        'CACHE_REDIS_PASSWORD': system_config_reader.get_value('password', 'Cache'),
    }
except (ImportError, CMDBError) as e:
    LOGGER.debug(e.message)
    cache_config = {'CACHE_TYPE': 'simple'}
from flask_caching import Cache

cache = Cache(config=cache_config)

CORS(app)


def create_rest_api(event_queue):
    import cmdb
    from cmdb.object_framework import CmdbObjectManager
    from cmdb.data_storage.database_manager import DatabaseManagerMongo
    from cmdb.data_storage.database_connection import MongoConnector

    cache.init_app(app)
    cache.clear()

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
        LOGGER.info('RestAPI starting with config mode {}'.format(app.config.get("ENV")))
    elif cmdb.__MODE__ == 'TESTING':
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['rest'])
        LOGGER.info('RestAPI starting with config mode {}'.format(app.config.get("ENV")))

    MANAGER_HOLDER.set_database_manager(database_manager)
    MANAGER_HOLDER.set_security_manager(security_manager)
    MANAGER_HOLDER.set_object_manager(object_manager)
    MANAGER_HOLDER.set_user_manager(user_manager)
    MANAGER_HOLDER.set_event_queue(event_queue)
    MANAGER_HOLDER.set_system_settings_reader(system_settings_reader)
    MANAGER_HOLDER.set_system_settings_writer(system_settings_writer)
    MANAGER_HOLDER.init_app(app)

    with app.app_context():
        register_converters()
        register_error_pages()
        register_blueprints()

    return app


def register_converters():
    from cmdb.interface.custom_converters import DictConverter
    app.url_map.converters['dict'] = DictConverter


def register_blueprints():
    from cmdb.interface.rest_api.connection import connection_routes
    from cmdb.interface.rest_api.object_routes import object_rest
    from cmdb.interface.rest_api.type_routes import type_rest
    from cmdb.interface.rest_api.auth_routes import auth_routes
    from cmdb.interface.rest_api.category_routes import categories_routes
    from cmdb.interface.rest_api.user_management.user_routes import user_routes
    from cmdb.interface.rest_api.user_management.right_routes import right_routes
    from cmdb.interface.rest_api.user_management.group_routes import group_routes
    from cmdb.interface.rest_api.settings_routes import settings_rest
    app.register_blueprint(auth_routes)
    app.register_blueprint(object_rest)
    app.register_blueprint(type_rest)
    app.register_blueprint(connection_routes)
    app.register_blueprint(categories_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(group_routes)
    app.register_blueprint(right_routes)
    app.register_blueprint(settings_rest)


def register_error_pages():
    from cmdb.interface.rest_api.error_routes import page_not_found, method_not_allowed, not_acceptable, \
        internal_server_error, unauthorized_user, bad_request, forbidden, page_gone, not_implemented
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized_user)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(406, not_acceptable)
    app.register_error_handler(410, page_gone)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(501, not_implemented)
