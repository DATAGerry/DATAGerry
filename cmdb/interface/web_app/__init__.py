"""
Init module for web routes
"""

from flask import Flask
from cmdb.interface.cmdb_holder import CmdbManagerHolder
from cmdb.interface.config import app_config
from cmdb.utils import get_logger
LOGGER = get_logger()
MANAGER_HOLDER = CmdbManagerHolder()


def create_web_app():
    import cmdb

    app = Flask(__name__)
    if cmdb.__MODE__:
        app.config.from_object(app_config['development'])
    else:
        app.config.from_object(app_config['production'])
    LOGGER.info('Webapp started with config mode {}'.format(app.config.get("ENV")))

    from cmdb.object_framework import CmdbObjectManager
    from cmdb.data_storage.database_manager import DatabaseManagerMongo
    from cmdb.data_storage.database_connection import MongoConnector
    from cmdb.utils.security import SecurityManager
    from cmdb.user_management import UserManagement
    from cmdb.utils import SystemConfigReader, SystemSettingsReader, SystemSettingsWriter
    from flask_breadcrumbs import Breadcrumbs

    system_config_reader = SystemConfigReader(
        config_name=SystemConfigReader.DEFAULT_CONFIG_NAME,
        config_location=SystemConfigReader.DEFAULT_CONFIG_LOCATION
    )

    database_manager = DatabaseManagerMongo(
        MongoConnector(
            host=system_config_reader.get_value('host', 'Database'),
            port=int(system_config_reader.get_value('port', 'Database')),
            database_name=system_config_reader.get_value('database_name', 'Database')
        )
    )

    object_manager = CmdbObjectManager(
        database_manager=database_manager
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

    MANAGER_HOLDER.set_database_manager(database_manager)
    MANAGER_HOLDER.set_security_manager(security_manager)
    MANAGER_HOLDER.set_object_manager(object_manager)
    MANAGER_HOLDER.set_user_manager(user_manager)
    MANAGER_HOLDER.set_system_settings_reader(system_settings_reader)
    MANAGER_HOLDER.set_system_settings_writer(system_settings_writer)
    MANAGER_HOLDER.init_app(app)

    # register_filters(app)
    with app.app_context():
        register_error_pages(app=app)
        register_blueprints(app=app)
        register_context_processors(app=app)
        Breadcrumbs(app=app)

    return app


def register_blueprints(app):
    from cmdb.interface.web_app.index_routes import index_pages
    from cmdb.interface.web_app.static_routes import static_pages
    from cmdb.interface.web_app.auth_routes import auth_pages
    from cmdb.interface.web_app.settings_routes import settings_pages
    from cmdb.interface.web_app.object_routes import object_pages

    app.register_blueprint(index_pages)
    app.register_blueprint(static_pages)
    app.register_blueprint(auth_pages)
    app.register_blueprint(settings_pages)
    app.register_blueprint(object_pages)


def register_context_processors(app):
    from cmdb.interface.web_app.context_injector import inject_current_url, inject_object_manager, inject_sidebar
    app.context_processor(inject_sidebar)


def register_error_pages(app):
    from cmdb.interface.web_app.error_routes import bad_request, unauthorized_user, \
        forbidden, page_not_found, page_gone, iam_a_teapot, internal_server_error
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized_user)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(410, page_gone)
    app.register_error_handler(418, iam_a_teapot)
    app.register_error_handler(500, internal_server_error)