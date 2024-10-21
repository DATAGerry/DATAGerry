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

from cmdb.manager.base_manager import BaseManager
from cmdb.database.database_manager_mongo import DatabaseManagerMongo

from cmdb.exportd.exportd_logs.exportd_log import ExportdLog, ExportdMetaLog, ExportdJobLog
from cmdb.exportd.exportd_logs.exportd_log import LogAction
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.framework.results import IterationResult

from cmdb.errors.manager.exportd_log_manager import ExportdLogManagerDeleteError,\
                                                    ExportdLogManagerInsertError,\
                                                    ExportdLogManagerGetError
from cmdb.errors.manager import ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              ExportdLogsManager - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class ExportdLogsManager(BaseManager):
    """TODO: document"""
    def __init__(self, dbm: DatabaseManagerMongo, database: str = None):
        if database:
            dbm.connector.set_database(database)

        super().__init__(ExportdMetaLog.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_log(self, action: LogAction, log_type: str, **kwargs) -> int:
        """TODO: document"""
        # Get possible public id
        log_init = {}

        log_init['public_id'] = self.get_new_exportd_log_public_id()
        log_init['action'] = action.value
        log_init['action_name'] = action.name
        log_init['log_type'] = log_type
        log_init['log_time'] = datetime.now(timezone.utc)

        log_data = {**log_init, **kwargs}

        try:
            new_log = ExportdJobLog.from_data(log_data)
            ack = self.insert(ExportdJobLog.to_json(new_log))
        except Exception as err:
            #TODO: ERROR-FIX
            raise ExportdLogManagerInsertError(str(err)) from err

        return ack

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_all_logs(self):
        """TODO: document"""
        log_list = []

        for found_log in self.find_all():
            try:
                log_list.append(ExportdLog(**found_log))
            except Exception as err:
                #TODO: ERROR-FIX
                LOGGER.error(err)
                raise ExportdLogManagerGetError(str(err)) from err

        return log_list


    def get_logs_by(self, sort='public_id', **requirements):
        """TODO: document"""
        ack = []

        try:
            logs = self.get_many(sort=sort, **requirements)
            for log in logs:
                ack.append(ExportdJobLog.from_data(log))
        except Exception as err:
            #TODO: ERROR-FIX
            LOGGER.error(err)
            raise ExportdLogManagerGetError(str(err)) from err

        return ack


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[ExportdJobLog]:
        """
        TODO: document
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            iteration_result: IterationResult[ExportdJobLog] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(ExportdJobLog)
        #TODO: ERROR-FIX
        except Exception as err:
            #TODO: ERROR-FIX
            raise ManagerIterationError(err) from err

        return iteration_result


    # FIND functions
    def get_exportd_job_logs(self, public_id: int) -> list:
        """
        Get corresponding logs to object.
        Args:
            public_id: Public id for logs

        Returns:
            List of exportd-job-logs
        """
        job_list: list = []

        try:
            query = {'filter': {'log_type': str(ExportdJobLog.__name__), 'job_id': public_id}}
            found_logs = self.find_all(**query)
            for found_log in found_logs:
                job_list.append(ExportdLog.from_data(found_log))
        except Exception as err:
            LOGGER.error('Error in get_exportd_job_logs: %s',str(err))
            raise ExportdLogManagerGetError(str(err)) from err

        return job_list


    def get_new_exportd_log_public_id(self) -> int:
        """
        Gets the next couter for the public_id from database and increases it

        Returns:
            int: The next public_id for ExportdLog
        """
        return self.get_next_public_id()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_log(self, public_id: int):
        """TODO: document"""
        try:
            ack = self.delete({'public_id': public_id})
        except Exception as err:
            #TODO: ERROR-FIX
            raise ExportdLogManagerDeleteError(str(err)) from err

        return ack
