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

from flask import abort, current_app, request

from cmdb.framework.dao.category import CategoryDAO, CategoryTree
from cmdb.framework.manager import ManagerGetError, ManagerInsertError, ManagerDeleteError, ManagerUpdateError
from cmdb.framework.manager.category_manager import CategoryManager
from cmdb.framework.manager.error.framework_errors import FrameworkIterationError
from cmdb.framework.manager.results import IterationResult
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
        GetMultiResponse: Which includes a IterationResult of the CategoryDAO.

        If the view parameter with tree was set the route returns a GetMultiResponse<CategoryTree>.

    Example:
        You can pass any parameter based on the CollectionParameters.
        Optional parameters are passed over the function declaration.
        The `view` parameter is optional and default `list`, but can be `tree` for the category tree view.

    Raises:
        FrameworkIterationError: If the collection could not be iterated.

        ManagerGetError: If the collection could not be found.

    .. http:get:: /rest/categories/

       HTTP GET/HEAD rest route. HEAD will be the same result except their will be no body.

       **Example request**:

       .. sourcecode:: http

          GET /rest/categories/ HTTP/1.1
          Host: datagerry.com
          Accept: application/json

       **Example response**:

       .. sourcecode:: http

          HTTP/1.1 200 OK
          Content-Type: application/json
          Content-Length: 3311
          X-Total-Count: 1
          X-API-Version: 1.0

          {
              "results": [
                {
                  "public_id": 1,
                  "name": "example",
                  "label": "Example",
                  "meta": {
                    "icon": "",
                    "order": null
                  },
                  "parent": null,
                  "types": [1]
                }
              ],
              "count": 1,
              "total": 1,
              "parameters": {
                "limit": 10,
                "sort": "public_id",
                "order": 1,
                "page": 1,
                "filter": {},
                "optional": {
                  "view": "list"
                }
              },
              "pager": {
                "page": 1,
                "page_size": 10,
                "total_pages": 1
              },
              "pagination": {
                "current": "http://localhost:4000/rest/categories/",
                "first": "http://localhost:4000/rest/categories/?page=1",
                "prev": "http://localhost:4000/rest/categories/?page=1",
                "next": "http://localhost:4000/rest/categories/?page=1",
                "last": "http://localhost:4000/rest/categories/?page=1"
              },
              "response_type": "GET",
              "model": "Category",
              "time": "2020-08-20T10:13:15.350747"
            }

       :query sort: the sort field name. default is public_id
       :query order: the sort order value for ascending or descending. default is 1 for ascending
       :query page: the current view page. default is 1
       :query limit: max number of results. default is 10
       :query filter: a mongodb query filter. default is {} which means everything
       :query view: the category view data-structure. Can be `list` or `tree`. default is `list`

       :reqheader Accept: application/json
       :reqheader Authorization: jwtoken to authenticate
       :resheader Content-Type: application/json
       :statuscode 200: Everything is fine.
       :statuscode 400: The request or the parameters are wrong formatted.
       :statuscode 404: No collection or resources found.

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
            iteration_result: IterationResult[CategoryDAO] = category_manager.iterate(
                filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
            category_list = [CategoryDAO.to_json(category) for category in iteration_result.results]
            api_response = GetMultiResponse(category_list, total=iteration_result.total, params=params,
                                            url=request.url, model=CategoryDAO.MODEL, body=body)
    except FrameworkIterationError as err:
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
        GetSingleResponse: Which includes the json data of a CategoryDAO.

    .. http:get:: /category/(int:public_id)

        The category with the public_id.

        **Example request**

        .. sourcecode:: http

            GET /rest/categories/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 588
            X-API-Version: 1.0

            {
              "result": {
                "public_id": 1,
                "name": "example",
                "label": "Example",
                "meta": {
                  "icon": "far fa-folder-open",
                  "order": 0
                },
                "parent": null,
                "types": [1]
              },
              "response_type": "GET",
              "model": "Category",
              "time": "2020-08-20T09:21:10.235525"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 404: No resource found.

    """
    category_manager: CategoryManager = CategoryManager(database_manager=current_app.database_manager)
    body = True if not request.method != 'HEAD' else False

    try:
        category_instance = category_manager.get(public_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    api_response = GetSingleResponse(CategoryDAO.to_json(category_instance), url=request.url,
                                     model=CategoryDAO.MODEL, body=body)
    return api_response.make_response()


@categories_blueprint.route('/', methods=['POST'])
@categories_blueprint.protect(auth=True, right='base.framework.category.add')
@categories_blueprint.validate(CategoryDAO.SCHEMA)
def insert_category(data: dict):
    """
    HTTP `POST` route for insert a single category resource.

    Args:
        data (CategoryDAO.SCHEMA): Insert data of a new category.

    Raises:
        ManagerGetError: If the inserted resource could not be found after inserting.
        ManagerInsertError: If something went wrong during insertion.

    Returns:
        InsertSingleResponse: Insert response with the new category and its public_id.

    .. http:post:: /category/

        HTTP Post route for inserting a new category.

        **Example request**

        .. sourcecode:: http

            POST /rest/categories/ HTTP/1.1
            Host: datagerry.com
            Accept: application/json

            {
              "name": "example",
              "label": "Example",
              "meta": {
                "icon": "",
                "order": 0
              },
              "parent": null,
              "types": [1]
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 588
            Location: http://localhost:4000/rest/categories/1
            X-API-Version: 1.0

            {
              "result_id": 1,
              "raw": {
                "public_id": 1,
                "name": "example",
                "label": "Example",
                "meta": {
                  "icon": "",
                  "order": 0
                },
                "parent": null,
                "types": [1]
              },
              "response_type": "INSERT",
              "model": "Category",
              "time": "2020-08-20T11:14:42.704920"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: Resource could not be inserted.
        :statuscode 404: No resource found.
    """
    category_manager: CategoryManager = CategoryManager(database_manager=current_app.database_manager)
    try:
        result_id: PublicID = category_manager.insert(data)
        raw_doc = category_manager.get(public_id=result_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerInsertError as err:
        return abort(400, err.message)
    api_response = InsertSingleResponse(result_id, raw=CategoryDAO.to_json(raw_doc), url=request.url,
                                        model=CategoryDAO.MODEL)
    return api_response.make_response(prefix='category')


@categories_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@categories_blueprint.protect(auth=True, right='base.framework.category.edit')
@categories_blueprint.validate(CategoryDAO.SCHEMA)
def update_category(public_id: int, data: dict):
    """
    HTTP `PUT`/`PATCH` route for update a single category resource.

    Args:
        public_id (int): Public ID of the updatable category
        data (CategoryDAO.SCHEMA): New category data to update

    Raises:
        ManagerGetError: When the category with the `public_id` was not found.
        ManagerUpdateError: When something went wrong during the update.

    Returns:
        UpdateSingleResponse: With update result of the new updated category.

    .. http:put:: /category/(int:public_id)

        HTTP `PUT`/`PATCH` route for updating a existing category.

        **Example request**

        .. sourcecode:: http

            PUT /rest/categories/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

            {
              ""public_id": 1,
              "name": "example",
              "label": "Example",
              "meta": {
                "icon": "",
                "order": 0
              },
              "parent": null,
              "types": [1]
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 202 ACCEOTED
            Content-Type: application/json
            Content-Length: 170
            Location: http://localhost:4000/rest/categories/1
            X-API-Version: 1.0

            {
              "result": {
                "public_id": 1,
                "name": "example2",
                "label": "Example,
                "meta": {
                  "icon": "",
                  "order": 0
                },
                "parent": null,
                "types": []
              },
              "response_type": "UPDATE",
              "model": "Category",
              "time": "2020-08-20T11:37:07.499137"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be updated.
        :statuscode 404: No resource found.
    """
    category_manager: CategoryManager = CategoryManager(database_manager=current_app.database_manager)
    try:
        category = CategoryDAO.from_data(data=data)
        update_result = category_manager.update(public_id=PublicID(public_id), resource=CategoryDAO.to_json(category))
        api_response = UpdateSingleResponse(result=data, url=request.url, model=CategoryDAO.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerUpdateError as err:
        return abort(400, err.message)
    except Exception as err:
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

    .. http:delete:: /category/(int:public_id)

        HTTP `DELETE` route for deleting a existing category.

        **Example request**

        .. sourcecode:: http

            DELETE /rest/categories/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 202 ACCEOTED
            Content-Type: application/json
            Content-Length: 170
            X-API-Version: 1.0

            {
              "deleted_entry": {
                "public_id": 1,
                "name": "example",
                "label": "Eexample",
                "meta": {
                  "icon": "",
                  "order": 1
                },
                "parent": null,
                "types": [
                  1
                ]
              },
              "response_type": "DELETE",
              "model": "Category",
              "time": "2020-08-20T11:45:50.809706"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be deleted.
        :statuscode 404: No resource found.
    """
    category_manager: CategoryManager = CategoryManager(database_manager=current_app.database_manager)
    try:
        deleted_category = category_manager.delete(public_id=PublicID(public_id))
        api_response = DeleteSingleResponse(raw=CategoryDAO.to_json(deleted_category), model=CategoryDAO.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerDeleteError as err:
        return abort(404, err.message)
    return api_response.make_response()
