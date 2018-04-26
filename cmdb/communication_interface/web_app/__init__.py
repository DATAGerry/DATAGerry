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
    from cmdb.communication_interface.web_app.index_routes import INDEX_PAGES
    from cmdb.communication_interface.web_app.static_routes import STATIC_PAGES
    from cmdb.communication_interface.web_app.objects import OBJECT_PAGES, TYPE_PAGES
    app.register_blueprint(INDEX_PAGES)
    app.register_blueprint(STATIC_PAGES)
    app.register_blueprint(OBJECT_PAGES)
    app.register_blueprint(TYPE_PAGES)


def register_context_processors(app):
    from cmdb.communication_interface.web_app.context_injector import inject_frontend_info
    app.context_processor(inject_frontend_info)


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


register_error_pages(APP)
register_blueprints(APP)
register_context_processors(APP)
