import json
import logging

from flask import Blueprint, jsonify, abort, request
from cmdb.utils.interface_wraps import login_required
from cmdb.interface.rest_api import MANAGER_HOLDER
from cmdb.interface.route_utils import DEFAULT_MIME_TYPE, make_response
from cmdb.utils import json_encoding

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
type_rest = Blueprint('type_rest', __name__, url_prefix='/type')


@login_required
@type_rest.route('/', methods=['GET'])
def get_type_list():
    object_manager = MANAGER_HOLDER.get_object_manager()
    try:
        type_list = object_manager.get_all_types()
    except CMDBError:
        return abort(404)
    resp = make_response(type_list)
    return resp


@login_required
@type_rest.route('/<int:public_id>', methods=['GET'])
def get_type(public_id: int):
    type_instance = None
    object_manager = MANAGER_HOLDER.get_object_manager()
    try:
        type_instance = object_manager.get_type(public_id)
    except CMDBError:
        return abort(404)
    resp = make_response(type_instance)
    return resp


@type_rest.route('/by/<dict:requirements>', defaults={'requirements': None}, methods=['GET', 'POST'])
def get_type_by(requirements: dict):
    return "test {}".format(requirements)


@login_required
@type_rest.route('/', methods=['POST'])
def add_type():
    type_instance = None
    resp = make_response(type_instance)
    return resp


@login_required
@type_rest.route('/<int:public_id>', methods=['PUT'])
def update_type(public_id: int):
    type_instance = None
    resp = make_response(type_instance)
    return resp


@login_required
@type_rest.route('/<int:public_id>', methods=['DELETE'])
def delete_type(public_id: int):
    type_instance = None
    resp = make_response(type_instance)
    return resp
