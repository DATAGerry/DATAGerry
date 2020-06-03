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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import logging
import json
from typing import List

from cmdb.framework.cmdb_category import CmdbCategory, CategoryTree
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerInsertError, ObjectManagerUpdateError, \
    ObjectManagerInitError, ObjectManagerDeleteError
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.interface.route_utils import make_response, RootBlueprint, login_required, insert_request_user, right_required

from flask import request, abort, current_app

from cmdb.search.query.query_builder import QueryBuilder
from cmdb.user_management import User

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

with current_app.app_context():
    object_manager: CmdbObjectManager = current_app.object_manager

LOGGER = logging.getLogger(__name__)
categories_blueprint = RootBlueprint('categories_rest', __name__, url_prefix='/category')


@categories_blueprint.route('/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.category.view')
def get_categories(request_user: User):
    """HTTP GET call for all categories without any kind of selection"""
    try:
        categories_list: List[dict] = [CmdbCategory.to_json(category) for category in
                                       object_manager.get_all_categories()]
    except ObjectManagerInitError as err:
        return abort(500, err.message)
    except ObjectManagerGetError as err:
        return abort(400, err.message)

    if len(categories_list) == 0:
        return make_response([], 204)

    return make_response(categories_list)


@categories_blueprint.route('/<int:public_id>/', methods=['GET'])
@categories_blueprint.route('/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.category.view')
def get_category(public_id: int, request_user: User):
    """HTTP GET call for a single category by the public id"""
    try:
        category_instance = object_manager.get_category(public_id)
    except ObjectManagerInitError as err:
        return abort(500, err.message)
    except ObjectManagerGetError as err:
        return abort(404, err.message)
    return make_response(CmdbCategory.to_json(category_instance))


@categories_blueprint.route('/find/<string:regex>/', defaults={'regex_options': 'imsx'}, methods=['GET'])
@categories_blueprint.route('/find/<string:regex>', defaults={'regex_options': 'imsx'}, methods=['GET'])
@categories_blueprint.route('/find/<string:regex>/<string:regex_options>/', methods=['GET'])
@categories_blueprint.route('/find/<string:regex>/<string:regex_options>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.category.view')
def find_categories_by_name(regex: str, regex_options: str, request_user: User):
    """HTTP GET call for a list of categories by a given regex name
    Examples:
        Input `ex` matches for example, Example, test_example
    Notes:
        The regex will match for name parameter and label
    """
    query_builder = QueryBuilder()

    if not regex or (regex == '') or regex is None or len(regex) == 0:
        return abort(400, 'No valid selection parameter was passed!')

    if any(ro not in 'imsx' for ro in regex_options):
        return abort(400, 'No valid regex options!')

    query_name = query_builder.regex_('name', f'{regex}', regex_options)
    query_label = query_builder.regex_('label', f'{regex}', regex_options)
    query = query_builder.or_([query_name, query_label])

    try:
        categories: List[CmdbCategory] = object_manager.get_categories_by(**query)
    except ObjectManagerInitError as err:
        return abort(500, err.message)
    except ObjectManagerGetError as err:
        return abort(400, err.message)

    if len(categories) == 0:
        return make_response([], 204)

    categories_in_json = [CmdbCategory.to_json(category) for category in categories]
    return make_response(categories_in_json)


@categories_blueprint.route('/tree/', methods=['GET'])
@categories_blueprint.route('/tree', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.category.view')
def get_category_tree(request_user: User):
    """HTTP GET call for full category tree"""
    try:
        tree = object_manager.get_category_tree()
    except ObjectManagerInitError as err:
        return abort(500, err.message)
    except ObjectManagerGetError as err:
        return abort(404, err.message)

    if len(tree) == 0:
        return make_response([], 204)
    return make_response(CategoryTree.to_json(tree))


@categories_blueprint.route('/<string:name>/', methods=['GET'])
@categories_blueprint.route('/<string:name>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.type.view')
def get_category_by_name(name: str, request_user: User):
    """HTTP GET call - get a specific category by its name"""
    try:
        category_instance = object_manager.get_category_by(name=name)
    except ObjectManagerGetError as err:
        return abort(404, err.message)
    except ObjectManagerInitError as err:
        return abort(501, err.message)
    return make_response(CmdbCategory.to_json(category_instance))


@categories_blueprint.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.framework.category.add')
def add_category(request_user: User):
    """HTTP POST call - add a new category from json post data"""
    try:
        request_data = request.get_data().decode('UTF-8')
        insert_data = json.loads(request_data)
    except TypeError as te:
        return abort(400, str(te))

    insert_data['public_id'] = int(object_manager.get_new_id(CmdbCategory.COLLECTION))
    try:
        new_category = CmdbCategory.from_data(insert_data)
    except Exception as err:
        return abort(400, str(err))

    try:
        insert_acknowledge = object_manager.insert_category(new_category)
    except ObjectManagerInsertError as err:
        return abort(400, err.message)
    return make_response(insert_acknowledge)


@categories_blueprint.route('/', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.framework.category.edit')
def update_category(request_user: User):
    try:
        request_data = request.get_data().decode('UTF-8')
        update_data = json.loads(request_data)
    except TypeError as te:
        return abort(400, str(te))

    try:
        updated_category = CmdbCategory.from_data(update_data)
    except Exception as err:
        return abort(400, str(err))

    try:
        ack = object_manager.update_category(updated_category)
    except ObjectManagerUpdateError as err:
        return abort(500, err.message)

    resp = make_response(ack.modified_count)
    return resp


@categories_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@categories_blueprint.route('/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.framework.category.delete')
def delete_category(public_id: int, request_user: User):
    """HTTP DELETE call"""
    try:
        delete_response = object_manager.delete_category(public_id)
    except ObjectManagerDeleteError as err:
        return abort(400, err.message)
    return make_response(delete_response)
