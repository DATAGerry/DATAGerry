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
import sys
import traceback

from flask import abort, request, current_app
from cmdb.framework.cmdb_render import RenderList
from cmdb.interface.route_utils import make_response, RootBlueprint, insert_request_user, login_required
from cmdb.user_management.user import User

with current_app.app_context():
    object_manager = current_app.object_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
search_blueprint = RootBlueprint('search_rest', __name__, url_prefix='/search')


@search_blueprint.route("/", methods=['GET'])
@login_required
@insert_request_user
def get_search(request_user: User):
    request_args = request.args.to_dict()

    if not bool(request_args):
        return abort(404)

    if request.args.get('limit') is not None:
        try:
            limit = int(request.args.get('limit'))
        except (ValueError, TypeError):
            return abort(400)
    else:
        limit = 0

    return _get_response(request_args, current_user=request_user, limit=limit)


@search_blueprint.route("/<string:search_input>", methods=['GET'])
@login_required
@insert_request_user
def text_search(search_input, request_user: User):
    return _get_response({'value': search_input}, q_operator='$or', current_user=request_user)


def _get_response(args, q_operator='$and', current_user: User = None, limit=0):
    query_list = []
    result_query = []

    # Collect all match values
    match_values = []

    # remove unnecessary query parameters
    _filter_query(args)

    try:
        for key, value in args.items():

            # Collect for later render evaluation
            match_values.append(value)

            for v in value.split(","):
                if key == "type_id":
                    try:
                        query_list.append({key: int(v)})
                    except (ValueError, TypeError):
                        return abort(400)
                else:
                    query_list.append({'fields.'+key: {'$regex': v}})

        result_query.append({q_operator: query_list})
        query = {"$or": result_query}

        object_list = object_manager.search_objects_with_limit(query, limit=limit)
        render = RenderList(object_list, current_user)
        if limit == 5:
            rendered_list = render.render_result_list(_collect_match_fields(object_list, match_values))
        else:
            rendered_list = render.render_result_list(None)
        return make_response(rendered_list)

    except CMDBError:
        raise traceback.print_exc(file=sys.stdout)


def _filter_query(args):

    """
    Removes the limit restriction as search parameter. And removes the search parameter "public_id" if this is undefined

    Args:
        args: query parameters

    Returns:

    """
    try:
        if args["type_id"] == "undefined":
            del args["type_id"]
        del args["limit"]
    except KeyError:
        # Must be removed, otherwise the search is falsified
        pass


def _collect_match_fields(object_list, match_values):
    import re

    key_match = []
    for passed_object in object_list:
        for term in match_values:
            for fields in getattr(passed_object, 'fields'):
                for key, value in fields.items():
                    if isinstance(value, str) and re.search(term, value):
                        key_match.append(fields['name'])
    return key_match
