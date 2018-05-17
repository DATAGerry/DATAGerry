"""
Init module for web routes
"""
from flask import Flask

APP = Flask(__name__)
APP.debug = True


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


register_filters(APP)
register_error_pages(APP)
register_blueprints(APP)
register_context_processors(APP)
