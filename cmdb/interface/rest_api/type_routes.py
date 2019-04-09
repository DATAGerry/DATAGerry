import logging

from cmdb import __MODE__
from flask import current_app, abort
from cmdb.utils.interface_wraps import login_required

from cmdb.interface.route_utils import make_response, RootBlueprint

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
type_routes = RootBlueprint('type_routes', __name__, url_prefix='/type')

if __MODE__ == 'TESTING':
    MANAGER_HOLDER = None
else:
    with current_app.app_context():
        MANAGER_HOLDER = current_app.get_manager()


@login_required
@type_routes.route('/', methods=['GET'])
def get_type_list():
    object_manager = MANAGER_HOLDER.get_object_manager()
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
    object_manager = MANAGER_HOLDER.get_object_manager()
    try:
        type_instance = object_manager.get_type(public_id)
    except CMDBError:
        return abort(404)
    resp = make_response(type_instance)
    return resp


@type_routes.route('/by/<dict:requirements>', defaults={'requirements': None}, methods=['GET', 'POST'])
def get_type_by(requirements: dict):
    return "test {}".format(requirements)


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
