# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
Init module for rest routes
"""
from flask_cors import CORS

from cmdb.database.mongo_database_manager import MongoDatabaseManager

import cmdb
from cmdb.interface.cmdb_app import BaseCmdbApp
from cmdb.interface.config import app_config
from cmdb.interface.custom_converters import RegexConverter

from cmdb.interface.rest_api.responses.error_handlers import internal_server_error,\
                                                              page_gone,\
                                                              not_acceptable,\
                                                              method_not_allowed,\
                                                              page_not_found,\
                                                              forbidden,\
                                                              unauthorized,\
                                                              bad_request,\
                                                              service_unavailable
# -------------------------------------------------------------------------------------------------------------------- #

def create_rest_api(database_manager: MongoDatabaseManager):
    """TODO: document"""
    app = BaseCmdbApp(__name__, database_manager=database_manager)
    app.url_map.strict_slashes = True

    # Import App Extensions
    CORS(app=app, expose_headers=['X-API-Version', 'X-Total-Count'])

    if cmdb.__MODE__ == 'DEBUG':
        config = app_config['development']
        app.config.from_object(config)
    elif cmdb.__MODE__ == 'TESTING':
        config = app_config['testing']
        app.config.from_object(config)
    else:
        config = app_config['production']
        app.config.from_object(config)

    with app.app_context():
        register_converters(app)
        register_error_pages(app)
        register_blueprints(app)

    return app


def register_converters(app: BaseCmdbApp):
    """TODO: document"""
    app.url_map.converters['regex'] = RegexConverter


def register_blueprints(app: BaseCmdbApp):
    """TODO: document"""
    from cmdb.interface.rest_api.routes.auth_routes import auth_blueprint
    from cmdb.interface.rest_api.routes.system_routes.setup_routes import setup_blueprint
    from cmdb.interface.rest_api.routes.settings_routes.date_routes import date_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.objects_routes import objects_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.object_links_routes import links_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.types_routes import types_blueprint
    from cmdb.interface.rest_api.routes.connection import connection_routes
    from cmdb.interface.rest_api.routes.framework_routes.categories_routes import categories_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.location_routes import location_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.section_template_routes import section_template_blueprint
    from cmdb.interface.rest_api.routes.user_management_routes.users_routes import users_blueprint
    from cmdb.interface.rest_api.routes.user_management_routes.user_settings_routes import user_settings_blueprint
    from cmdb.interface.rest_api.routes.user_management_routes.groups_routes import groups_blueprint
    from cmdb.interface.rest_api.routes.user_management_routes.rights_routes import rights_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.search_routes import search_blueprint
    from cmdb.interface.rest_api.routes.exporter_routes.exporter_object_routes import exporter_blueprint
    from cmdb.interface.rest_api.routes.exporter_routes.exporter_type_routes import type_export_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.logs_routes import logs_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.setting_routes import settings_blueprint
    from cmdb.interface.rest_api.routes.importer_routes.import_routes import importer_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.docapi_routes import docapi_blueprint, docs_blueprint
    from cmdb.interface.rest_api.routes.media_library_routes.media_file_routes import media_file_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.special_routes import special_blueprint
    from cmdb.interface.rest_api.routes.report_routes.report_category_routes import report_categories_blueprint
    from cmdb.interface.rest_api.routes.report_routes.report_routes import reports_blueprint
    from cmdb.interface.rest_api.routes.webhook_routes.webhook_routes import webhook_blueprint
    from cmdb.interface.rest_api.routes.webhook_routes.webhook_event_routes import webhook_event_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(setup_blueprint, url_prefix='/setup')
    app.register_blueprint(date_blueprint, url_prefix='/date')
    app.register_blueprint(objects_blueprint, url_prefix='/objects')
    app.register_blueprint(links_blueprint, url_prefix='/objects/links')
    app.register_blueprint(types_blueprint, url_prefix='/types')
    app.register_blueprint(connection_routes)
    app.register_blueprint(categories_blueprint, url_prefix='/categories')
    app.register_blueprint(location_blueprint, url_prefix='/locations')
    app.register_blueprint(section_template_blueprint, url_prefix='/section_templates')
    app.register_blueprint(users_blueprint, url_prefix='/users')
    app.register_blueprint(user_settings_blueprint, url_prefix='/users/<int:user_id>/settings')
    app.register_blueprint(groups_blueprint, url_prefix='/groups')
    app.register_blueprint(rights_blueprint, url_prefix='/rights')
    app.register_blueprint(search_blueprint)
    app.register_blueprint(exporter_blueprint, url_prefix='/exporter')
    app.register_blueprint(type_export_blueprint)
    app.register_blueprint(logs_blueprint, url_prefix='/logs')
    app.register_blueprint(settings_blueprint)
    app.register_blueprint(importer_blueprint)
    app.register_blueprint(docapi_blueprint)
    app.register_blueprint(docs_blueprint, url_prefix='/docs')
    app.register_blueprint(media_file_blueprint)
    app.register_blueprint(special_blueprint)
    app.register_blueprint(report_categories_blueprint, url_prefix='/report_categories')
    app.register_blueprint(reports_blueprint, url_prefix='/reports')
    app.register_blueprint(webhook_blueprint, url_prefix='/webhooks')
    app.register_blueprint(webhook_event_blueprint, url_prefix='/webhook_events')

    if cmdb.__MODE__ == 'DEBUG':
        from cmdb.interface.rest_api.routes.debug_routes import debug_blueprint
        app.register_blueprint(debug_blueprint)


def register_error_pages(app: BaseCmdbApp):
    """
    Registers error handlers for the app

    Params:
        app (BaseCmdbApp): app where to register the error handlers
    """
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(406, not_acceptable)
    app.register_error_handler(410, page_gone)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(503, service_unavailable)
