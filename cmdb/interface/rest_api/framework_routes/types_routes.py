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
"""TODO: document"""
import logging
from datetime import datetime, timezone
from flask import abort, request

from cmdb.manager.type_manager import TypeManager
from cmdb.manager.locations_manager import LocationsManager
from cmdb.manager.object_manager import ObjectManager
from cmdb.manager.cmdb_object_manager import CmdbObjectManager

from cmdb.framework.models.type import TypeModel
from cmdb.interface.rest_api.framework_routes.type_parameters import TypeIterationParameters
from cmdb.framework.results.iteration import IterationResult
from cmdb.framework.utils import PublicID
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetMultiResponse, GetSingleResponse, InsertSingleResponse, UpdateSingleResponse, \
    DeleteSingleResponse, make_api_response
from cmdb.cmdb_objects.cmdb_location import CmdbLocation
from cmdb.cmdb_objects.cmdb_object import CmdbObject
from cmdb.interface.route_utils import insert_request_user
from cmdb.user_management.models.user import UserModel
from cmdb.manager.manager_provider import ManagerType, ManagerProvider

from cmdb.errors.manager import ManagerGetError,\
                                ManagerInsertError,\
                                ManagerUpdateError,\
                                ManagerDeleteError,\
                                ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

types_blueprint = APIBlueprint('types', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@types_blueprint.route('/', methods=['POST'])
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.add')
@types_blueprint.validate(TypeModel.SCHEMA)
def insert_type(data: dict, request_user: UserModel):
    """
    HTTP `POST` route for insert a single type resource

    Args:
        data (TypeModel.SCHEMA): Insert data of a new type

    Raises:
        ManagerGetError: If the inserted resource could not be found after inserting
        ManagerInsertError: If something went wrong during insertion

    Returns:
        InsertSingleResponse: Insert response with the new type and its public_id
    """
    type_manager: TypeManager = ManagerProvider.get_manager(ManagerType.TYPE_MANAGER, request_user)

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
    except ManagerGetError:
        #TODO: ERROR-FIX
        return abort(404)
    except ManagerInsertError as err:
        LOGGER.debug("[insert_type] ManagerInsertError: %s", err.message)
        return abort(400, "The Type could not be inserted !")

    api_response = InsertSingleResponse(result_id=result_id,
                                        raw=TypeModel.to_json(raw_doc),
                                        url=request.url,
                                        model=TypeModel.MODEL)

    return api_response.make_response(prefix='types')

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@types_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.view')
@types_blueprint.parse_parameters(TypeIterationParameters)
def get_types(params: TypeIterationParameters, request_user: UserModel):
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
        ManagerGetError: If the collection could not be found.

    """
    type_manager: TypeManager = ManagerProvider.get_manager(ManagerType.TYPE_MANAGER, request_user)

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
                                                                        filter=params.filter,
                                                                        limit=params.limit,
                                                                        skip=params.skip,
                                                                        sort=params.sort,
                                                                        order=params.order)

        types = [TypeModel.to_json(type) for type in iteration_result.results]

        api_response = GetMultiResponse(types,
                                        total=iteration_result.total,
                                        params=params,
                                        url=request.url,
                                        model=TypeModel.MODEL,
                                        body=request.method == 'HEAD')
    except ManagerIterationError:
        #TODO: ERROR-FIX
        return abort(400)
    except ManagerGetError:
        #TODO: ERROR-FIX
        return abort(404)

    return api_response.make_response()


@types_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.view')
def get_type(public_id: int, request_user: UserModel):
    """
    HTTP `GET`/`HEAD` route for a single type resource.

    Args:
        public_id (int): Public ID of the type.

    Raises:
        ManagerGetError: When the selected type does not exists.

    Returns:
        GetSingleResponse: Which includes the json data of a TypeModel.
    """
    type_manager: TypeManager = ManagerProvider.get_manager(ManagerType.TYPE_MANAGER, request_user)

    try:
        type_ = type_manager.get(public_id)
    except ManagerGetError:
        return abort(404)
    api_response = GetSingleResponse(TypeModel.to_json(type_), url=request.url,
                                     model=TypeModel.MODEL, body=request.method == 'HEAD')

    return api_response.make_response()


@types_blueprint.route('/<int:public_id>/count_objects', methods=['GET'])
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.read')
def count_objects(public_id: int, request_user: UserModel):
    """
    Return the number of objects in der database with the given public_id as type_id
    Args:
        public_id (int): public_id of the type
    """
    object_manager: ObjectManager = ManagerProvider.get_manager(ManagerType.OBJECT_MANAGER, request_user)

    try:
        objects_count = object_manager.count_objects(public_id)
    except ManagerGetError:
        #TODO: ERROR-FIX
        return abort(404)

    return make_api_response(objects_count)

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@types_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.edit')
@types_blueprint.validate(TypeModel.SCHEMA)
def update_type(public_id: int, data: dict, request_user: UserModel):
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
    type_manager: TypeManager = ManagerProvider.get_manager(ManagerType.TYPE_MANAGER, request_user)
    locations_manager: LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS_MANAGER, request_user)
    object_manager: ObjectManager = ManagerProvider.get_manager(ManagerType.OBJECT_MANAGER, request_user)

    try:
        unchanged_type = type_manager.get(public_id)

        data.setdefault('last_edit_time', datetime.now(timezone.utc))
        type_ = TypeModel.from_data(data=data)
        type_manager.update(public_id=PublicID(public_id), type=TypeModel.to_json(type_))
        api_response = UpdateSingleResponse(result=data, url=request.url, model=TypeModel.MODEL)
    except ManagerGetError:
        #TODO: ERROR-FIX
        return abort(404)
    except ManagerUpdateError as err:
        LOGGER.debug("[update_type] ManagerUpdateError: %s", err.message)
        return abort(400, f"Type with public_id: {public_id} could not be updated!")

    # when types are updated, update all locations with relevant data from this type
    updated_type = type_manager.get(public_id)
    locations_with_type = locations_manager.get_locations_by(type_id=public_id)

    loc_data = {
        'type_label': updated_type.label,
        'type_icon': updated_type.render_meta.icon,
        'type_selectable': updated_type.selectable_as_parent
    }

    location: CmdbLocation
    for location in locations_with_type:
        locations_manager.update({'public_id':location.public_id}, loc_data)

    # check and update all multi data sections for the type if required
    updated_objects = type_manager.handle_mutli_data_sections(unchanged_type, data)

    an_object: CmdbObject
    for an_object in updated_objects:
        object_manager._update(object_manager.collection, {'public_id': an_object.public_id}, CmdbObject.to_json(an_object))

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@types_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.delete')
def delete_type(public_id: int, request_user: UserModel):
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
    type_manager: TypeManager = ManagerProvider.get_manager(ManagerType.TYPE_MANAGER, request_user)
    object_manager: ObjectManager = ManagerProvider.get_manager(ManagerType.OBJECT_MANAGER, request_user)
    deprecated_object_manager: CmdbObjectManager = ManagerProvider.get_manager(ManagerType.CMDB_OBJECT_MANAGER,
                                                                               request_user)

    try:
        objects_count = object_manager.count_objects(public_id)

        if objects_count > 0:
            raise ManagerDeleteError('Delete not possible if objects of this type exist')

        objects_ids = [object_.get_public_id() for object_ in deprecated_object_manager.get_objects_by_type(public_id)]
        deprecated_object_manager.delete_many_objects({'type_id': public_id}, objects_ids, None)
        deleted_type = type_manager.delete(public_id=PublicID(public_id))

        api_response = DeleteSingleResponse(raw=TypeModel.to_json(deleted_type), model=TypeModel.MODEL)
    except ManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[delete_type] ManagerGetError: %s", err.message)
        return abort(404)
    except ManagerDeleteError as err:
        LOGGER.debug("[delete_type] ManagerDeleteError: %s", err.message)
        return abort(400, f"Could not delete the type with ID: {public_id}")
    except Exception as err:
        #TODO: ERROR-FIX
        return abort(400)

    return api_response.make_response()
