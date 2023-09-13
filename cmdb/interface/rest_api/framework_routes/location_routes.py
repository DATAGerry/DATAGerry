
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

"""
Definition of all routes for locations
"""
import logging
from typing import List
from flask import abort, request, current_app

from cmdb.framework import CmdbLocation
from cmdb.framework.cmdb_errors import LocationManagerDeleteError, LocationManagerGetError, ObjectManagerUpdateError
from cmdb.framework.models.log import LogAction, CmdbObjectLog
from cmdb.framework.managers.log_manager import LogManagerInsertError, CmdbLogManager
from cmdb.framework.cmdb_location_manager import CmdbLocationManager
from cmdb.framework.cmdb_render import RenderList
from cmdb.framework.managers.type_manager import TypeManager
from cmdb.framework.results import IterationResult
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import GetMultiResponse, UpdateSingleResponse, ResponseFailedMessage
from cmdb.interface.route_utils import make_response, insert_request_user
from cmdb.interface.blueprint import APIBlueprint
from cmdb.manager import ManagerIterationError, ManagerGetError
from cmdb.security.acl.errors import AccessDeniedError
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel, UserManager
from cmdb.utils.error import CMDBError
from cmdb.framework.managers.location_manager import LocationManager
from cmdb.framework.cmdb_object_manager import CmdbObjectManager


# get required managers
with current_app.app_context():
    location_manager = CmdbLocationManager(current_app.database_manager, current_app.event_queue)
    type_manager = TypeManager(database_manager=current_app.database_manager)
    log_manager = CmdbLogManager(current_app.database_manager)
    user_manager = UserManager(current_app.database_manager)
    object_manager = CmdbObjectManager(current_app.database_manager, current_app.event_queue)

LOGGER = logging.getLogger(__name__)
location_blueprint = APIBlueprint('locations', __name__)


class LocationNode:
    """
    Represents a node in the location tree
    """
    def __init__(self, params: dict):
        self.public_id: int = params['public_id']
        self.name: str = params['name']
        self.parent: int = params['parent']
        self.icon: str = params['type_icon']
        self.object_id: int = params['object_id']
        self.children: list[LocationNode] = []

    def get_children(self, public_id:int, locations_list: list[dict]):
        """
        Gets recursively all children for a location

        Args:
            public_id (int): public:id of the location
            locations_list (list): list of locations from database

        Returns:
            list[LocationNode]: returns all children for the given public_id
        """
        sorted_children: list["LocationNode"] = []
        filtered_list: list[dict] = []

        if len(locations_list) > 0:
            for location in locations_list:
                if location['parent'] == public_id:
                    sorted_children.append(LocationNode(location))
                else:
                    filtered_list.append(location)

            if len(filtered_list) > 0:
                for child in sorted_children:
                    child.children = self.get_children(child.get_public_id(), filtered_list)
        return sorted_children


    def get_public_id(self):
        """
        Returns the public_id of this LocationNode

        Returns:
            (int): public_id of this LocationNode
        """
        return self.public_id

    def __repr__(self) -> str:
        return f"[LocationNode => public_id: {self.public_id}, \
                                  name: {self.name}, \
                                  parent: {self.parent}, \
                                  icon: {self.icon}, \
                                  object_id: {self.object_id}, \
                                  children: {len(self.children)}]"

    @classmethod
    def to_json(cls, instance: "LocationNode") -> dict:
        """Convert a ExportdJobLog instance to json conform data"""

        json_data = {
            'public_id': instance.public_id,
            'name': instance.name,
            'parent': instance.parent,
            'icon': instance.icon,
            'object_id': instance.object_id,
        }

        # convert children to json
        children = []
        if len(instance.children) > 0:
            for child in instance.children:
                children.append(cls.to_json(child))

        # if there were any children then append the children-key
        if len(children) > 0:
            json_data['children'] = children

        return json_data

# ---------------------------------------------------------------------------- #
#                                CRUD - SECTION                                #
# ---------------------------------------------------------------------------- #


# ------------------------------- CRUD - CREATE ------------------------------ #

