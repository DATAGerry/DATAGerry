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

import logging

import cmdb
from cmdb.interface.cmdb_app import BaseCmdbApp
from cmdb.interface.config import app_config
from cmdb.interface.docs.doc_routes import doc_pages

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)

from cmdb.utils.system_reader import SystemConfigReader

system_config_reader = SystemConfigReader()


def create_docs_server(event_queue):
    # Create manager
    from cmdb.data_storage import DatabaseManagerMongo, MongoConnector
    app_database = DatabaseManagerMongo(
        connector=MongoConnector(
            **system_config_reader.get_all_values_from_section('Database')
        )
    )

    app = BaseCmdbApp(__name__, app_database)

    if cmdb.__MODE__ == 'DEBUG':
        app.config.from_object(app_config['rest_development'])
        LOGGER.info('Docs starting with config mode {}'.format(app.config.get("ENV")))
    elif cmdb.__MODE__ == 'TESTING':
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['rest'])
        LOGGER.info('Docs starting with config mode {}'.format(app.config.get("ENV")))

    app.register_blueprint(doc_pages, url_prefix="/")

    return app
