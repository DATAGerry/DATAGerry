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

import cmdb,logging, ast, sys, traceback
from flask import abort, current_app as app, request
from cmdb.framework.cmdb_render import CmdbRender
from cmdb.interface.route_utils import make_response, RootBlueprint
from cmdb.framework.cmdb_object_manager import object_manager as obm
from cmdb.utils.interface_wraps import login_required


try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
search_routes = RootBlueprint('search_rest', __name__, url_prefix='/search')


@search_routes.route("/", methods=['GET'])
@login_required
def get_search():
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

    return _get_response(request_args, limit=limit)


@search_routes.route("/<string:search_input>", methods=['GET'])
@login_required
def text_search(search_input):
    return _get_response({'value': search_input}, q_operator = '$or')


def _get_response(args, q_operator='$and', limit=0):
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

        render = _cm_db_render(obm.search_objects_with_limit(query, limit=limit), match=match_values)
        resp = make_response(CmdbRender.result_loop_render(obm, render))
        return resp

    except CMDBError:
        raise traceback.print_exc(file=sys.stdout)


def _cm_db_render(all_objects_list, match=[]) -> list:
    all_objects = []
    type_buffer_list = {}

    try:
        for passed_object in all_objects_list:
            passed_object_type_id = passed_object.get_type_id()

            if passed_object_type_id in type_buffer_list:
                current_type = type_buffer_list[passed_object_type_id]
            else:
                current_type = obm.get_type(passed_object_type_id)
                type_buffer_list.update({passed_object_type_id: current_type})

            tmp_render = CmdbRender(type_instance=current_type, object_instance=passed_object)
            tmp_render.set_matched_fieldset(_collect_match_fields(passed_object, match))
            all_objects.append(tmp_render)
    except Exception:
        raise traceback.print_exc(file=sys.stdout)

    return all_objects


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


def _collect_match_fields(passed_object, match_values):
    key_match = []
    for term in match_values:
        for fields in getattr(passed_object, 'fields'):
            for key, value in fields.items():
                if isinstance(value, str) and term in value:
                    key_match.append(fields['name'])
    return key_match
