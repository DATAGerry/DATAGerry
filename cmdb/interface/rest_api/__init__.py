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
from cmdb.user_management import UserManager
from cmdb.utils import SecurityManager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


def create_rest_api(event_queue):
    from cmdb.interface.config import app_config
    from cmdb.utils.system_reader import SystemConfigReader
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

    # Create manager
    from cmdb.data_storage.database_manager import DatabaseManagerMongo, MongoConnector
    app_database = DatabaseManagerMongo(
        connector=MongoConnector(
            **system_config_reader.get_all_values_from_section('Database')
        )
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
        database_manager=app_database,
        security_manager=security_manager
    )

    exportd_job_manager = ExportdJobManagement(
        database_manager=app_database,
        event_queue=event_queue
    )

    # Create APP
    from cmdb.interface.cmdb_app import BaseCmdbApp

    app = BaseCmdbApp(__name__, database_manager=app_database, exportd_manager=exportd_job_manager,
                      object_manager=object_manager, log_manager=log_manager, user_manager=user_manager,
                      security_manager=security_manager)

    # Import App Extensions
    from flask_cors import CORS
    CORS(app)
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
    from cmdb.interface.custom_converters import DictConverter
    app.url_map.converters['dict'] = DictConverter


def register_blueprints(app):
    from cmdb.interface.rest_api.connection import connection_routes
    from cmdb.interface.rest_api.framework_routes.object_routes import object_blueprint
    from cmdb.interface.rest_api.framework_routes.type_routes import type_blueprint
    from cmdb.interface.rest_api.auth_routes import auth_blueprint
    from cmdb.interface.rest_api.framework_routes.category_routes import categories_blueprint
    from cmdb.interface.rest_api.user_management_routes.user_routes import user_blueprint
    from cmdb.interface.rest_api.user_management_routes.right_routes import right_blueprint
    from cmdb.interface.rest_api.user_management_routes.group_routes import group_blueprint
    from cmdb.interface.rest_api.search_routes import search_blueprint
    from cmdb.interface.rest_api.exporter_routes.file_routes import file_blueprint
    from cmdb.interface.rest_api.exporter_routes.export_type_routes import type_export_blueprint
    from cmdb.interface.rest_api.framework_routes.status_routes import status_blueprint
    from cmdb.interface.rest_api.framework_routes.collection_routes import collection_blueprint
    from cmdb.interface.rest_api.log_routes import log_blueprint
    from cmdb.interface.rest_api.setting_routes import settings_blueprint
    from cmdb.interface.rest_api.import_routes import importer_blueprint
    from cmdb.interface.rest_api.exporter_routes.exportd_job_routes import exportd_job_blueprint
    from cmdb.interface.rest_api.external_systems_routes import external_system

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(object_blueprint)
    app.register_blueprint(type_blueprint)
    app.register_blueprint(connection_routes)
    app.register_blueprint(categories_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(group_blueprint)
    app.register_blueprint(right_blueprint)
    app.register_blueprint(search_blueprint)
    app.register_blueprint(file_blueprint)
    app.register_blueprint(type_export_blueprint)
    app.register_blueprint(status_blueprint)
    app.register_blueprint(collection_blueprint)
    app.register_blueprint(log_blueprint)
    app.register_blueprint(settings_blueprint)
    app.register_blueprint(importer_blueprint)
    app.register_blueprint(exportd_job_blueprint)
    app.register_blueprint(external_system)


def register_error_pages(app):
    from cmdb.interface.rest_api.error_routes import page_not_found, method_not_allowed, not_acceptable, \
        internal_server_error, unauthorized, bad_request, forbidden, page_gone, not_implemented
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(406, not_acceptable)
    app.register_error_handler(410, page_gone)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(501, not_implemented)
