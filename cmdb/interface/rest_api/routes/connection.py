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
"""TODO: document"""
import logging
from flask import current_app, abort

from cmdb.database.mongo_database_manager import MongoDatabaseManager

from cmdb import __title__, __version__
from cmdb.interface.rest_api.responses import DefaultResponse
from cmdb.interface.blueprints import RootBlueprint
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

connection_routes = RootBlueprint('connection_routes', __name__)

with current_app.app_context():
    dbm: MongoDatabaseManager = current_app.database_manager

# -------------------------------------------------------------------------------------------------------------------- #

@connection_routes.route('/', methods=['GET', 'HEAD'])
def connection_response():
    """
    This route is called when {{url}}/rest/ is called

    Returns:
        Response: Dict with infos about Datagerry(title, version and connection status of db)
    """
    try:
        infos = {
            'title': __title__,
            'version': __version__,
            'connected': dbm.status()
        }

        api_response = DefaultResponse(infos)

        return api_response.make_response()
    except Exception as err:
        LOGGER.debug("[connection_response] Exception: %s", str(err))
        abort(500, "Could not connect to REST API!")
