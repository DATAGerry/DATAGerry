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
import json
import logging

from flask import current_app, request, abort

from cmdb.interface.route_utils import RootBlueprint, make_response, insert_request_user, login_required
from cmdb.search import Search
from cmdb.search.query import Query
from cmdb.search.query.query_builder import QueryBuilder
from cmdb.search.searchers import SearcherFramework
from cmdb.user_management.user import User

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

with current_app.app_context():
    object_manager = current_app.object_manager

LOGGER = logging.getLogger(__name__)
search_blueprint = RootBlueprint('search_rest', __name__, url_prefix='/search')


@search_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@insert_request_user
def search_framework(request_user: User):
    try:
        limit = request.args.get('limit', Search.DEFAULT_LIMIT, int)
        LOGGER.debug(f'[SearchRoutes][Limit]: {limit}')
        skip = request.args.get('skip', Search.DEFAULT_SKIP, int)
        search_parameters: dict = request.args.get('query') or '{}'
    except ValueError as err:
        return abort(400, err)
    try:
        if request.method == 'GET':
            search_parameters = json.loads(search_parameters)
        elif request.method == 'POST':
            search_parameters = json.loads(request.data)
        else:
            return abort(405)
    except Exception as err:
        LOGGER.error(f'[Search Framework]: {err}')
        return abort(400, err)

    query_builder = QueryBuilder()
    query: Query = query_builder.build(search_parameters)

    searcher = SearcherFramework(manager=object_manager)
    result = searcher.search(query=query, request_user=request_user, limit=limit, skip=skip)

    return make_response(result)
