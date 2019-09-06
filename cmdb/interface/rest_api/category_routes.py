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
import json

from cmdb.framework.cmdb_object_manager import object_manager
from cmdb.framework.cmdb_category import CmdbCategory
from cmdb.utils.wraps import login_required
from cmdb.interface.route_utils import make_response, RootBlueprint

from flask import request, abort
from bson import json_util

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
categories_routes = RootBlueprint('categories_rest', __name__, url_prefix='/category')


@categories_routes.route('/', methods=['GET'])
@login_required
def get_categories():
    categories_list = object_manager.get_all_categories()
    resp = make_response(categories_list)
    return resp


@categories_routes.route('/tree', methods=['GET'])
@login_required
def get_category_tree():
    from cmdb.framework.cmdb_errors import NoRootCategories
    try:
        category_tree = object_manager.get_category_tree()
    except NoRootCategories:
        category_tree = []
    return make_response(category_tree)


@categories_routes.route('/<int:public_id>', methods=['GET'])
@login_required
def get_category(public_id):
    category_instance = object_manager.get_category(public_id)
    return make_response(category_instance)


@categories_routes.route('/', methods=['POST'])
@login_required
def add_category():
    http_post_request_data = json.dumps(request.json)
    ack = None
    modified_category_data = None
    try:
        modified_category_data = json.loads(http_post_request_data, object_hook=json_util.object_hook)
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)
    try:
        modified_category_data['public_id'] = int(object_manager.get_new_id(CmdbCategory.COLLECTION) + 1)
        ack = object_manager.insert_category(modified_category_data)
    except CMDBError as e:
        LOGGER.debug(e.message)
    return make_response(ack)


@categories_routes.route('/', methods=['PUT'])
@login_required
def update_category():
    http_put_request_data = json.dumps(request.json)
    ack = None
    modified_category_data = None
    LOGGER.debug(http_put_request_data)
    try:
        modified_category_data = json.loads(http_put_request_data, object_hook=json_util.object_hook)
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)
    try:
        update_category_instance = CmdbCategory(**modified_category_data)
    except CMDBError:
        return abort(400)

    try:
        ack = object_manager.update_category(update_category_instance)
    except CMDBError:
        return abort(500)

    resp = make_response(ack.modified_count)
    return resp


@categories_routes.route('/<int:public_id>', methods=['DELETE'])
@login_required
def delete_category(public_id):
    delete_response = object_manager.delete_category(public_id)

    # update category
    categories = object_manager.get_categories_by({'parent_id': public_id})
    for category in categories:
        category.parent_id = None
        object_manager.update_category(category)

    return make_response(delete_response)
