import logging

from flask import request
from cmdb.utils.interface_wraps import login_required
from cmdb.interface.rest_api import app
from cmdb.interface.route_utils import make_response, RootBlueprint

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
categories_routes = RootBlueprint('categories_rest', __name__, url_prefix='/category')

with app.app_context():
    MANAGER_HOLDER = app.get_manager()


@login_required
@categories_routes.route('/', methods=['GET'])
def get_categories():
    categories_list = MANAGER_HOLDER.get_object_manager().get_all_categories()
    resp = make_response(categories_list)
    return resp


@login_required
@categories_routes.route('/tree', methods=['GET'])
def get_category_tree():
    category_tree = MANAGER_HOLDER.get_object_manager().get_category_tree()
    return make_response(category_tree)


@login_required
@categories_routes.route('/<int:public_id>', methods=['GET'])
def get_category(public_id):
    category_instance = MANAGER_HOLDER.get_object_manager().get_category(public_id)
    return make_response(category_instance)


@login_required
@categories_routes.route('/add', methods=['POST'])
def add_category():
    pass


@login_required
@categories_routes.route('/update/<int:public_id>', methods=['PUT'])
def update_category(public_id):
    pass


@login_required
@categories_routes.route('/delete/<int:public_id>', methods=['DELETE'])
def delete_category(public_id):
    delete_response = MANAGER_HOLDER.get_object_manager().delete_category(public_id)
    return make_response(delete_response)



