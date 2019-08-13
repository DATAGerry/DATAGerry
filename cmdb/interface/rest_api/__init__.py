# dataGerry - OpenSource Enterprise CMDB
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

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


def create_rest_api(event_queue):
    from cmdb.interface.config import app_config
    from cmdb.utils.system_reader import SystemConfigReader
    try:

        system_config_reader = SystemConfigReader()

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
    from cmdb.interface.cmdb_app import BaseCmdbApp
    app = BaseCmdbApp(__name__)
    from flask_cors import CORS
    CORS(app)
    import cmdb
    cache.init_app(app)
    cache.clear()

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
    from cmdb.interface.rest_api.object_routes import object_rest
    from cmdb.interface.rest_api.type_routes import type_routes
    from cmdb.interface.rest_api.auth_routes import auth_routes
    from cmdb.interface.rest_api.category_routes import categories_routes
    from cmdb.interface.rest_api.user_management.user_routes import user_routes
    from cmdb.interface.rest_api.user_management.right_routes import right_routes
    from cmdb.interface.rest_api.user_management.group_routes import group_routes
    from cmdb.interface.rest_api.settings_routes import settings_rest
    from cmdb.interface.rest_api.search_routes import search_routes
    from cmdb.interface.rest_api.export_routes import export_route
    from cmdb.interface.rest_api.status_routes import status_routes
    app.register_blueprint(auth_routes)
    app.register_blueprint(object_rest)
    app.register_blueprint(type_routes)
    app.register_blueprint(connection_routes)
    app.register_blueprint(categories_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(group_routes)
    app.register_blueprint(right_routes)
    app.register_blueprint(settings_rest)
    app.register_blueprint(search_routes)
    app.register_blueprint(export_route)
    app.register_blueprint(status_routes)


def register_error_pages(app):
    from cmdb.interface.rest_api.error_routes import page_not_found, method_not_allowed, not_acceptable, \
        internal_server_error, unauthorized_user, bad_request, forbidden, page_gone, not_implemented
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized_user)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(406, not_acceptable)
    app.register_error_handler(410, page_gone)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(501, not_implemented)
