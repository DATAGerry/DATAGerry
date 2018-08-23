"""
Init module for rest routes
"""
from flask import Flask
from cmdb.interface.config import app_config
from cmdb.utils import get_logger
LOGGER = get_logger()


def create_rest_api():
    import cmdb
    from cmdb.object_framework import get_object_manager

    app = Flask(__name__)
    if cmdb.__DEBUG__:
        app.config.from_object(app_config['rest_development'])
    else:
        app.config.from_object(app_config['rest'])
    LOGGER.info('RestAPI started with config mode {}'.format(app.config.get("ENV")))
    app.obm = get_object_manager()
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
