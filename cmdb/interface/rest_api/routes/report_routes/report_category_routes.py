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
TODO: document
"""
import logging
from flask import abort, request

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.manager.report_categories_manager import ReportCategoriesManager

from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.route_utils import insert_request_user
from cmdb.interface.rest_api.responses import DefaultResponse, GetMultiResponse, UpdateSingleResponse
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.models.user_model.user import UserModel
from cmdb.models.reports_model.cmdb_report_category import CmdbReportCategory
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import ManagerInsertError,\
                                ManagerIterationError,\
                                ManagerGetError,\
                                ManagerUpdateError,\
                                ManagerDeleteError,\
                                DisallowedActionError
from cmdb.errors.database import NoDocumentFound
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

report_categories_blueprint = APIBlueprint('report_categories', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@report_categories_blueprint.route('/', methods=['POST'])
@report_categories_blueprint.parse_request_parameters()
@insert_request_user
def create_report_category(params: dict, request_user: UserModel):
    """
    Creates a CmdbReportCategory in the database

    Args:
        params (dict): CmdbReportCategory parameters
    Returns:
        int: public_id of the created CmdbReportCategory
    """
    report_categories_manager: ReportCategoriesManager = ManagerProvider.get_manager(
                                                                            ManagerType.REPORT_CATEGORIES_MANAGER,
                                                                            request_user)

    try:
        params['public_id'] = report_categories_manager.get_next_public_id()
        # It is not possible to create a predefined CmdbReportCategory
        params['predefined'] = False

        new_report_category_id = report_categories_manager.insert_report_category(params)
    except ManagerInsertError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[create_report_category] ManagerInsertError: %s", err.message)
        return abort(400, "Could not create the report category!")

    api_response = DefaultResponse(new_report_category_id)

    return api_response.make_response()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@report_categories_blueprint.route('/<int:public_id>', methods=['GET'])
@insert_request_user
def get_report_category(public_id: int, request_user: UserModel):
    """
    Retrieves the CmdbReportCategory with the given public_id
    
    Args:
        public_id (int): public_id of CmdbReportCategory which should be retrieved
        request_user (UserModel): User which is requesting the CmdbReportCategory
    """
    report_categories_manager: ReportCategoriesManager = ManagerProvider.get_manager(
                                                                            ManagerType.REPORT_CATEGORIES_MANAGER,
                                                                            request_user)

    try:
        report_category = report_categories_manager.get_report_category(public_id)
    except ManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_report_category] ManagerGetError: %s", err.message)
        return abort(400, f"Could not retrieve CmdbReportCategory with ID: {public_id}!")


    api_response = DefaultResponse(report_category)

    return api_response.make_response()


@report_categories_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@report_categories_blueprint.parse_collection_parameters()
def get_report_categories(params: CollectionParameters, request_user: UserModel):
    """
    Returns all CmdbReportCategories based on the params

    Args:
        params (CollectionParameters): Parameters to identify documents in database
    Returns:
        (GetMultiResponse): All CmdbReportCategories considering the params
    """
    report_categories_manager: ReportCategoriesManager = ManagerProvider.get_manager(
                                                                            ManagerType.REPORT_CATEGORIES_MANAGER,
                                                                            request_user)

    try:
        builder_params: BuilderParameters = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbReportCategory] = report_categories_manager.iterate(builder_params)
        report_category_list: list[dict] = [report_category_.__dict__ for report_category_ in iteration_result.results]

        api_response = GetMultiResponse(report_category_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        request.method == 'HEAD')
    except ManagerIterationError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_report_categories] ManagerIterationError: %s", err.message)
        return abort(400, "Could not retrieve CmdbReportCategories!")

    return api_response.make_response()

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@report_categories_blueprint.route('/', methods=['PUT'])
@report_categories_blueprint.parse_request_parameters()
@insert_request_user
def update_report_category(params: dict, request_user: UserModel):
    """
    Updates a CmdbReportCategory

    Args:
        params (dict): updated CmdbReportCategory parameters
    Returns:
        UpdateSingleResponse: Response with UpdateResult
    """
    report_categories_manager: ReportCategoriesManager = ManagerProvider.get_manager(
                                                                            ManagerType.REPORT_CATEGORIES_MANAGER,
                                                                            request_user)

    try:
        current_category: CmdbReportCategory = report_categories_manager.get_report_category(params['public_id'])

        if current_category:
            #TODO: REFACTOR-FIX
            result = report_categories_manager.update({'public_id':params['public_id']}, params)
        else:
            raise NoDocumentFound(report_categories_manager.collection)

    except ManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[update_report_category] ManagerGetError: %s", err.message)
        return abort(400, f"Could not retrieve CmdbReportCategory with ID: {params['public_id']}!")
    except ManagerUpdateError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[update_report_category] ManagerUpdateError: %s", err.message)
        return abort(400, f"Could not update CmdbReportCategory with ID: {params['public_id']}!")
    except NoDocumentFound:
        return abort(404, "Report Category not found!")

    api_response = UpdateSingleResponse(result)

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@report_categories_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@insert_request_user
def delete_report_category(public_id: int, request_user: UserModel):
    """
    Deletes the CmdbReportCategory with the given public_id
    
    Args:
        public_id (int): public_id of CmdbReportCategory which should be retrieved
        request_user (UserModel): User which is requesting the CmdbReportCategory
    """
    report_categories_manager: ReportCategoriesManager = ManagerProvider.get_manager(
                                                                            ManagerType.REPORT_CATEGORIES_MANAGER,
                                                                            request_user)

    try:
        report_category_instance: CmdbReportCategory = report_categories_manager.get_report_category(public_id)

        if report_category_instance.predefined:
            LOGGER.debug("[delete_report_category] Error: Trying to delete a predefined CmdbReportCategory")
            raise DisallowedActionError(f"Trying to delete a predefined CmdbReportCategory with id: {public_id}")

        #TODO: REFACTOR-FIX
        ack: bool = report_categories_manager.delete({'public_id':public_id})
    except ManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[delete_report_category] ManagerGetError: %s", err.message)
        return abort(400, f"Could not retrieve ReportCategory with ID: {public_id}!")
    except DisallowedActionError:
        return abort(405, f"Unable to delete predefined CmdbReportCategory with ID: {public_id}!")
    except ManagerDeleteError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[delete_report_category] ManagerDeleteError: %s", err)
        return abort(400, f"Could not delete ReportCategory with ID: {public_id}!")

    api_response = DefaultResponse(ack)

    return api_response.make_response()
