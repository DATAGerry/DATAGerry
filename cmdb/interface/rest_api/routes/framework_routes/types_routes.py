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

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.manager.types_manager import TypesManager
from cmdb.manager.locations_manager import LocationsManager
from cmdb.manager.objects_manager import ObjectsManager

from cmdb.framework.models.type_model.type import TypeModel
from cmdb.framework.results.iteration import IterationResult
from cmdb.cmdb_objects.cmdb_location import CmdbLocation
from cmdb.cmdb_objects.cmdb_object import CmdbObject
from cmdb.user_management.models.user import UserModel
from cmdb.interface.route_utils import insert_request_user
from cmdb.interface.rest_api.routes.framework_routes.type_parameters import TypeIterationParameters
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import DeleteSingleResponse,\
                                              UpdateSingleResponse,\
                                              InsertSingleResponse,\
                                              GetMultiResponse,\
                                              GetSingleResponse,\
                                              GetSingleValueResponse

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
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)

    data.setdefault('creation_time', datetime.now(timezone.utc))
    possible_id = data.get('public_id', None)

    if possible_id:
        try:
            types_manager.get_type(possible_id)
        except ManagerGetError:
            pass
        else:
            return abort(400, f'Type with PublicID {possible_id} already exists.')

    try:
        result_id = types_manager.insert_type(data)
        raw_doc = types_manager.get_type(result_id)
    except ManagerGetError:
        #ERROR-FIX
        return abort(404)
    except ManagerInsertError as err:
        LOGGER.debug("[insert_type] ManagerInsertError: %s", err.message)
        return abort(400, "The Type could not be inserted !")

    api_response = InsertSingleResponse(result_id=result_id, raw=TypeModel.to_json(raw_doc))

    return api_response.make_response()

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
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)

    view = params.active

    if view:
        if isinstance(params.filter, dict):
            if params.filter.keys():
                params.filter.update({'active': view})
            else:
                params.filter = [{'$match': {'active': view}}, {'$match': params.filter}]
        elif isinstance(params.filter, list):
            params.filter.append({'$match': {'active': view}})

    builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

    try:
        iteration_result: IterationResult[TypeModel] = types_manager.iterate(builder_params)

        types = [TypeModel.to_json(type) for type in iteration_result.results]

        api_response = GetMultiResponse(types,
                                        total=iteration_result.total,
                                        params=params,
                                        url=request.url,
                                        body=request.method == 'HEAD')
    except ManagerIterationError:
        #ERROR-FIX
        return abort(400)
    except ManagerGetError:
        #ERROR-FIX
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
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)

    try:
        type_ = types_manager.get_type(public_id)
    except ManagerGetError:
        return abort(404)
    api_response = GetSingleResponse(TypeModel.to_json(type_), body=request.method == 'HEAD')

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
    objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

    try:
        objects_count = objects_manager.count_objects({'type_id':public_id})
        api_response = GetSingleValueResponse(objects_count)
    except ManagerGetError:
        #ERROR-FIX
        return abort(404)
    except Exception:
        #ERROR-FIX
        return abort(500)

    return api_response.make_response()

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
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)
    locations_manager: LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS_MANAGER, request_user)
    objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

    try:
        unchanged_type = types_manager.get_type(public_id)

        data.setdefault('last_edit_time', datetime.now(timezone.utc))
        type_ = TypeModel.from_data(data=data)
        types_manager.update_type(public_id, TypeModel.to_json(type_))
        api_response = UpdateSingleResponse(result=data)
    except ManagerGetError:
        #ERROR-FIX
        return abort(404)
    except ManagerUpdateError as err:
        LOGGER.debug("[update_type] ManagerUpdateError: %s", err.message)
        return abort(400, f"Type with public_id: {public_id} could not be updated!")

    # when types are updated, update all locations with relevant data from this type
    updated_type = types_manager.get_type(public_id)
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
    updated_objects = types_manager.handle_mutli_data_sections(unchanged_type, data)

    an_object: CmdbObject
    for an_object in updated_objects:
        objects_manager.update_object(an_object.public_id, CmdbObject.to_json(an_object))

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
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)
    objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

    try:
        objects_count = objects_manager.count_objects({'type_id':public_id})

        if objects_count > 0:
            raise ManagerDeleteError('Delete not possible if objects of this type exist')

        objects_ids = [object_.get_public_id() for object_ in objects_manager.get_objects_by(type_id=public_id)]
        objects_manager.delete_many_objects({'type_id': public_id}, objects_ids, None)
        deleted_type = types_manager.delete_type(public_id)

        api_response = DeleteSingleResponse(raw=TypeModel.to_json(deleted_type))
    except ManagerGetError as err:
        #ERROR-FIX
        LOGGER.debug("[delete_type] ManagerGetError: %s", err.message)
        return abort(404)
    except ManagerDeleteError as err:
        LOGGER.debug("[delete_type] ManagerDeleteError: %s", err.message)
        return abort(400, f"Could not delete the type with ID: {public_id}")
    except Exception as err:
        #ERROR-FIX
        return abort(400)

    return api_response.make_response()
