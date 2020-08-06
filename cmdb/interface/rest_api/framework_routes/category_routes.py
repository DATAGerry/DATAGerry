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

from cerberus import Validator
from flask import request, abort, current_app

from cmdb.framework.dao.category import CategoryDAO, CategoryTree
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerInsertError, ObjectManagerUpdateError, \
    ObjectManagerInitError, ObjectManagerDeleteError
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.manager import ManagerGetError, ManagerInsertError, ManagerDeleteError
from cmdb.framework.manager.category_manager import CategoryManager
from cmdb.framework.utils import PublicID
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import GetSingleResponse, GetMultiResponse, InsertSingleResponse, DeleteSingleResponse
from cmdb.interface.route_utils import make_response, login_required, insert_request_user, \
    right_required
from cmdb.interface.blueprint import APIBlueprint
from cmdb.user_management.user import User

with current_app.app_context():
    object_manager: CmdbObjectManager = current_app.object_manager
    category_manager: CategoryManager = CategoryManager(database_manager=current_app.database_manager)

LOGGER = logging.getLogger(__name__)
categories_blueprint = APIBlueprint('categories', __name__)


@categories_blueprint.route('/', methods=['GET'])
@categories_blueprint.protect(auth=True, right='base.framework.category.view')
@categories_blueprint.parse_collection_parameters()
def get_categories(params: CollectionParameters):
    """HTTP GET call for all categories without any kind of selection"""
    try:
        categories_list: List[CategoryDAO] = category_manager.get_many(
            params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
    except ManagerGetError as err:
        return abort(404, err.message)
    api_response = GetMultiResponse([CategoryDAO.to_json(category) for category in categories_list], 10,
                                    model=CategoryDAO.MODEL)
    return api_response.make_response()


@categories_blueprint.route('/<int:public_id>', methods=['GET'])
@categories_blueprint.protect(auth=True, right='base.framework.category.view')
def get_category(public_id: int):
    """HTTP GET call for a single category by the public id"""
    try:
        category_instance = category_manager.get(public_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    api_response = GetSingleResponse(CategoryDAO.to_json(category_instance), model=CategoryDAO.MODEL)
    return api_response.make_response()


@categories_blueprint.route('/', methods=['POST'])
@categories_blueprint.protect(auth=True, right='base.framework.category.add')
@categories_blueprint.validate(CategoryDAO.SCHEMA)
def insert_category(document: dict):
    try:
        result_id: PublicID = category_manager.insert(document)
    except ManagerInsertError as err:
        return abort(400, err.message)
    api_response = InsertSingleResponse(result_id, model=CategoryDAO.MODEL)
    return api_response.make_response(prefix='category')


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
        updated_category = CategoryDAO.from_data(update_data)
    except Exception as err:
        return abort(400, str(err))

    try:
        ack = object_manager.update_category(updated_category)
    except ObjectManagerUpdateError as err:
        return abort(500, err.message)

    resp = make_response(ack.modified_count)
    return resp


@categories_blueprint.route('/<int:public_id>', methods=['DELETE'])
@categories_blueprint.protect(auth=True, right='base.framework.category.delete')
def delete_category(public_id: int):
    """HTTP DELETE call"""
    try:
        delete_response = category_manager.delete(public_id)
        api_response = DeleteSingleResponse(raw=delete_response.raw_result, model=CategoryDAO.MODEL)
    except ManagerDeleteError as err:
        return abort(404, err.message)
    return api_response.make_response()
