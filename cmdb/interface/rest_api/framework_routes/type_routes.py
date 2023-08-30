# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
from datetime import datetime, timezone

from flask import abort, request, current_app

from cmdb.framework.models.type import TypeModel
from cmdb.interface.rest_api.framework_routes.type_parameters import TypeIterationParameters
from cmdb.manager.errors import ManagerGetError, ManagerInsertError, ManagerUpdateError, ManagerDeleteError, \
    ManagerIterationError
from cmdb.framework.results.iteration import IterationResult
from cmdb.framework.managers.type_manager import TypeManager
from cmdb.framework.utils import PublicID
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetMultiResponse, GetSingleResponse, InsertSingleResponse, UpdateSingleResponse, \
    DeleteSingleResponse
from cmdb.framework.cmdb_location_manager import CmdbLocationManager
from cmdb.framework.cmdb_location import CmdbLocation

LOGGER = logging.getLogger(__name__)
type_blueprint = APIBlueprint('type', __name__)


@type_blueprint.route('/', methods=['GET', 'HEAD'])
@type_blueprint.protect(auth=True, right='base.framework.type.view')
@type_blueprint.parse_parameters(TypeIterationParameters)
def get_types(params: TypeIterationParameters):
    """
    HTTP `GET`/`HEAD` route for getting a iterable collection of resources.

    Args:
        params (CollectionParameters): Passed parameters over the http query string

    Returns:
        GetMultiResponse: Which includes a IterationResult of the TypeModel.

    Example:
        You can pass any parameter based on the CollectionParameters.
        Optional parameters are passed over the function declaration.

    Raises:
        FrameworkIterationError: If the collection could not be iterated.
        ManagerGetError: If the collection could not be found.

    """
    type_manager = TypeManager(database_manager=current_app.database_manager)
    body = request.method == 'HEAD'
    view = params.active
    if view:
        if isinstance(params.filter, dict):
            if params.filter.keys():
                params.filter.update({'active': view})
            else:
                params.filter = [{'$match': {'active': view}}, {'$match': params.filter}]
        elif isinstance(params.filter, list):
            params.filter.append({'$match': {'active': view}})
    try:
        iteration_result: IterationResult[TypeModel] = type_manager.iterate(
            filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
        types = [TypeModel.to_json(type) for type in iteration_result.results]
        api_response = GetMultiResponse(types, total=iteration_result.total, params=params,
                                        url=request.url, model=TypeModel.MODEL, body=body)
    except ManagerIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


@type_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@type_blueprint.protect(auth=True, right='base.framework.type.view')
def get_type(public_id: int):
    """
    HTTP `GET`/`HEAD` route for a single type resource.

    Args:
        public_id (int): Public ID of the type.

    Raises:
        ManagerGetError: When the selected type does not exists.

    Returns:
        GetSingleResponse: Which includes the json data of a TypeModel.
    """
    type_manager = TypeManager(database_manager=current_app.database_manager)
    body = request.method == 'HEAD'

    try:
        type_ = type_manager.get(public_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    api_response = GetSingleResponse(TypeModel.to_json(type_), url=request.url,
                                     model=TypeModel.MODEL, body=body)
    return api_response.make_response()


@type_blueprint.route('/', methods=['POST'])
@type_blueprint.protect(auth=True, right='base.framework.type.add')
@type_blueprint.validate(TypeModel.SCHEMA)
def insert_type(data: dict):
    """
    HTTP `POST` route for insert a single type resource.

    Args:
        data (TypeModel.SCHEMA): Insert data of a new type.

    Raises:
        ManagerGetError: If the inserted resource could not be found after inserting.
        ManagerInsertError: If something went wrong during insertion.

    Returns:
        InsertSingleResponse: Insert response with the new type and its public_id.
    """
    type_manager = TypeManager(database_manager=current_app.database_manager)
    data.setdefault('creation_time', datetime.now(timezone.utc))
    possible_id = data.get('public_id', None)
    if possible_id:
        try:
            type_manager.get(public_id=possible_id)
        except ManagerGetError:
            pass
        else:
            return abort(400, f'Type with PublicID {possible_id} already exists.')

    try:
        result_id: PublicID = type_manager.insert(data)
        raw_doc = type_manager.get(public_id=result_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerInsertError as err:
        return abort(400, err.message)
    api_response = InsertSingleResponse(result_id=result_id, raw=TypeModel.to_json(raw_doc), url=request.url,
                                        model=TypeModel.MODEL)
    return api_response.make_response(prefix='types')


@type_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@type_blueprint.protect(auth=True, right='base.framework.type.edit')
@type_blueprint.validate(TypeModel.SCHEMA)
def update_type(public_id: int, data: dict):
    """
    HTTP `PUT`/`PATCH` route for update a single type resource.

    Args:
        public_id (int): Public ID of the updatable type
        data (TypeModel.SCHEMA): New type data to update

    Raises:
        ManagerGetError: When the type with the `public_id` was not found.
        ManagerUpdateError: When something went wrong during the update.

    Returns:
        UpdateSingleResponse: With update result of the new updated type.
    """
    type_manager = TypeManager(database_manager=current_app.database_manager)
    location_manager = CmdbLocationManager(current_app.database_manager, current_app.event_queue)
    try:

        data.setdefault('last_edit_time', datetime.now(timezone.utc))
        type_ = TypeModel.from_data(data=data)

        type_manager.update(public_id=PublicID(public_id), type=TypeModel.to_json(type_))

        api_response = UpdateSingleResponse(result=data, url=request.url, model=TypeModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerUpdateError as err:
        return abort(400, err.message)
    

    # when types are updated, update all locations with relevant data from this type
    updated_type = type_manager.get(public_id)
    locations_with_type = location_manager.get_locations_by_type(public_id)

    data = {
        'type_label': updated_type.label,
        'type_icon': updated_type.render_meta.icon,
        'type_selectable': updated_type.selectable_as_parent
    }

    for location in locations_with_type:
        location_manager._update(CmdbLocation.COLLECTION, location.public_id, data)

    return api_response.make_response()


@type_blueprint.route('/<int:public_id>', methods=['DELETE'])
@type_blueprint.protect(auth=True, right='base.framework.type.delete')
def delete_type(public_id: int):
    """
    HTTP `DELETE` route for delete a single type resource.

    Args:
        public_id (int): Public ID of the deletable type

    Raises:
        ManagerGetError: When the type with the `public_id` was not found.
        ManagerDeleteError: When something went wrong during the deletion.

    Notes:
        Deleting the type will also delete all objects in this type!

    Returns:
        DeleteSingleResponse: Delete result with the deleted type as data.
    """
    type_manager = TypeManager(database_manager=current_app.database_manager)
    from cmdb.framework.cmdb_object_manager import CmdbObjectManager
    deprecated_object_manager = CmdbObjectManager(database_manager=current_app.database_manager)

    try:
        objects_ids = [object_.get_public_id() for object_ in deprecated_object_manager.get_objects_by_type(public_id)]
        deprecated_object_manager.delete_many_objects({'type_id': public_id}, objects_ids, None)
        deleted_type = type_manager.delete(public_id=PublicID(public_id))
        api_response = DeleteSingleResponse(raw=TypeModel.to_json(deleted_type), model=TypeModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerDeleteError as err:
        return abort(400, err.message)
    except Exception as err:
        return abort(400, str(err))
    return api_response.make_response()
