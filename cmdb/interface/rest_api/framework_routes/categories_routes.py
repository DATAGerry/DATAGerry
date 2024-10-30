# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
"""Definition of all routes for CmdbSectionTemplates"""
import logging
from datetime import datetime, timezone
from flask import request, abort

from cmdb.manager.categories_manager import CategoriesManager

from cmdb.framework.models.category import CategoryModel
from cmdb.framework.models.category_model.category_tree import CategoryTree
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.framework.results.iteration import IterationResult
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import GetSingleResponse, \
                                    GetMultiResponse, \
                                    InsertSingleResponse, \
                                    DeleteSingleResponse, \
                                    UpdateSingleResponse
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.route_utils import insert_request_user
from cmdb.user_management.models.user import UserModel
from cmdb.manager.manager_provider import ManagerType, ManagerProvider

from cmdb.errors.manager import ManagerGetError, \
                                ManagerInsertError, \
                                ManagerDeleteError, \
                                ManagerUpdateError, \
                                ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #
LOGGER = logging.getLogger(__name__)

categories_blueprint = APIBlueprint('categories', __name__)
# ---------------------------------------------------- CRUD-CREATE --------------------------------------------------- #

@categories_blueprint.route('/', methods=['POST'])
@insert_request_user
@categories_blueprint.protect(auth=True, right='base.framework.category.add')
@categories_blueprint.validate(CategoryModel.SCHEMA)
def insert_category(data: dict, request_user: UserModel):
    """
    HTTP `POST` route for insert a category into the database

    Args:
        data (CategoryModel.SCHEMA): Insert data of a new category

    Raises:
        ManagerGetError: If the inserted resource could not be found after inserting.
        ManagerInsertError: If something went wrong during insertion.

    Returns:
        InsertSingleResponse: Insert response with the new category and its public_id.
    """
    categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES_MANAGER, request_user)

    data.setdefault('creation_time', datetime.now(timezone.utc))

    try:
        result_id: int = categories_manager.insert_category(data)

        new_category = categories_manager.get_category(result_id)
    except ManagerGetError as err:
        LOGGER.debug("[insert_category] ManagerGetError: %s", err.message)
        return abort(404, "Could not retrieve the created categeory from database!")
    except ManagerInsertError as err:
        LOGGER.debug("[insert_category] ManagerInsertError: %s", err.message)
        return abort(400, "Could not insert the new categeory in database)!")

    api_response = InsertSingleResponse(result_id=result_id, raw=new_category)

    return api_response.make_response()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@categories_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@categories_blueprint.protect(auth=True, right='base.framework.category.view')
@categories_blueprint.parse_collection_parameters(view='list')
def get_categories(params: CollectionParameters, request_user: UserModel):
    """
    HTTP `GET`/`HEAD` route for getting a iterable collection of categories

    Args:
        params (CollectionParameters): Passed parameters over the http query string + optional `view` parameter.
    Returns:
        GetMultiResponse: Which includes a IterationResult of the CategoryModel.
        If the view parameter with tree was set the route returns a GetMultiResponse<CategoryTree>.
    Example:
        You can pass any parameter based on the CollectionParameters.
        Optional parameters are passed over the function declaration.
        The `view` parameter is optional and default `list`, but can be `tree` for the category tree view.
    """
    categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES_MANAGER, request_user)

    body = request.method == 'HEAD'

    try:
        if params.optional['view'] == 'tree':
            tree: CategoryTree = categories_manager.tree
            api_response = GetMultiResponse(CategoryTree.to_json(tree),
                                            len(tree),
                                            params,
                                            request.url,
                                            body)

            return api_response.make_response(pagination=False)

        # if view is not 'tree'
        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CategoryModel] = categories_manager.iterate(builder_params)

        category_list = [CategoryModel.to_json(category) for category in iteration_result.results]

        api_response = GetMultiResponse(category_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        body)
    except ManagerIterationError as err:
        LOGGER.debug("[get_categories] ManagerIterationError: %s", err.message)
        return abort(400, "Could not retrieve categories from database!")

    return api_response.make_response()


@categories_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@categories_blueprint.protect(auth=True, right='base.framework.category.view')
def get_category(public_id: int, request_user: UserModel):
    """
    HTTP `GET`/`HEAD` route to retrieve a single category

    Args:
        public_id (int): public_id of the category
    Raises:
        ManagerGetError: When the selected category could not be retrieved
    Returns:
        GetSingleResponse: Which includes the json data of the CategoryModel
    """
    categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES_MANAGER, request_user)

    try:
        category_instance = categories_manager.get_category(public_id)
    except ManagerGetError as err:
        LOGGER.debug("[get_category] ManagerGetError: %s", err.message)
        return abort(404, "Could not retrieve the requested categeory from database!")

    api_response = GetSingleResponse(category_instance, body = request.method == 'HEAD')

    return api_response.make_response()

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@categories_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@categories_blueprint.protect(auth=True, right='base.framework.category.edit')
@categories_blueprint.validate(CategoryModel.SCHEMA)
def update_category(public_id: int, data: dict, request_user: UserModel):
    """
    HTTP `PUT`/`PATCH` route to update a single category

    Args:
        public_id (int): public_id of the category which should be updated
        data (CategoryModel.SCHEMA): New category data to update
    Raises:
        ManagerUpdateError: When something went wrong during the updating
    Returns:
        UpdateSingleResponse: With update result of the new updated category
    """
    categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES_MANAGER, request_user)

    try:
        category = CategoryModel.from_data(data)

        categories_manager.update_category(public_id, category)

        api_response = UpdateSingleResponse(result=data)
    except ManagerUpdateError as err:
        LOGGER.debug("[update_category] ManagerUpdateError: %s", err.message)
        return abort(400, f"Could not update the categeory with public_id: {public_id}!")

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@categories_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@categories_blueprint.protect(auth=True, right='base.framework.category.delete')
def delete_category(public_id: int, request_user: UserModel):
    """
    HTTP `DELETE` route to delete a single category

    Args:
        public_id (int): public_id of the category which should be deleted
    Raises:
        ManagerDeleteError: When something went wrong during the deletion
        ManagerGetError: When the child categories could not be retrieved
    Returns:
        DeleteSingleResponse: Delete result with the deleted category as data
    """
    categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES_MANAGER, request_user)

    try:
        category_instance = categories_manager.get_category(public_id)
        categories_manager.delete_category(public_id)

        # Update 'parent' attribute on direct children
        categories_manager.reset_children_categories(public_id)

        api_response = DeleteSingleResponse(raw=category_instance)
    except ManagerGetError as err:
        LOGGER.debug("[delete_category] ManagerGetError: %s", err.message)
        return abort(404, "Could not retrieve the child categeories from the database!")
    except ManagerDeleteError as err:
        LOGGER.debug("[delete_category] ManagerDeleteError: %s", err.message)
        return abort(400, f"Could not delete the categeory with the ID:{public_id}!")

    return api_response.make_response()
