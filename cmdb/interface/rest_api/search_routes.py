import logging
from flask import abort
from cmdb.interface.rest_api import app
from cmdb.interface.rest_api import MANAGER_HOLDER
from cmdb.object_framework.cmdb_render import CmdbRender
from cmdb.interface.route_utils import make_response, RootBlueprint


try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
search_routes = RootBlueprint('search_rest', __name__, url_prefix='/search')

with app.app_context():
    MANAGER_HOLDER = app.get_manager()


@search_routes.route("/<string:searchtext>")
def fulltextsearch(searchtext: str):
    all_objects = []
    try:
        type_buffer_list = {}

        regex = {'fields.value': {'$regex': searchtext}}

        all_objects_list = MANAGER_HOLDER.get_object_manager().search_objects(regex)
        for passed_object in all_objects_list:

            passed_object_type_id = passed_object.get_type_id()
            if passed_object_type_id in type_buffer_list:
                current_type = type_buffer_list[passed_object_type_id]
            else:
                try:
                    current_type = MANAGER_HOLDER.get_object_manager().get_type(passed_object_type_id)
                    type_buffer_list.update({passed_object_type_id: current_type})
                except CMDBError as e:
                    continue
            tmp_render = CmdbRender(type_instance=current_type, object_instance=passed_object)
            all_objects.append(tmp_render.result())
    except CMDBError:
        return abort(400)

    resp = make_response(all_objects)
    return resp
