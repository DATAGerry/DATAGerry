# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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

from cmdb.interface.cmdb_app import BaseCmdbApp
from cmdb.interface.config import app_config


def create_rest_api(database_manager, event_queue):
    app = BaseCmdbApp(__name__, database_manager=database_manager, event_queue=event_queue)
    app.url_map.strict_slashes = True

    # Import App Extensions
    CORS(app, expose_headers=['X-API-Version', 'X-Total-Count'])

    import cmdb
    if cmdb.__MODE__ == 'DEBUG':
        config = app_config['development']
        config.APPLICATION_ROOT = '/rest/'
        app.config.from_object(config)
    elif cmdb.__MODE__ == 'TESTING':
        config = app_config['testing']
        config.APPLICATION_ROOT = '/rest/'
        app.config.from_object(config)
    else:
        config = app_config['production']
        config.APPLICATION_ROOT = '/rest/'
        app.config.from_object(config)

    with app.app_context():
        register_converters(app)
        register_error_pages(app)
        register_blueprints(app)

    return app


def register_converters(app):
    from cmdb.interface.custom_converters import RegexConverter
    app.url_map.converters['regex'] = RegexConverter


def register_blueprints(app):
    from cmdb.interface.rest_api.connection import connection_routes
    from cmdb.interface.rest_api.framework_routes.object_routes import objects_blueprint
    from cmdb.interface.rest_api.framework_routes.type_routes import types_blueprint
    from cmdb.interface.rest_api.auth_routes import auth_blueprint
    from cmdb.interface.rest_api.settings_routes.date_routes import date_blueprint
    from cmdb.interface.rest_api.framework_routes.category_routes import categories_blueprint

    from cmdb.interface.rest_api.user_management_routes.user_routes import users_blueprint
    from cmdb.interface.rest_api.user_management_routes.user_settings_routes import user_settings_blueprint
    from cmdb.interface.rest_api.user_management_routes.right_routes import rights_blueprint
    from cmdb.interface.rest_api.user_management_routes.group_routes import groups_blueprint

    from cmdb.interface.rest_api.search_routes import search_blueprint
    from cmdb.interface.rest_api.exporter_routes.exporter_object_routes import exporter_blueprint
    from cmdb.interface.rest_api.exporter_routes.exporter_type_routes import type_export_blueprint
    from cmdb.interface.rest_api.log_routes import log_blueprint
    from cmdb.interface.rest_api.setting_routes import settings_blueprint
    from cmdb.interface.rest_api.import_routes import importer_blueprint
    from cmdb.interface.rest_api.exporter_routes.exporter_object_routes import exporter_blueprint
    from cmdb.interface.rest_api.exporter_routes.exporter_type_routes import type_export_blueprint
    from cmdb.interface.rest_api.exportd_routes import exportd_blueprint

    from cmdb.interface.rest_api.exportd_routes.exportd_job_routes import exportd_job_blueprint
    from cmdb.interface.rest_api.exportd_routes.exportd_log_routes import exportd_log_blueprint

    from cmdb.interface.rest_api.external_systems_routes import external_system
    from cmdb.interface.rest_api.docapi_routes import docapi_blueprint, docs_blueprint
    from cmdb.interface.rest_api.media_library_routes.media_file_routes import media_file_blueprint
    from cmdb.interface.rest_api.special_routes import special_blueprint

    from cmdb.interface.rest_api.framework_routes.object_link_routes import links_blueprint

    app.register_multi_blueprint(auth_blueprint, multi_prefix=['/auth'])
    app.register_multi_blueprint(date_blueprint, multi_prefix=['/date'])
    app.register_multi_blueprint(objects_blueprint, multi_prefix=['/object', '/objects'])
    app.register_multi_blueprint(links_blueprint, multi_prefix=['/object/link', '/objects/links'])
    app.register_multi_blueprint(types_blueprint, multi_prefix=['/type', '/types'])
    app.register_blueprint(connection_routes)

    app.register_multi_blueprint(categories_blueprint, multi_prefix=['/category', '/categories'])
    app.register_multi_blueprint(users_blueprint, multi_prefix=['/user', '/users'])
    app.register_blueprint(user_settings_blueprint, url_prefix='/users/<int:user_id>/settings')

    app.register_multi_blueprint(groups_blueprint, multi_prefix=['/group', '/groups'])
    app.register_multi_blueprint(rights_blueprint, multi_prefix=['/right', '/rights'])
    app.register_blueprint(search_blueprint)
    app.register_multi_blueprint(exporter_blueprint, multi_prefix=['/exporter', '/exporter/'])
    app.register_blueprint(type_export_blueprint)
    app.register_multi_blueprint(log_blueprint, multi_prefix=['/log', '/logs'])
    app.register_blueprint(settings_blueprint)
    app.register_blueprint(importer_blueprint)
    app.register_multi_blueprint(exportd_blueprint, multi_prefix=['/exportd'])
    app.register_blueprint(exportd_job_blueprint)
    app.register_blueprint(exportd_log_blueprint)
    app.register_blueprint(external_system)
    app.register_blueprint(docapi_blueprint)
    app.register_multi_blueprint(docs_blueprint, multi_prefix=['/docs', '/doc'])
    app.register_blueprint(media_file_blueprint)
    app.register_blueprint(special_blueprint)

    import cmdb
    if cmdb.__MODE__ == 'DEBUG':
        from cmdb.interface.rest_api.debug_routes import debug_blueprint
        app.register_blueprint(debug_blueprint)


def register_error_pages(app):
    from cmdb.interface.error_handlers import not_implemented
    from cmdb.interface.error_handlers import internal_server_error
    from cmdb.interface.error_handlers import page_gone
    from cmdb.interface.error_handlers import not_acceptable
    from cmdb.interface.error_handlers import method_not_allowed
    from cmdb.interface.error_handlers import page_not_found
    from cmdb.interface.error_handlers import forbidden
    from cmdb.interface.error_handlers import unauthorized
    from cmdb.interface.error_handlers import bad_request
    from cmdb.interface.error_handlers import service_unavailable

    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(406, not_acceptable)
    app.register_error_handler(410, page_gone)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(501, not_implemented)
    app.register_error_handler(503, service_unavailable)
