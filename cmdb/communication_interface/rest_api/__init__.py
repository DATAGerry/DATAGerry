"""
Init module for rest routes
"""
from flask import Flask

from cmdb.communication_interface.config import app_config
from cmdb.data_storage import init_database


def create_rest_api():
    from cmdb.object_framework import CmdbObjectManager
    from cmdb.application_utils import get_system_config_reader, get_system_settings_reader

    app = Flask(__name__)
    app.debug = True
    system_config_reader = get_system_config_reader()
    database_manager = init_database()

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