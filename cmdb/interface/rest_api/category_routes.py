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
from typing import List

from cmdb.framework.cmdb_category import CmdbCategory
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerInsertError, ObjectManagerUpdateError
from cmdb.interface.route_utils import make_response, RootBlueprint, login_required, insert_request_user, right_required

from flask import request, abort, current_app
from bson import json_util

from cmdb.user_management import User

with current_app.app_context():
    object_manager = current_app.object_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
categories_blueprint = RootBlueprint('categories_rest', __name__, url_prefix='/category')


@categories_blueprint.route('/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.category.view')
def get_categories(request_user: User):
    categories_list: List[CmdbCategory] = object_manager.get_all_categories()
    if len(categories_list) == 0:
        return make_response(categories_list, 204)
    return make_response(categories_list)


@categories_blueprint.route('/tree/', methods=['GET'])
@categories_blueprint.route('/tree', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.category.view')
def get_category_tree(request_user: User):
    from cmdb.framework.cmdb_errors import NoRootCategories
    try:
        category_tree = object_manager.get_category_tree()
    except NoRootCategories:
        return make_response([], 204)
    return make_response(category_tree)


@categories_blueprint.route('/<int:public_id>/', methods=['GET'])
@categories_blueprint.route('/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.category.view')
def get_category(public_id, request_user: User):
    try:
        category_instance = object_manager.get_category(public_id)
    except ObjectManagerGetError as e:
        LOGGER.error(f'Error while get category with Public ID {public_id}: {e}')
        return abort(404, 'Category was not found!')
    return make_response(category_instance)


@categories_blueprint.route('/root/', methods=['GET'])
@categories_blueprint.route('/root', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.category.view')
def get_root_category(request_user: User):
    try:
        category_instance = object_manager.get_categories_by(_filter={'root': True})
    except ObjectManagerGetError as e:
        LOGGER.error(f'Root category was not found!: {e}')
        return abort(404, 'Root category was not found!')
    return make_response(category_instance)


@categories_blueprint.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.framework.category.add')
def add_category(request_user: User):
    http_post_request_data = json.dumps(request.json)
    try:
        modified_category_data = json.loads(http_post_request_data, object_hook=json_util.object_hook)
    except TypeError as e:
        return abort(400)
    try:
        modified_category_data['public_id'] = int(object_manager.get_new_id(CmdbCategory.COLLECTION))
        ack = object_manager.insert_category(modified_category_data)
    except ObjectManagerInsertError:
        return abort(400)
    return make_response(ack)


@categories_blueprint.route('/', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.framework.category.edit')
def update_category(request_user: User):
    try:
        http_put_request_data = json.dumps(request.json)
    except TypeError:
        return abort(400)
    try:
        modified_category_data = json.loads(http_put_request_data, object_hook=json_util.object_hook)
    except TypeError as e:
        LOGGER.warning(e)
        return abort(400)

    try:
        ack = object_manager.update_category(modified_category_data)
    except ObjectManagerUpdateError as e:
        LOGGER.error(f'Error while updating category: {e}')
        return abort(500)
    resp = make_response(ack.modified_count)
    return resp


@categories_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@categories_blueprint.route('/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.framework.category.edit')
def delete_category(public_id, request_user: User):
    delete_response = object_manager.delete_category(public_id)

    categories = object_manager.get_categories_by({'parent_id': public_id})
    for category in categories:
        category.parent_id = None
        object_manager.update_category(category)

    return make_response(delete_response)
