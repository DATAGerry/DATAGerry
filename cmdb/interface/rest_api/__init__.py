"""
Init module for rest routes
"""
from flask import Flask
from cmdb.interface.config import app_config
from cmdb.utils import get_logger
LOGGER = get_logger()


def create_rest_api():
    import cmdb
    from cmdb.object_framework import CmdbObjectManager
    from cmdb.data_storage.database_manager import DatabaseManagerMongo
    from cmdb.data_storage.database_connection import MongoConnector
    from cmdb.utils import SystemConfigReader

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

    app = Flask(__name__)
    if cmdb.__MODE__ == 'DEBUG':
        app.config.from_object(app_config['rest_development'])
        LOGGER.info('RestAPI starting with config mode {}'.format(app.config.get("ENV")))
    elif cmdb.__MODE__ == 'TESTING':
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['rest'])
        LOGGER.info('RestAPI starting with config mode {}'.format(app.config.get("ENV")))

    app.obm = object_manager
    register_blueprints(app)
    register_error_pages(app)
    return app


def register_blueprints(app):
    from cmdb.interface.rest_api.object_routes import object_rest
    app.register_blueprint(object_rest)


def register_error_pages(app):
    from cmdb.interface.rest_api.error_routes import page_not_found, method_not_allowed, not_acceptable, \
        conflict, internal_server_error
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(406, not_acceptable)
    app.register_error_handler(409, conflict)
    app.register_error_handler(500, internal_server_error)
