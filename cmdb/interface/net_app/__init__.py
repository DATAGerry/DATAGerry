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
Init module for static routes
"""
import logging
from flask_cors import CORS

from cmdb.interface.cmdb_app import BaseCmdbApp
from cmdb.interface.config import app_config
from cmdb.utils.system_config import SystemConfigReader

LOGGER = logging.getLogger(__name__)

system_config_reader = SystemConfigReader()


def create_app(event_queue):
    # Create managers
    from cmdb.database.managers import DatabaseManagerMongo
    app_database = DatabaseManagerMongo(
        **system_config_reader.get_all_values_from_section('Database')
    )

    app = BaseCmdbApp(__name__, app_database)
    CORS(app)
    import cmdb
    from cmdb.interface.net_app.app_routes import app_pages, redirect_index

    if cmdb.__MODE__ == 'DEBUG':
        config = app_config['development']
        app.config.from_object(config)
    else:
        config = app_config['production']
        app.config.from_object(config)

    # add static routes
    app.register_blueprint(app_pages, url_prefix='/')
    app.register_error_handler(404, redirect_index)

    @app.route('/favicon.ico')
    def favicon():
        from os import path
        from flask import send_from_directory
        return send_from_directory(path.join(app.root_path, '_static'), 'favicon.ico')

    @app.route('/browserconfig.xml')
    def browser_config():
        from os import path
        from flask import send_from_directory
        return send_from_directory(path.join(app.root_path, '_static'), 'browserconfig.xml')

    return app
