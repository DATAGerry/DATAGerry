"""
Init module for web routes
"""

from flask import Flask
from cmdb.interface.config import app_config
from cmdb.utils import get_system_settings_reader
from cmdb.data_storage import get_pre_init_database
from cmdb.utils import get_logger
LOGGER = get_logger()


def create_web_app():
    import cmdb
    from cmdb.utils import get_system_config_reader
    from cmdb.object_framework import get_object_manager

    app = Flask(__name__)
    if cmdb.__MODE__:
        app.config.from_object(app_config['development'])
    else:
        app.config.from_object(app_config['production'])
    LOGGER.info('Webapp started with config mode {}'.format(app.config.get("ENV")))

    #register_filters(app)
    register_error_pages(app)
    register_blueprints(app)
    register_context_processors(app)

    system_config_reader = get_system_config_reader()
    database_manager = get_pre_init_database()

    object_manager = get_object_manager()
    system_setting_reader = get_system_settings_reader(database_manager=database_manager)

    app.obm = object_manager
    app.scr = system_config_reader
    app.ssr = system_setting_reader

    return app


def register_blueprints(app):
    from cmdb.interface.web_app.index_routes import index_pages
    app.register_blueprint(index_pages)


def register_context_processors(app):
    from cmdb.interface.web_app.context_injector import inject_current_url, inject_object_manager
    app.context_processor(inject_object_manager)


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