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
"""Definition of all routes for Locations"""
import logging
from flask import request, current_app, abort

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.manager.locations_manager import LocationsManager
from cmdb.manager.types_manager import TypesManager
from cmdb.manager.objects_manager import ObjectsManager

from cmdb.models.user_model.user import UserModel
from cmdb.models.location_model.location_node import LocationNode
from cmdb.models.location_model.cmdb_location import CmdbLocation
from cmdb.framework.rendering.render_list import RenderList
from cmdb.framework.results import IterationResult
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import (
    UpdateSingleResponse,
    GetMultiResponse,
    DefaultResponse,
)

from cmdb.errors.manager import ManagerInsertError,\
                                ManagerIterationError,\
                                ManagerGetError,\
                                ManagerUpdateError,\
                                ManagerDeleteError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

location_blueprint = APIBlueprint('locations', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@location_blueprint.route('/', methods=['POST'])
@location_blueprint.parse_request_parameters()
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@location_blueprint.protect(auth=True, right='base.framework.object.edit')
def create_location(params: dict, request_user: UserModel):
    """
    Creates a location in the database

    Args:
        params (dict): location parameters
        request_user (UserModel): User requesting the creation of a location

    Returns:
        int: public_id of the created location
    """
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)
    locations_manager: LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS_MANAGER, request_user)
    objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

    location_creation_params= {}

    location_creation_params['object_id'] = int(params['object_id'])
    location_creation_params['parent'] = int(params['parent'])
    location_creation_params['type_id'] = int(params['type_id'])

    object_type = types_manager.get_type(location_creation_params['type_id'])

    location_creation_params['type_label'] = object_type.label
    location_creation_params['type_icon'] = object_type.get_icon()
    location_creation_params['type_selectable'] = object_type.selectable_as_parent

    location_creation_params['public_id'] = locations_manager.get_next_public_id()

    if params['name'] == '' or params['name'] is None:
        current_object = objects_manager.get_object(int(params['object_id']))

        if current_app.cloud_mode:
            current_app.database_manager.connector.set_database(request_user.database)

        rendered_list = RenderList([current_object],
                                   request_user,
                                   True,
                                   objects_manager).render_result_list(True)

        params['name'] = rendered_list[0]['summary_line']

    location_creation_params['name'] =  params['name'] if params['name'] not in ['', None]\
                                                       else f"ObjectID: {location_creation_params['object_id']}"

    try:
        created_location_id = locations_manager.insert_location(location_creation_params)
    except ManagerInsertError as err:
        LOGGER.debug("[ManagerInsertError] ManagerInsertError: %s", err.message)
        return abort(400, "Could not insert the new location in database)!")

    api_response = DefaultResponse(created_location_id)

    return api_response.make_response()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@location_blueprint.route('/', methods=['GET', 'HEAD'])
@location_blueprint.parse_collection_parameters(view='native')
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@location_blueprint.protect(auth=True, right='base.framework.object.view')
def get_all_locations(params: CollectionParameters, request_user: UserModel):
    """
    Returns all locations based on the params

    Args:
        params (CollectionParameters): params for locations request
        request_user (UserModel): User requesting the data

    Returns:
        (Response): All locations considering the params
    """
    locations_manager: LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS_MANAGER, request_user)

    try:
        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))
        iteration_result: IterationResult[CmdbLocation] = locations_manager.iterate(builder_params)

        location_list: list[dict] = [location_.__dict__ for location_ in iteration_result.results]

        api_response = GetMultiResponse(location_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        request.method == 'HEAD')

    except ManagerIterationError as err:
        LOGGER.debug("[get_all_locations] ManagerIterationError: %s", err.message)
        return abort(400, "Could not retrieve locations from database!")

    return api_response.make_response()


@location_blueprint.route('/tree', methods=['GET', 'HEAD'])
@location_blueprint.parse_collection_parameters()
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@location_blueprint.protect(auth=True, right='base.framework.object.view')
def get_locations_tree(params: CollectionParameters, request_user: UserModel):
    """
    Returns all locations as a location tree

    Args:
        params (CollectionParameters): params for location tree (excluding root location)
        request_user (UserModel): User requesting the data

    Returns:
        list: locations as a tree
    """
    locations_manager: LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS_MANAGER, request_user)

    try:
        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))
        iteration_result: IterationResult[CmdbLocation] = locations_manager.iterate(builder_params)

        location_list: list[dict] = [location_.__dict__ for location_ in iteration_result.results]
        # get all root locations
        filtered_location_list = []
        root_locations: list[LocationNode] = []

        for location in location_list:
            if location['parent'] == 1:
                root_locations.append(LocationNode(location))
            else:
                filtered_location_list.append(location)

        # get all children for each root location
        for root_location in root_locations:
            children = root_location.get_children(root_location.public_id, filtered_location_list)
            root_location.children = children

        # pack the root locations
        packed_locations = []

        for root_location in root_locations:
            packed_locations.append(root_location.to_json(root_location))

        api_response = GetMultiResponse(packed_locations,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        request.method == 'HEAD')

    except ManagerIterationError as err:
        LOGGER.debug("[get_locations_tree] ManagerIterationError: %s", err.message)
        return abort(400, "Could not retrieve locations from database!")

    return api_response.make_response()


