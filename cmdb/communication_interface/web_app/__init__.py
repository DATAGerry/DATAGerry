"""
Init module for web routes
"""
from flask import Flask


def create_web_app():
    from cmdb.object_framework import CmdbObjectManager
    from cmdb.data_storage import DatabaseManagerMongo, MongoConnector
    from cmdb.application_utils import get_system_config_reader, get_system_settings_reader

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
    app.debug = True
    app.dbm = database_manager
    app.obm = object_manager
    app.scr = system_config_reader
    app.ssr = system_setting_reader

    register_filters(app)
    register_error_pages(app)
    register_blueprints(app)
    register_context_processors(app)

    return app


def register_blueprints(app):
    """
    registers blueprints
    :param app: flask app
    :return:
    """
    from cmdb.communication_interface.web_app.index_routes import index_pages
    from cmdb.communication_interface.web_app.static_routes import static_pages
    app.register_blueprint(index_pages)
    app.register_blueprint(static_pages)


def register_context_processors(app):
    from cmdb.communication_interface.web_app.context_injector import inject_frontend_info, inject_current_url, \
        inject_sidebar, inject_object_manager
    app.context_processor(inject_object_manager)
    app.context_processor(inject_frontend_info)
    app.context_processor(inject_current_url)
    app.context_processor(inject_sidebar)


def register_filters(app):
    from cmdb.communication_interface.web_app.filters import label_active, default_cat_icon
    from cmdb.communication_interface.web_app.utils import url_for_other_page
    app.jinja_env.filters['label_active'] = label_active
    app.jinja_env.filters['default_cat_icon'] = default_cat_icon
    app.jinja_env.globals['url_for_other_page'] = url_for_other_page


def register_error_pages(app):
    """
    registers error pages
    :param app: flask app
    :return:
    """
    from cmdb.communication_interface.web_app.error_routes import bad_request, unauthorized_user, \
        forbidden, page_not_found, page_gone, iam_a_teapot, internal_server_error

    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized_user)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(410, page_gone)
    app.register_error_handler(418, iam_a_teapot)
    app.register_error_handler(500, internal_server_error)