@location_blueprint.route('/', methods=['POST'])
@location_blueprint.protect(auth=True, right='base.framework.object.edit')
@location_blueprint.parse_location_parameters()
@insert_request_user
def create_location(params: dict, request_user: UserModel):
    """
    Creates a location in the database

    Args:
        params (dict): location parameters
        request_user (UserModel): User requesting the creation of a location

    Returns:
        int: public_id of the created location
    """
    location_creation_params= {}

    location_creation_params['object_id'] = int(params['object_id'])
    location_creation_params['parent'] = int(params['parent'])
    location_creation_params['type_id'] = int(params['type_id'])

    object_type = type_manager.get(location_creation_params['type_id'])

    location_creation_params['type_label'] = object_type.label
    location_creation_params['type_icon'] = object_type.get_icon()
    location_creation_params['type_selectable'] = object_type.selectable_as_parent

    location_creation_params['public_id'] = location_manager.get_new_id(CmdbLocation.COLLECTION)

    if params['name'] == '' or params['name'] is None:
        current_object = object_manager.get_object(int(params['object_id']))

        rendered_list = RenderList([current_object], request_user, current_app.database_manager, True,
                                    object_manager=object_manager ).render_result_list(raw=True)

        params['name'] = rendered_list[0]['summary_line']



    location_creation_params['name'] =  params['name'] if params['name'] not in ['', None] else f"ObjectID: {location_creation_params['object_id']}"

    created_location_id = location_manager.insert_location(location_creation_params, request_user, AccessControlPermission.CREATE)

    return make_response(created_location_id)


# -------------------------------- CRUD - READ ------------------------------- #


@location_blueprint.route('/', methods=['GET', 'HEAD'])
@location_blueprint.protect(auth=True, right='base.framework.object.view')
@location_blueprint.parse_collection_parameters(view='native')
@insert_request_user
def get_all_locations(params: CollectionParameters, request_user: UserModel):
    """
    Returns all locations based on the params

    Args:
        params (CollectionParameters): params for locations request
        request_user (UserModel): User requesting the data

    Returns:
        (Response): All locations considering the params
    """

    manager = LocationManager(database_manager=current_app.database_manager)

    try:
        iteration_result: IterationResult[CmdbLocation] = manager.iterate(
            filter=params.filter,
            limit=params.limit,
            skip=params.skip,
            sort=params.sort,
            order=params.order,
            user=request_user,
            permission=AccessControlPermission.READ
        )

        location_list: List[dict] = [location_.__dict__ for location_ in iteration_result.results]
        api_response = GetMultiResponse(location_list, total=iteration_result.total, params=params,
                                            url=request.url, model=CmdbLocation.MODEL, body=request.method == 'HEAD')

    except ManagerIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)


    return api_response.make_response()


@location_blueprint.route('/tree', methods=['GET', 'HEAD'])
@location_blueprint.protect(auth=True, right='base.framework.object.view')
@location_blueprint.parse_collection_parameters()
@insert_request_user
def get_locations_tree(params: CollectionParameters, request_user: UserModel):
    """
    Returns all locations as a location tree

    Args:
        params (CollectionParameters): params for location tree (excluding root location)
        request_user (UserModel): User requesting the data

    Returns:
        _type_: _description_
    """
    manager = LocationManager(database_manager=current_app.database_manager)

    try:
        iteration_result: IterationResult[CmdbLocation] = manager.iterate(
            filter=params.filter,
            limit=params.limit,
            skip=params.skip,
            sort=params.sort,
            order=params.order,
            user=request_user,
            permission=AccessControlPermission.READ
        )

        location_list: List[dict] = [location_.__dict__ for location_ in iteration_result.results]
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

        api_response = GetMultiResponse(packed_locations, total=iteration_result.total, params=params,
                                            url=request.url, model=CmdbLocation.MODEL, body=request.method == 'HEAD')

    except ManagerIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)

    return api_response.make_response()


@location_blueprint.route('/<int:public_id>', methods=['GET'])
@location_blueprint.protect(auth=True, right='base.framework.object.view')
@insert_request_user
def get_location(public_id: int, request_user: UserModel):
    """
    Returns the selected location for a given public_id
    
    Args:
        public_id (int): public_id of location
        request_user (UserModel): User which is requesting the data
    """
    try:
        location_instance = location_manager.get_location(public_id, user=request_user,
                                                    permission=AccessControlPermission.READ)
    except (LocationManagerGetError, ManagerGetError) as err:
        return abort(404, err.message)
    except AccessDeniedError as err:
        return abort(403, err.message)

    resp = make_response(location_instance)
    return resp


@location_blueprint.route('/<int:object_id>/object', methods=['GET'])
@location_blueprint.protect(auth=True, right='base.framework.object.view')
@insert_request_user
def get_location_for_object(object_id: int, request_user: UserModel):
    """
    Returns the selected location for a given object_id
    
    Args:
        object_id (int): object_id of object 
        request_user (UserModel): User which is requesting the data
    """
    try:
        location_instance = location_manager.get_location_for_object(object_id, user=request_user,
                                                    permission=AccessControlPermission.READ)
    except (LocationManagerGetError, ManagerGetError) as err:
        return abort(404, err.message)
    except AccessDeniedError as err:
        return abort(403, err.message)

    return make_response(location_instance)


