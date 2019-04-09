import logging

from cmdb import __MODE__
from flask import current_app
from cmdb.utils.interface_wraps import login_required
from cmdb.interface.route_utils import make_response, RootBlueprint

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
right_routes = RootBlueprint('right_rest', __name__, url_prefix='/right')

if __MODE__ == 'TESTING':
    MANAGER_HOLDER = None
else:
    with current_app.app_context():
        MANAGER_HOLDER = current_app.get_manager()


@login_required
@right_routes.route('/', methods=['GET'])
def get_all_rights():
    user_manager = MANAGER_HOLDER.get_user_manager()
    right_list = user_manager.get_all_rights()

    resp = make_response(right_list)
    return resp


@login_required
@right_routes.route('/tree', methods=['GET'])
def get_right_tree():
    user_manager = MANAGER_HOLDER.get_user_manager()
    right_tree = user_manager.get_right_tree()
    resp = make_response(right_tree)
    return resp


@login_required
@right_routes.route('/<string:name>', methods=['GET'])
def get_right(name: str):
    right_instance = MANAGER_HOLDER.get_user_manager().get_right_by_name(name)
    return make_response(right_instance)


@login_required
@right_routes.route('/level/<int:level>', methods=['GET'])
def get_rights_with_min_level(level: int):
    right_list = MANAGER_HOLDER.get_user_manager().get_right_names_with_min_level(level)
    return make_response(right_list)


@login_required
@right_routes.route('/levels', methods=['GET'])
def get_security_levels():
    security_levels = MANAGER_HOLDER.get_user_manager().get_security_levels()
    return make_response(security_levels)

# other crud functions are not required because of static right programming
