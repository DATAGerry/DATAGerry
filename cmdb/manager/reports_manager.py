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
This module contains the implementation of the ReportsManager
"""
import logging

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.manager.base_manager import BaseManager

from cmdb.models.reports_model.cmdb_report import CmdbReport
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import ManagerInsertError, ManagerGetError, ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                            ReportCategoriesManager - CLASS                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class ReportsManager(BaseManager):
    """
    The ReportsManager handles the interaction between the Reports-API and the database
    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, database:str = None):
        """
        Set the database connection and the queue for sending events

        Args:
            dbm (MongoDatabaseManager): Database connection
        """
        if database:
            dbm.connector.set_database(database)

        super().__init__(CmdbReport.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_report(self, data: dict) -> int:
        """
        Inserts a single CmdbReport in the database

        Args:
            data (dict): Data of the new CmdbReport

        Returns:
            int: public_id of the newly created CmdbReport
        """
        try:
            new_report_category = CmdbReport(**data)
        except Exception as err:
            #TODO: ERROR-FIX
            raise ManagerInsertError(err) from err

        try:
            ack = self.insert(new_report_category.__dict__)
            #TODO: ERROR-FIX
        except Exception as err:
            raise ManagerInsertError(err) from err

        return ack

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_report(self, public_id: int) -> CmdbReport:
        """
        Retrives a CmdbReport from the database with the given public_id

        Args:
            public_id (int): public_id of the CmdbReport which should be retrieved
        Raises:
            ManagerGetError: Raised if the CmdbReport could not be retrieved
        Returns:
            CmdbReport: The requested CmdbReport if it exists, else None
        """
        try:
            requested_report_category = self.get_one(public_id)
        except Exception as err:
            #TODO: ERROR-FIX
            raise ManagerGetError(f"Report with ID: {public_id}! 'GET' Error: {err}") from err

        if requested_report_category:
            requested_report_category = CmdbReport.from_data(requested_report_category)

            return requested_report_category

        #TODO: ERROR-FIX
        raise ManagerGetError(f'Report with ID: {public_id} not found!')


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[CmdbReport]:
        """
        Performs an aggregation on the database

        Args:
            builder_params (BuilderParameters): Contains input to identify the target of action
            user (UserModel, optional): User requesting this action
        Raises:
            ManagerIterationError: Raised when something goes wrong during the aggregate part
            ManagerIterationError: Raised when something goes wrong during the building of the IterationResult
        Returns:
            IterationResult[CmdbReport]: Result which matches the Builderparameters
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)
        except ManagerGetError as err:
            #TODO: ERROR-FIX
            raise ManagerIterationError(err) from err

        try:
            iteration_result: IterationResult[CmdbReport] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbReport)
        except Exception as err:
            #TODO: ERROR-FIX
            raise ManagerIterationError(err) from err

        return iteration_result
