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
"""
Definition of all routes for section templates
"""
import json
import logging
from typing import List

from flask import abort, request, current_app

from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.route_utils import make_response, insert_request_user

from cmdb.user_management import UserModel
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.framework import CmdbSectionTemplate
from cmdb.framework.results import IterationResult
from cmdb.framework.cmdb_section_template_manager import CmdbSectionTemplateManager
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.interface.response import GetMultiResponse, UpdateSingleResponse, ResponseFailedMessage
from cmdb.manager import ManagerIterationError, ManagerGetError
from cmdb.framework.managers.section_template_manager import SectionTemplateManager
from cmdb.framework.cmdb_errors import SectionTemplateManagerGetError, ObjectManagerUpdateError, \
    SectionTemplateManagerDeleteError
from cmdb.security.acl.errors import AccessDeniedError
from cmdb.utils.error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

section_template_blueprint = APIBlueprint('section_templates', __name__)

section_template_manager = CmdbSectionTemplateManager(current_app.database_manager, current_app.event_queue)
manager = SectionTemplateManager(database_manager=current_app.database_manager)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@section_template_blueprint.route('/', methods=['POST'])
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.add')
@section_template_blueprint.parse_location_parameters()
@insert_request_user
def create_section_template(params: dict, request_user: UserModel):
    """
    Creates a section template in the database

    Args:
        params (dict): section template parameters
        request_user (UserModel): User requesting the creation of a section template

    Returns:
        int: public_id of the created section template
    """
    try:
        params['public_id'] = section_template_manager.get_new_id(CmdbSectionTemplate.COLLECTION)
        params['is_global'] = params['is_global'] in ('true', 'True')
        params['predefined'] = params['predefined'] in ('true', 'True')
        params['fields'] = json.loads(params['fields'])
        params['type'] = 'section'

        created_section_template_id = section_template_manager.insert_section_template(
                                                                    params,
                                                                    request_user,
                                                                    AccessControlPermission.CREATE
                                                                )
    except Exception:
        LOGGER.info("Exception in section_template_create")

    return make_response(created_section_template_id)

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@section_template_blueprint.route('/', methods=['GET', 'HEAD'])
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.view')
@section_template_blueprint.parse_collection_parameters(view='native')
@insert_request_user
def get_all_section_templates(params: CollectionParameters, request_user: UserModel):
    """
    Returns all locations based on the params

    Args:
        params (CollectionParameters): params for locations request
        request_user (UserModel): User requesting the data

    Returns:
        (Response): All locations considering the params
    """
    try:
        iteration_result: IterationResult[CmdbSectionTemplate] = manager.iterate(
                                                                filter=params.filter,
                                                                limit=params.limit,
                                                                skip=params.skip,
                                                                sort=params.sort,
                                                                order=params.order,
                                                                user=request_user,
                                                                permission=AccessControlPermission.READ
                                                            )

        location_list: List[dict] = [location_.__dict__ for location_ in iteration_result.results]

        api_response = GetMultiResponse(location_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        CmdbSectionTemplate.MODEL,
                                        request.method == 'HEAD')

    except ManagerIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)

    return api_response.make_response()


@section_template_blueprint.route('/<int:public_id>', methods=['GET'])
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.view')
@insert_request_user
def get_section_template(public_id: int, request_user: UserModel):
    """
    Returns the selected section template for the given public_id
    
    Args:
        public_id (int): public_id of section template
        request_user (UserModel): User which is requesting the data
    """
    try:
        section_template_instance = section_template_manager.get_section_template(public_id, user=request_user,
                                                    permission=AccessControlPermission.READ)
    except (SectionTemplateManagerGetError, ManagerGetError) as err:
        return abort(404, err.message)
    except AccessDeniedError as err:
        return abort(403, err.message)

    if not section_template_instance:
        section_template_instance = []

    return make_response(section_template_instance)


@section_template_blueprint.route('/<int:public_id>/count', methods=['GET'])
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.view')
@insert_request_user
def get_global_section_template_count(public_id: int, request_user: UserModel):
    """Retrives the count of types and objects using this global template"""
    try:
        instance: CmdbSectionTemplate = section_template_manager.get_section_template(
                                                                                    public_id,
                                                                                    request_user,
                                                                                    AccessControlPermission.READ
                                                                                  )

        counts: dict = section_template_manager.get_global_template_usage_count(instance.name, instance.is_global)

    except (SectionTemplateManagerGetError, ManagerGetError) as err:
        return abort(404, err.message)

    except AccessDeniedError as err:
        return abort(403, err.message)

    return make_response(counts)

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@section_template_blueprint.route('/', methods=['PUT', 'PATCH'])
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.edit')
@section_template_blueprint.parse_location_parameters()
@insert_request_user
def update_section_template(params: dict, request_user: UserModel):
    """
    Updates a section template

    Args:
        params (dict): section template parameters
        request_user (UserModel): User requesting the update

    Returns:
        _type_: _description_
    """
    params['is_global'] = params['is_global'] in ('true', 'True')
    params['predefined'] = params['predefined'] in ('true', 'True')
    params['fields'] = json.loads(params['fields'])
    params['public_id'] = int(params['public_id'])
    params['type'] = 'section'

    failed: ResponseFailedMessage = []

    try:
        # get the current state
        current_template: CmdbSectionTemplate = section_template_manager.get_section_template(params['public_id'])

        result = section_template_manager._update(CmdbSectionTemplate.COLLECTION, params['public_id'], params)

        # Apply changes to all types and objects using the template
        section_template_manager.handle_section_template_changes(params, current_template)

    except (SectionTemplateManagerGetError, ManagerGetError, ObjectManagerUpdateError) as error:
        failed.append(ResponseFailedMessage(error_message=error.message, status=404,
                                                public_id=params['public_id'], obj=params).to_dict())


    api_response = UpdateSingleResponse(result, failed, request.url, CmdbSectionTemplate.MODEL)

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@section_template_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.delete')
@insert_request_user
def delete_section_template(public_id: int, request_user: UserModel):
    """TODO: document"""
    try:
        template_instance: CmdbSectionTemplate = section_template_manager.get_section_template(public_id)

        if template_instance.predefined:
            LOGGER.error("Trying to delete a predefined template")
            return abort(404)

        if template_instance.is_global:
            section_template_manager.cleanup_global_section_templates(template_instance.name)

        ack = section_template_manager.delete_section_template(public_id=public_id,
                                               user=request_user,
                                               permission=AccessControlPermission.DELETE)
    except SectionTemplateManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    except SectionTemplateManagerDeleteError as err:
        LOGGER.error(err)
        return abort(405)
    except AccessDeniedError as err:
        LOGGER.error(err)
        return abort(403, err.message)
    except CMDBError:
        return abort(500)

    return make_response(ack)
