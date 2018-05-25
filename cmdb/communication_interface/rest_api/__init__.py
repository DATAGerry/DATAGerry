"""
Init module for rest routes
"""
from flask import Flask

from cmdb.communication_interface.config import app_config


def create_rest_api():
    from cmdb.object_framework import CmdbObjectManager
    from cmdb.data_storage import DatabaseManagerMongo, MongoConnector
    from cmdb.application_utils import get_system_config_reader, get_system_settings_reader

    app = Flask(__name__)
    app.debug = True
    system_config_reader = get_system_config_reader()
    database_manager = DatabaseManagerMongo(
        connector=MongoConnector(
            host=system_config_reader.get_value('host', 'Database'),
            port=int(system_config_reader.get_value('port', 'Database')),
            database_name=system_config_reader.get_value('database_name', 'Database'),
            timeout=MongoConnector.DEFAULT_CONNECTION_TIMEOUT
        )
    )
    object_manager = CmdbObjectManager(database_manager=database_manager)
    system_setting_reader = get_system_settings_reader(database_manager=database_manager)

    app = Flask(__name__)
    app.config.from_object(app_config['rest_development'])
    app.dbm = database_manager
    app.obm = object_manager
    app.scr = system_config_reader
    app.ssr = system_setting_reader

    register_blueprints(app)
    register_error_pages(app)

    return app


def register_blueprints(app):
    from cmdb.communication_interface.rest_api.type_routes import type_rest
    from cmdb.communication_interface.rest_api.object_routes import object_rest
    app.register_blueprint(type_rest)
    app.register_blueprint(object_rest)


def register_error_pages(app):
    from cmdb.communication_interface.rest_api.error_routes import page_not_found, not_acceptable
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(406, not_acceptable)
