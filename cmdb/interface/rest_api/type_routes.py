import logging

from flask import abort
from cmdb.utils.interface_wraps import login_required
from cmdb.object_framework.cmdb_object_manager import object_manager as obm
from cmdb.interface.route_utils import make_response, RootBlueprint

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
type_routes = RootBlueprint('type_routes', __name__, url_prefix='/type')

object_manager = obm


@login_required
@type_routes.route('/', methods=['GET'])
def get_type_list():
    try:
        type_list = object_manager.get_all_types()
    except CMDBError:
        return abort(500)
    resp = make_response(type_list)
    return resp


@login_required
@type_routes.route('/<int:public_id>', methods=['GET'])
def get_type(public_id: int):
    type_instance = None
    try:
        type_instance = object_manager.get_type(public_id)
    except CMDBError:
        return abort(404)
    resp = make_response(type_instance)
    return resp


@login_required
@type_routes.route('/', methods=['POST'])
def add_type():
    type_instance = None
    resp = make_response(type_instance)
    return resp


@login_required
@type_routes.route('/<int:public_id>', methods=['PUT'])
def update_type(public_id: int):
    type_instance = None
    resp = make_response(type_instance)
    return resp


@login_required
@type_routes.route('/<int:public_id>', methods=['DELETE'])
def delete_type(public_id: int):
    type_instance = None
    resp = make_response(type_instance)
    return resp
