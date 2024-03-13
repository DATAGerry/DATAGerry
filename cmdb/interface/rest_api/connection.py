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

from flask import current_app

from cmdb.interface.route_utils import make_response
from cmdb.interface.blueprint import RootBlueprint
from cmdb.database.database_manager_mongo import DatabaseManagerMongo


connection_routes = RootBlueprint('connection_routes', __name__)
LOGGER = logging.getLogger(__name__)

with current_app.app_context():
    database_manager: DatabaseManagerMongo = current_app.database_manager


@connection_routes.route('/')
def connection_response():
    """TODO: document"""
    from cmdb import __title__, __version__
    resp = {
        'title': __title__,
        'version': __version__,
        'connected': database_manager.status()
    }
    return make_response(resp)
