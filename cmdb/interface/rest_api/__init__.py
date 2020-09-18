# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Init module for rest routes
"""
import logging

from cmdb.framework.cmdb_log_manager import CmdbLogManager
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.exportd.exportd_job.exportd_job_manager import ExportdJobManagement
from cmdb.exportd.exportd_logs.exportd_log_manager import ExportdLogManager
from cmdb.docapi.docapi_template.docapi_template_manager import DocapiTemplateManager
from cmdb.media_library.media_file_manager import MediaFileManagement
from cmdb.user_management import UserManager
from cmdb.security.security import SecurityManager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


def create_rest_api(event_queue):
    from cmdb.interface.config import app_config
    from cmdb.utils.system_config import SystemConfigReader
    system_config_reader = SystemConfigReader()

    try:
        cache_config = {
            'DEBUG': True,
            'CACHE_TYPE': system_config_reader.get_value('name', 'Cache'),
            'CACHE_REDIS_HOST': system_config_reader.get_value('host', 'Cache'),
            'CACHE_REDIS_PORT': system_config_reader.get_value('port', 'Cache'),
            'CACHE_REDIS_PASSWORD': system_config_reader.get_value('password', 'Cache'),
        }
    except (ImportError, CMDBError) as e:
        LOGGER.debug(e.message)
        cache_config = {'CACHE_TYPE': 'simple'}
    from flask_caching import Cache

    cache = Cache(config=cache_config)

    # Create managers
    from cmdb.data_storage.database_manager import DatabaseManagerMongo
    app_database = DatabaseManagerMongo(
        **system_config_reader.get_all_values_from_section('Database')
    )
    object_manager = CmdbObjectManager(
        database_manager=app_database,
        event_queue=event_queue
    )

    log_manager = CmdbLogManager(
        database_manager=app_database
    )

    security_manager = SecurityManager(
        database_manager=app_database
    )

    user_manager = UserManager(
        database_manager=app_database
    )

    exportd_job_manager = ExportdJobManagement(
        database_manager=app_database,
        event_queue=event_queue
    )

    exportd_log_manager = ExportdLogManager(
        database_manager=app_database
    )

    media_file_manager = MediaFileManagement(
        database_manager=app_database
    )

    docapi_tpl_manager = DocapiTemplateManager(
        database_manager=app_database
    )

    # Create APP
    from cmdb.interface.cmdb_app import BaseCmdbApp

    app = BaseCmdbApp(__name__, database_manager=app_database, docapi_tpl_manager=docapi_tpl_manager,
                      media_file_manager=media_file_manager, exportd_manager=exportd_job_manager,
                      exportd_log_manager=exportd_log_manager, object_manager=object_manager,
                      log_manager=log_manager, user_manager=user_manager,
                      security_manager=security_manager)

    app.url_map.strict_slashes = True

    # Import App Extensions
    from flask_cors import CORS
    CORS(app, expose_headers=['X-API-Version', 'X-Total-Count'])
    import cmdb
    cache.init_app(app)
    cache.clear()
    app.cache = cache

    if cmdb.__MODE__ == 'DEBUG':
        app.config.from_object(app_config['rest_development'])
        LOGGER.info('RestAPI starting with config mode {}'.format(app.config.get("ENV")))
    elif cmdb.__MODE__ == 'TESTING':
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['rest'])
        LOGGER.info('RestAPI starting with config mode {}'.format(app.config.get("ENV")))

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
    from cmdb.interface.rest_api.framework_routes.object_routes import object_blueprint
    from cmdb.interface.rest_api.framework_routes.type_routes import types_blueprint
    from cmdb.interface.rest_api.auth_routes import auth_blueprint
    from cmdb.interface.rest_api.framework_routes.category_routes import categories_blueprint
    from cmdb.interface.rest_api.user_management_routes.user_routes import user_blueprint
    from cmdb.interface.rest_api.user_management_routes.right_routes import right_blueprint
    from cmdb.interface.rest_api.user_management_routes.group_routes import group_blueprint
    from cmdb.interface.rest_api.search_routes import search_blueprint
    from cmdb.interface.rest_api.exporter_routes.file_routes import file_blueprint
    from cmdb.interface.rest_api.exporter_routes.export_type_routes import type_export_blueprint
    from cmdb.interface.rest_api.log_routes import log_blueprint
    from cmdb.interface.rest_api.setting_routes import settings_blueprint
    from cmdb.interface.rest_api.import_routes import importer_blueprint
    from cmdb.interface.rest_api.exporter_routes.exportd_job_routes import exportd_job_blueprint
    from cmdb.interface.rest_api.exporter_routes.exportd_log_routes import exportd_log_blueprint
    from cmdb.interface.rest_api.external_systems_routes import external_system
    from cmdb.interface.rest_api.docapi_routes import docapi_blueprint
    from cmdb.interface.rest_api.media_library_routes.media_file_routes import media_file_blueprint
    from cmdb.interface.rest_api.special_routes import special_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(object_blueprint)
    app.register_multi_blueprint(types_blueprint, multi_prefix=['/type', '/types'])
    app.register_blueprint(connection_routes)
    app.register_multi_blueprint(categories_blueprint, multi_prefix=['/category', '/categories'])
    app.register_blueprint(user_blueprint)
    app.register_blueprint(group_blueprint)
    app.register_blueprint(right_blueprint)
    app.register_blueprint(search_blueprint)
    app.register_blueprint(file_blueprint)
    app.register_blueprint(type_export_blueprint)
    app.register_blueprint(log_blueprint)
    app.register_blueprint(settings_blueprint)
    app.register_blueprint(importer_blueprint)
    app.register_blueprint(exportd_job_blueprint)
    app.register_blueprint(exportd_log_blueprint)
    app.register_blueprint(external_system)
    app.register_blueprint(docapi_blueprint)
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
