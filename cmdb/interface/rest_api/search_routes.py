import cmdb,logging, ast
from flask import abort, current_app as app, request
from cmdb.object_framework.cmdb_object_manager import object_manager
from cmdb.object_framework.cmdb_render import CmdbRender
from cmdb.interface.route_utils import make_response, RootBlueprint


try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
search_routes = RootBlueprint('search_rest', __name__, url_prefix='/search')


@search_routes.route("/")
def get_search():
    try:
        fields_list = []
        request_args = request.args.to_dict()

        if not bool(request_args):
            return abort(400)

        for key, value in request_args.items():
            for v in value.split(","):
                fields_list.append({'fields.'+key: {'$regex': v}})

        query = {"$and": fields_list}

        resp = make_response(_cm_db_render(object_manager.search_objects(query)))
        return resp
    except CMDBError:
        return abort(400)


@search_routes.route("/<string:search_text>")
def text_search(search_text):
    try:
        fields_list = []
        for v in search_text.split(','):
            fields_list.append({'fields.value': {'$regex': v}})
        query = {"$or": fields_list}

        resp = make_response(_cm_db_render(object_manager.search_objects(query)))
        return resp
    except CMDBError:
        return abort(400)


def _cm_db_render(all_objects_list) -> list:
    all_objects = []
    type_buffer_list = {}

    for passed_object in all_objects_list:
        passed_object_type_id = passed_object.get_type_id()
        if passed_object_type_id in type_buffer_list:
            current_type = type_buffer_list[passed_object_type_id]
        else:
            try:
                current_type = object_manager.get_type(passed_object_type_id)
                type_buffer_list.update({passed_object_type_id: current_type})
            except CMDBError as e:
                continue
        tmp_render = CmdbRender(type_instance=current_type, object_instance=passed_object)
        all_objects.append(tmp_render.result())

    return all_objects
