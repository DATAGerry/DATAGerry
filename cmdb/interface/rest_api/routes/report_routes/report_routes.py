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
from ast import literal_eval
from flask import abort, request

from cmdb.database.mongo_query_builder import MongoDBQueryBuilder
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.reports_manager import ReportsManager
from cmdb.manager.objects_manager import ObjectsManager

from cmdb.models.user_model.user import UserModel
from cmdb.models.reports_model.cmdb_report import CmdbReport
from cmdb.models.reports_model.mds_mode_enum import MdsMode
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import DefaultResponse, GetMultiResponse, UpdateSingleResponse
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import (
    ManagerInsertError,
    ManagerGetError,
    ManagerIterationError,
    ManagerUpdateError,
    ManagerDeleteError,
)
from cmdb.errors.database import NoDocumentFound
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

reports_blueprint = APIBlueprint('reports', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@reports_blueprint.route('/', methods=['POST'])
@reports_blueprint.parse_request_parameters()
@insert_request_user
def create_report(params: dict, request_user: UserModel):
    """
    Creates a CmdbReport in the database

    Args:
        params (dict): CmdbReport parameters
    Returns:
        int: public_id of the created CmdbReport
    """
    reports_manager: ReportsManager = ManagerProvider.get_manager(ManagerType.REPORTS_MANAGER, request_user)

    try:
        params['public_id'] = reports_manager.get_next_public_id()
        params['report_category_id'] = int(params['report_category_id'])
        params['type_id'] = int(params['type_id'])
        params['predefined'] = params['predefined'] in ["True", "true"]
        params['mds_mode'] = params['mds_mode'] if params['mds_mode'] in [MdsMode.ROWS,
                                                                          MdsMode.COLUMNS] else MdsMode.ROWS
        params['conditions'] = literal_eval(params['conditions'])
        params['selected_fields'] = literal_eval(params['selected_fields'])
        params['report_query'] = {'data': str(MongoDBQueryBuilder(params['conditions'], params['type_id']).build())}

        new_report_id = reports_manager.insert_report(params)
    except ManagerInsertError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[create_report] ManagerInsertError: %s", err.message)
        return abort(400, "Could not create the report!")
    except Exception as err:
        LOGGER.debug("[create_report] Exception: %s, Type: %s", err, type(err))

    api_response = DefaultResponse(new_report_id)

    return api_response.make_response()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@reports_blueprint.route('/<int:public_id>', methods=['GET'])
@insert_request_user
def get_report(public_id: int, request_user: UserModel):
    """
    Retrieves the CmdbReport with the given public_id
    
    Args:
        public_id (int): public_id of CmdbReport which should be retrieved
        request_user (UserModel): User which is requesting the CmdbReport
    """
    reports_manager: ReportsManager = ManagerProvider.get_manager(ManagerType.REPORTS_MANAGER, request_user)

    try:
        requested_report = reports_manager.get_report(public_id)
    except ManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_report] ManagerGetError: %s", err.message)
        return abort(400, f"Could not retrieve Report with ID: {public_id}!")

    api_response = DefaultResponse(requested_report)

    return api_response.make_response()


@reports_blueprint.route('/', methods=['GET', 'HEAD'])
@reports_blueprint.parse_collection_parameters()
@insert_request_user
def get_reports(params: CollectionParameters, request_user: UserModel):
    """
    Returns all CmdbReports based on the params

    Args:
        params (CollectionParameters): Parameters to identify documents in database
    Returns:
        (GetMultiResponse): All CmdbReports considering the params
    """
    reports_manager: ReportsManager = ManagerProvider.get_manager(ManagerType.REPORTS_MANAGER, request_user)

    try:
        builder_params: BuilderParameters = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbReport] = reports_manager.iterate(builder_params)
        report_list: list[dict] = [report_.__dict__ for report_ in iteration_result.results]

        api_response = GetMultiResponse(report_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        request.method == 'HEAD')
    except ManagerIterationError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_reports] ManagerIterationError: %s", err.message)
        return abort(400, "Could not retrieve CmdbReports!")

    return api_response.make_response()


