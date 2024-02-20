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
Definition of all routes for CmdbSectionTemplates
"""
import json
import logging

from flask import request, current_app

from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.route_utils import make_response

from cmdb.manager.section_templates_manager import SectionTemplatesManager

from cmdb.interface.api_parameters import CollectionParameters
from cmdb.framework import CmdbSectionTemplate
from cmdb.framework.results import IterationResult
from cmdb.interface.response import GetMultiResponse, UpdateSingleResponse, ErrorBody
from cmdb.manager.query_builder.builder_parameters import BuilderParameters

from cmdb.errors.manager import ManagerInsertError,\
                                ManagerIterationError,\
                                ManagerGetError,\
                                ManagerUpdateError,\
                                ManagerDeleteError,\
                                DisallowedActionError
from cmdb.errors.database import NoDocumentFound
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

section_template_blueprint = APIBlueprint('section_templates', __name__)


template_manager = SectionTemplatesManager(current_app.database_manager, current_app.event_queue)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@section_template_blueprint.route('/', methods=['POST'])
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.add')
@section_template_blueprint.parse_location_parameters()
def create_section_template(params: dict):
    """
    Creates a CmdbSectionTemplate in the database

    Args:
        params (dict): CmdbSectionTemplate parameters
    Returns:
        int: public_id of the created CmdbSectionTemplate
    """
    try:
        params['public_id'] = template_manager.get_next_public_id()
        params['is_global'] = params['is_global'] in ('true', 'True')
        params['predefined'] = params['predefined'] in ('true', 'True')
        params['fields'] = json.loads(params['fields'])
        params['type'] = 'section'

        created_section_template_id = template_manager.insert_section_template(params)
    except ManagerInsertError as err:
        LOGGER.debug("Exception in section_template_create")
        return ErrorBody(400, str(err)).response()

    return make_response(created_section_template_id)

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@section_template_blueprint.route('/', methods=['GET', 'HEAD'])
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.view')
@section_template_blueprint.parse_collection_parameters(view='native')
def get_all_section_templates(params: CollectionParameters):
    """Returns all CmdbSectionTemplates based on the params

    Args:
        params (CollectionParameters): Parameters to identify documents in database
    Returns:
        (GetMultiResponse): All CmdbSectionTemplates considering the params
    """
    try:
        builder_params: BuilderParameters = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbSectionTemplate] = template_manager.iterate(builder_params)
        template_list: list[dict] = [template_.__dict__ for template_ in iteration_result.results]

        api_response = GetMultiResponse(template_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        CmdbSectionTemplate.MODEL,
                                        request.method == 'HEAD')
    except ManagerIterationError as err:
        LOGGER.debug("ManagerIterationError: %s", err)
        return ErrorBody(400, "Could not retrieve SectionTemplates!").response()

    return api_response.make_response()

# -------------------------------------------------------------------------------------------------------------------- #

@section_template_blueprint.route('/<int:public_id>', methods=['GET'])
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.view')
def get_section_template(public_id: int):
    """
    Retrieves the CmdbSectionTemplate with the given public_id
    
    Args:
        public_id (int): public_id of CmdbSectionTemplate which should be retrieved
        request_user (UserModel): User which is requesting the CmdbSectionTemplate
    """
    try:
        section_template_instance = template_manager.get_section_template(public_id)
    except ManagerGetError as err:
        LOGGER.debug("ManagerGetError: %s", err)
        return ErrorBody(400, f"Could not retrieve SectionTemplate with public_id: {public_id}!").response()

    if not section_template_instance:
        section_template_instance = []

    return make_response(section_template_instance)

# -------------------------------------------------------------------------------------------------------------------- #

@section_template_blueprint.route('/<int:public_id>/count', methods=['GET'])
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.view')
def get_global_section_template_count(public_id: int):
    """
    Retrives the count of types and objects using this global CmdbSectionTemplate

    Args:
        public_id (int): public_id of CmdbSectionTemplate which should be checked
    Returns:
        dict: Dict with counts of types and objects using this global CmdbSectionTemplate
    """
    try:
        instance: CmdbSectionTemplate = template_manager.get_section_template(public_id)

        counts: dict = template_manager.get_global_template_usage_count(instance.name, instance.is_global)

    except ManagerGetError as err:
        LOGGER.debug("ManagerGetError: %s", err)
        return ErrorBody(400, f"Could not retrieve SectionTemplate with public_id: {public_id}!").response()

    return make_response(counts)

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@section_template_blueprint.route('/', methods=['PUT', 'PATCH'])
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.edit')
@section_template_blueprint.parse_location_parameters()
def update_section_template(params: dict):
    """
    Updates a CmdbSectionTemplate

    Args:
        params (dict): new CmdbSectionTemplate parameters
    Returns:
        _type_: _description_
    """
    params['is_global'] = params['is_global'] in ('true', 'True')
    params['predefined'] = params['predefined'] in ('true', 'True')
    params['fields'] = json.loads(params['fields'])
    params['public_id'] = int(params['public_id'])
    params['type'] = 'section'

    try:
        current_template: CmdbSectionTemplate = template_manager.get_section_template(params['public_id'])

        if current_template:
            result = template_manager.update({'public_id':params['public_id']}, params)

            # Apply changes to all types and objects using the template
            template_manager.handle_section_template_changes(params, current_template)
        else:
            raise NoDocumentFound(template_manager.collection, params['public_id'])

    except ManagerGetError as err:
        LOGGER.debug("ManagerGetError: %s", err)
        return ErrorBody(400, f"Could not retrieve SectionTemplate with public_id: {params['public_id']}!").response()
    except ManagerUpdateError as err:
        LOGGER.debug("ManagerUpdateError: %s", err)
        return ErrorBody(400, f"Could not update SectionTemplate with public_id: {params['public_id']}!").response()
    except NoDocumentFound as err:
        return ErrorBody(404, str(err)).response()

    api_response = UpdateSingleResponse(result, None, request.url, CmdbSectionTemplate.MODEL)

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@section_template_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.delete')
def delete_section_template(public_id: int):
    """TODO: document"""
    try:
        template_instance: CmdbSectionTemplate = template_manager.get_section_template(public_id)

        if template_instance.predefined:
            LOGGER.debug("ERROR: Trying to delete a predefined CmdbSectionTemplate")
            raise DisallowedActionError(f"Trying to delete a predefined CmdbSectionTemplate with id: {public_id}")

        if template_instance.is_global:
            template_manager.cleanup_global_section_templates(template_instance.name)

        ack: bool = template_manager.delete({'public_id':public_id})

    except ManagerGetError as err:
        LOGGER.debug("ManagerGetError: %s", err)
        return ErrorBody(400, f"Could not retrieve SectionTemplate with public_id: {public_id}!").response()
    except DisallowedActionError as err:
        LOGGER.debug("DisallowedActionError: %s", err)
        return ErrorBody(405, str(err)).response()
    except ManagerDeleteError as err:
        LOGGER.debug("ManagerDeleteError: %s", err)
        return ErrorBody(400, f"Could not delete SectionTemplate with public_id: {public_id}!").response()

    return make_response(ack)
