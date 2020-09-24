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
from datetime import datetime

from flask import abort, current_app, request

from cmdb.framework.models.category import CategoryModel, CategoryTree
from cmdb.manager.errors import ManagerGetError, ManagerInsertError, ManagerDeleteError, ManagerUpdateError, \
    ManagerIterationError
from cmdb.framework.managers.category_manager import CategoryManager
from cmdb.framework.results.iteration import IterationResult
from cmdb.framework.utils import PublicID
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import GetSingleResponse, GetMultiResponse, InsertSingleResponse, DeleteSingleResponse, \
    UpdateSingleResponse
from cmdb.interface.blueprint import APIBlueprint

LOGGER = logging.getLogger(__name__)
categories_blueprint = APIBlueprint('categories', __name__)


@categories_blueprint.route('/', methods=['GET', 'HEAD'])
@categories_blueprint.protect(auth=True, right='base.framework.category.view')
@categories_blueprint.parse_collection_parameters(view='list')
def get_categories(params: CollectionParameters):
    """
    HTTP `GET`/`HEAD` route for getting a iterable collection of resources.

    Args:
        params (CollectionParameters): Passed parameters over the http query string + optional `view` parameter.

    Returns:
        GetMultiResponse: Which includes a IterationResult of the CategoryModel.
        If the view parameter with tree was set the route returns a GetMultiResponse<CategoryTree>.

    Example:
        You can pass any parameter based on the CollectionParameters.
        Optional parameters are passed over the function declaration.
        The `view` parameter is optional and default `list`, but can be `tree` for the category tree view.

    Raises:
        FrameworkIterationError: If the collection could not be iterated.
        ManagerGetError: If the collection could not be found.

    """
    category_manager: CategoryManager = CategoryManager(database_manager=current_app.database_manager)
    body = True if not request.method != 'HEAD' else False

    try:
        if params.optional['view'] == 'tree':
            tree: CategoryTree = category_manager.tree
            api_response = GetMultiResponse(CategoryTree.to_json(tree), total=len(tree), params=params,
                                            url=request.url, model=CategoryTree.MODEL, body=body)
            return api_response.make_response(pagination=False)
        else:
            iteration_result: IterationResult[CategoryModel] = category_manager.iterate(
                filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
            category_list = [CategoryModel.to_json(category) for category in iteration_result.results]
            api_response = GetMultiResponse(category_list, total=iteration_result.total, params=params,
                                            url=request.url, model=CategoryModel.MODEL, body=body)
    except ManagerIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


@categories_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@categories_blueprint.protect(auth=True, right='base.framework.category.view')
def get_category(public_id: int):
    """
    HTTP `GET`/`HEAD` route for a single category resource.

    Args:
        public_id (int): Public ID of the category.

    Raises:
        ManagerGetError: When the selected category does not exists.

    Returns:
        GetSingleResponse: Which includes the json data of a CategoryModel.
    """
    category_manager: CategoryManager = CategoryManager(database_manager=current_app.database_manager)
    body = True if not request.method != 'HEAD' else False

    try:
        category_instance = category_manager.get(public_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    api_response = GetSingleResponse(CategoryModel.to_json(category_instance), url=request.url,
                                     model=CategoryModel.MODEL, body=body)
    return api_response.make_response()


@categories_blueprint.route('/', methods=['POST'])
@categories_blueprint.protect(auth=True, right='base.framework.category.add')
@categories_blueprint.validate(CategoryModel.SCHEMA)
def insert_category(data: dict):
    """
    HTTP `POST` route for insert a single category resource.

    Args:
        data (CategoryModel.SCHEMA): Insert data of a new category.

    Raises:
        ManagerGetError: If the inserted resource could not be found after inserting.
        ManagerInsertError: If something went wrong during insertion.

    Returns:
        InsertSingleResponse: Insert response with the new category and its public_id.
    """
    category_manager: CategoryManager = CategoryManager(database_manager=current_app.database_manager)
    data.setdefault('creation_time', datetime.utcnow())
    try:
        result_id: PublicID = category_manager.insert(data)
        raw_doc = category_manager.get(public_id=result_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerInsertError as err:
        return abort(400, err.message)
    api_response = InsertSingleResponse(result_id, raw=CategoryModel.to_json(raw_doc), url=request.url,
                                        model=CategoryModel.MODEL)
    return api_response.make_response(prefix='categories')


@categories_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@categories_blueprint.protect(auth=True, right='base.framework.category.edit')
@categories_blueprint.validate(CategoryModel.SCHEMA)
def update_category(public_id: int, data: dict):
    """
    HTTP `PUT`/`PATCH` route for update a single category resource.

    Args:
        public_id (int): Public ID of the updatable category
        data (CategoryModel.SCHEMA): New category data to update

    Raises:
        ManagerGetError: When the category with the `public_id` was not found.
        ManagerUpdateError: When something went wrong during the update.

    Returns:
        UpdateSingleResponse: With update result of the new updated category.
    """
    category_manager: CategoryManager = CategoryManager(database_manager=current_app.database_manager)
    try:
        category = CategoryModel.from_data(data=data)
        category_manager.update(public_id=PublicID(public_id), category=CategoryModel.to_json(category))
        api_response = UpdateSingleResponse(result=data, url=request.url, model=CategoryModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerUpdateError as err:
        return abort(400, err.message)

    return api_response.make_response()


@categories_blueprint.route('/<int:public_id>', methods=['DELETE'])
@categories_blueprint.protect(auth=True, right='base.framework.category.delete')
def delete_category(public_id: int):
    """
    HTTP `DELETE` route for delete a single category resource.

    Args:
        public_id (int): Public ID of the deletable category

    Raises:
        ManagerGetError: When the category with the `public_id` was not found.
        ManagerDeleteError: When something went wrong during the deletion.

    Returns:
        DeleteSingleResponse: Delete result with the deleted category as data.
    """
    category_manager: CategoryManager = CategoryManager(database_manager=current_app.database_manager)
    try:
        deleted_category = category_manager.delete(public_id=PublicID(public_id))
        api_response = DeleteSingleResponse(raw=CategoryModel.to_json(deleted_category), model=CategoryModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerDeleteError as err:
        return abort(404, err.message)
    return api_response.make_response()