@reports_blueprint.route('/<int:public_id>/run', methods=['GET'])
@insert_request_user
def run_report_query(public_id: int, request_user: UserModel):
    """
    Returns the result of the query of the report

    Args:
        params (int): public_id of the CmdbReport
    Returns:
        (DefaultResponse): Dict of the query result
    """
    try:
        reports_manager: ReportsManager = ManagerProvider.get_manager(ManagerType.REPORTS_MANAGER, request_user)
        objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

        requested_report = reports_manager.get_report(public_id)

        query_str = requested_report.report_query['data']
        report_query = literal_eval(query_str)

        builder_params = BuilderParameters(criteria=report_query)

        result = objects_manager.iterate(builder_params).results

        api_response = DefaultResponse(result)
    except Exception as err:
        LOGGER.debug("[run_report_query] Exception: %s, Type: %s", err, type(err))
        return abort (400, "Could not run the requested report!")

    return api_response.make_response()

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@reports_blueprint.route('/<int:public_id>', methods=['PUT','PATCH'])
@reports_blueprint.parse_request_parameters()
@insert_request_user
def update_report(params: dict, request_user: UserModel):
    """
    Updates a CmdbReport

    Args:
        params (dict): updated CmdbReport parameters
    Returns:
        UpdateSingleResponse: Response with UpdateResult
    """
    reports_manager: ReportsManager = ManagerProvider.get_manager(ManagerType.REPORTS_MANAGER, request_user)

    try:
        params['public_id'] = int(params['public_id'])
        params['report_category_id'] = int(params['report_category_id'])
        params['type_id'] = int(params['type_id'])
        params['predefined'] = params['predefined'] in ["True", "true"]
        params['conditions'] = literal_eval(params['conditions'])
        params['selected_fields'] = literal_eval(params['selected_fields'])
        params['mds_mode'] = params['mds_mode'] if params['mds_mode'] in [MdsMode.ROWS,
                                                                          MdsMode.COLUMNS] else MdsMode.ROWS

        current_report = reports_manager.get_report(params['public_id'])

        if current_report:
            params['report_query'] = {'data': str(MongoDBQueryBuilder(params['conditions'], params['type_id']).build())}
            #TODO: REFACTOR-FIX
            reports_manager.update({'public_id': params['public_id']}, params)
            current_report = reports_manager.get_report(params['public_id'])
        else:
            raise NoDocumentFound(reports_manager.collection)

    except ManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[update_report] ManagerGetError: %s", err.message)
        return abort(400, f"Could not retrieve CmdbReport with ID: {params['public_id']}!")
    except ManagerUpdateError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[update_report] ManagerUpdateError: %s", err.message)
        return abort(400, f"Could not update CmdbReport with ID: {params['public_id']}!")
    except NoDocumentFound:
        return abort(404, "Report not found!")
    except Exception as err:
        LOGGER.debug("[update_report] Exception: %s, Type: %s", err, type(err))
        return abort(400, "Something went wrong during updating the report!")

    api_response = UpdateSingleResponse(current_report.__dict__)

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@reports_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@insert_request_user
def delete_report(public_id: int, request_user: UserModel):
    """
    Deletes the CmdbReport with the given public_id
    
    Args:
        public_id (int): public_id of CmdbReport which should be retrieved
        request_user (UserModel): User which is requesting the CmdbReport
    """
    reports_manager: ReportsManager = ManagerProvider.get_manager(ManagerType.REPORTS_MANAGER, request_user)

    try:
        report_instance: CmdbReport = reports_manager.get_report(public_id)

        if not report_instance:
            return abort(400, f"Could not retrieve Report with ID: {public_id}!")

        #TODO: REFACTOR-FIX
        ack: bool = reports_manager.delete({'public_id':public_id})
    except ManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[delete_report] ManagerGetError: %s", err.message)
        return abort(400, f"Could not retrieve Report with ID: {public_id}!")
    except ManagerDeleteError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[delete_report] ManagerDeleteError: %s", err)
        return abort(400, f"Could not delete Report with ID: {public_id}!")

    api_response = DefaultResponse(ack)

    return api_response.make_response()