@location_blueprint.route('/<int:public_id>', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@location_blueprint.protect(auth=True, right='base.framework.object.view')
def get_location(public_id: int, request_user: UserModel):
    """
    Returns the selected location for a given public_id
    
    Args:
        public_id (int): public_id of location
        request_user (UserModel): User which is requesting the data
    """
    locations_manager: LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS_MANAGER, request_user)

    try:
        location_instance = locations_manager.get_location(public_id)
    except ManagerGetError as err:
        LOGGER.debug("[get_location] ManagerGetError: %s", err.message)
        return abort(404, "Could not retrieve the location from database!")

    api_response = DefaultResponse(location_instance)

    return api_response.make_response()


@location_blueprint.route('/<int:object_id>/object', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@location_blueprint.protect(auth=True, right='base.framework.object.view')
def get_location_for_object(object_id: int, request_user: UserModel):
    """
    Returns the selected location for a given object_id
    
    Args:
        object_id (int): object_id of object 
        request_user (UserModel): User which is requesting the data
    """
    locations_manager: LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS_MANAGER, request_user)

    try:
        location_instance = locations_manager.get_location_for_object(object_id)
    except ManagerGetError as err:
        LOGGER.debug("[get_location_for_object] ManagerGetError: %s", err.message)
        return abort(404, "Could not retrieve the location from database!")

    api_response = DefaultResponse(location_instance)

    return api_response.make_response()


@location_blueprint.route('/<int:object_id>/parent', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@location_blueprint.protect(auth=True, right='base.framework.object.view')
def get_parent(object_id: int, request_user: UserModel):
    """
    Returns the parent location for a given object_id
    
    Args:
        object_id (int): object_id of object 
        request_user (UserModel): User which is requesting the data
    """
    locations_manager: LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS_MANAGER, request_user)

    parent = None

    try:
        current_location = locations_manager.get_location_for_object(object_id)

        if current_location:
            parent_id = current_location.parent
            parent = locations_manager.get_location(parent_id)
    except Exception as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_parent] Exception: %s, Type: %s", err, type(err))

    api_response = DefaultResponse(parent)

    return api_response.make_response()


@location_blueprint.route('/<int:object_id>/children', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@location_blueprint.protect(auth=True, right='base.framework.object.view')
def get_children(object_id: int, request_user: UserModel):
    """
    Get all children of next level for a given object_id
    
    Args:
        object_id (int): object_id of object 
        request_user (UserModel): User which is requesting the data
    
    Returns:
        (Response): All children of next level for the given object_id
    """
    locations_manager: LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS_MANAGER, request_user)

    children = []

    try:
        current_location = locations_manager.get_location_for_object(object_id)

        if current_location:
            location_public_id = current_location.public_id
            children = locations_manager.get_locations_by(parent=location_public_id)

    except Exception as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_children] Exception: %s, Type: %s", err, type(err))

    api_response = DefaultResponse(children)

    return api_response.make_response()

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@location_blueprint.route('/update_location', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@location_blueprint.protect(auth=True, right='base.framework.object.edit')
@location_blueprint.parse_request_parameters()
def update_location_for_object(params: dict, request_user: UserModel):
    """
    Updates a location

    Args:
        params (dict): location parameters
        request_user (UserModel): User requesting the update
    Returns:
        UpdateSingleResponse: with acknowledged from database
    """
    locations_manager: LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS_MANAGER, request_user)
    objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

    location_update_params = {}

    object_id = int(params['object_id'])
    location_update_params['parent'] = int(params['parent'])

    if params['name'] == '' or params['name'] is None:
        current_object = objects_manager.get_object(object_id)

        if current_app.cloud_mode:
            current_app.database_manager.connector.set_database(request_user.database)

        rendered_list = RenderList([current_object],
                                   request_user,
                                   True,
                                   objects_manager).render_result_list(raw=True)

        params['name'] = rendered_list[0]['summary_line']

    location_update_params['name'] =  params['name'] if params['name'] not in ['', None]\
                                                     else f"ObjectID: {location_update_params['object_id']}"

    try:
        result = locations_manager.update({'object_id': object_id}, location_update_params)
    except ManagerUpdateError as err:
        LOGGER.debug("[update_location_for_object] ManagerUpdateError: %s", err.message)
        return abort(400, "Could not update the location!")

    api_response = UpdateSingleResponse(result)

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@location_blueprint.route('/<int:object_id>/object', methods=['DELETE'])
@insert_request_user
@location_blueprint.protect(auth=True, right='base.framework.object.edit')
def delete_location_for_object(object_id: int, request_user: UserModel):
    """
    Deletes a location where the object_id is assigned 

    Args:
        request_user (UserModel): user making the request
    Returns:
        bool: Confirmation for deletion
    """
    locations_manager:LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS_MANAGER, request_user)

    try:
        current_location_instance = locations_manager.get_location_for_object(object_id)
        location_public_id = current_location_instance.public_id

        ack = locations_manager.delete({'public_id':location_public_id})
    except ManagerGetError as err:
        LOGGER.debug("[delete_location_for_object] ManagerGetError: %s", err.message)
        return abort(404, "Could not retrieve the location which should be deleted!")
    except ManagerDeleteError as err:
        LOGGER.debug("[delete_location_for_object] ManagerDeleteError: %s", err.message)
        return abort(400, f"Could not delete the location with ID: {object_id} !")

    api_response = DefaultResponse(ack)

    return api_response.make_response()