@location_blueprint.route('/<int:object_id>/parent', methods=['GET'])
@location_blueprint.protect(auth=True, right='base.framework.object.view')
@insert_request_user
def get_parent(object_id: int, request_user: UserModel):
    """
    Returns the parent location for a given object_id
    
    Args:
        object_id (int): object_id of object 
        request_user (UserModel): User which is requesting the data
    """
    parent = None

    try:
        current_location = location_manager.get_location_for_object(object_id, user=request_user,
                                                    permission=AccessControlPermission.READ)

        if current_location:
            parent_id = current_location.parent
            parent = location_manager.get_location(parent_id, request_user, AccessControlPermission.READ)

    except (LocationManagerGetError, ManagerGetError) as err:
        return abort(404, err.message)
    except AccessDeniedError as err:
        return abort(403, err.message)

    return make_response(parent)

@location_blueprint.route('/<int:object_id>/children', methods=['GET'])
@location_blueprint.protect(auth=True, right='base.framework.object.view')
@insert_request_user
def get_children(object_id: int, request_user: UserModel):
    """
    Get all children of next level for a given object_id
    
    Args:
        object_id (int): object_id of object 
        request_user (UserModel): User which is requesting the data
    
    Returns:
        (Response): All children of next level for the given object_id
    """
    children = []

    try:
        current_location = location_manager.get_location_for_object(object_id, user=request_user,
                                                    permission=AccessControlPermission.READ)
        if current_location:
            location_public_id = current_location.public_id
            children = location_manager.get_locations_by(parent=location_public_id)

    except (LocationManagerGetError, ManagerGetError) as err:
        return abort(404, err.message)

    return make_response(children)

# ------------------------------- CRUD - UPDATE ------------------------------ #

@location_blueprint.route('/update_location', methods=['PUT', 'PATCH'])
@location_blueprint.protect(auth=True, right='base.framework.object.edit')
@location_blueprint.parse_location_parameters()
@insert_request_user
def update_location_for_object(params: dict, request_user: UserModel):
    """
    Updates a location

    Args:
        params (dict): location parameters
        request_user (UserModel): User requesting the update

    Returns:
        _type_: _description_
    """
    location_update_params = {}
    failed: ResponseFailedMessage = []

    object_id = int(params['object_id'])
    location_update_params['parent'] = int(params['parent'])

    if params['name'] == '' or params['name'] is None:
        current_object = object_manager.get_object(object_id)

        rendered_list = RenderList([current_object], request_user, current_app.database_manager, True,
                                    object_manager=object_manager ).render_result_list(raw=True)

        params['name'] = rendered_list[0]['summary_line']

    location_update_params['name'] =  params['name'] if params['name'] not in ['', None] else f"ObjectID: {location_update_params['object_id']}"

    try:
        result = location_manager._update_for_object(CmdbLocation.COLLECTION, object_id, location_update_params)

    except (LocationManagerGetError, ManagerGetError, ObjectManagerUpdateError) as error:
        failed.append(ResponseFailedMessage(error_message=error.message, status=404,
                                                public_id=object_id, obj=location_update_params).to_dict())


    api_response = UpdateSingleResponse(result, failed, request.url, CmdbLocation.MODEL)

    return api_response.make_response()


# ------------------------------- CRUD - DELETE ------------------------------ #


@location_blueprint.route('/<int:object_id>/object', methods=['DELETE'])
@location_blueprint.protect(auth=True, right='base.framework.object.edit')
@insert_request_user
def delete_location_for_object(object_id: int, request_user: UserModel):
    """
    Deletes a location where the object_id assigned 

    Args:
        request_user (UserModel): user making the request

    Returns:
        _type_: confirmation for deletion
    """
    try:
        current_location_instance = location_manager.get_location_for_object(object_id)
        location_public_id = current_location_instance.public_id

        # delete is only allowed if this location don't have any children
        has_children = location_manager.has_children(location_public_id)

        if has_children:
            raise LocationManagerDeleteError('Deleting is only possbile if there are no children for this location')

        ack = location_manager.delete_location(public_id=location_public_id,
                                               user=request_user,
                                               permission=AccessControlPermission.DELETE)
    except LocationManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    except LocationManagerDeleteError as err:
        LOGGER.error(err)
        return abort(405)
    except AccessDeniedError as err:
        LOGGER.error(err)
        return abort(403, err.message)
    except CMDBError:
        return abort(500)

    # try:
    #     # generate log
    #     log_data = {
    #         'object_id': public_id,
    #         'version': current_object_render_result.object_information['version'],
    #         'user_id': request_user.get_public_id(),
    #         'user_name': request_user.get_display_name(),
    #         'comment': 'Object was deleted',
    #         'render_state': json.dumps(current_object_render_result, default=default).encode('UTF-8')
    #     }
    #     log_manager.insert(action=LogAction.DELETE, log_type=CmdbObjectLog.__name__, **log_data)
    # except (CMDBError, LogManagerInsertError) as err:
    #     LOGGER.error(err)
    return make_response(ack)
