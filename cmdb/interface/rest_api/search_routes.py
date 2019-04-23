import cmdb,logging, ast, sys, traceback
from flask import abort, current_app as app, request
from cmdb.object_framework.cmdb_render import CmdbRender
from cmdb.interface.route_utils import make_response, RootBlueprint
from cmdb.object_framework.cmdb_object_manager import object_manager as obm


try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
search_routes = RootBlueprint('search_rest', __name__, url_prefix='/search')


@search_routes.route("/")
def get_search():
    request_args = request.args.to_dict()
    if not bool(request_args):
        return abort(404)
    return _get_response(request_args)


@search_routes.route("/<string:search_input>")
def text_search(search_input):
    return _get_response({'value': search_input})


def _get_response(args, q_operator='$and'):
    query_list = []
    result_query = []

    try:
        for key, value in args.items():
            for v in value.split(","):
                query_list.append({'fields.'+key: {'$regex': v}})
            result_query.append({q_operator: query_list})
        query = {"$or": result_query}
        return make_response(_cm_db_render(obm.search_objects(query)))

    except CMDBError:
        raise traceback.print_exc(file=sys.stdout)


def _cm_db_render(all_objects_list) -> list:
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
            all_objects.append(tmp_render.result())
    except Exception:
        raise traceback.print_exc(file=sys.stdout)

    return all_objects
