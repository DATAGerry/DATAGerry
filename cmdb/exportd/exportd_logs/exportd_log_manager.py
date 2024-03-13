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
from datetime import datetime, timezone
from cmdb.framework.cmdb_base import CmdbManagerBase

from cmdb.exportd.exportd_logs.exportd_log import ExportdLog, ExportdMetaLog, ExportdJobLog
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerInsertError, \
    ObjectManagerDeleteError
from cmdb.exportd.exportd_logs.exportd_log import LOGGER, LogAction
from cmdb.utils.error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class ExportdLogManager(CmdbManagerBase):
    """TODO: document"""
    def __init__(self, database_manager=None):
        super().__init__(database_manager)


    # CRUD functions
    def get_all_logs(self):
        """TODO: document"""
        log_list = []
        for found_log in self.dbm.find_all(collection=ExportdMetaLog.COLLECTION):
            try:
                log_list.append(ExportdLog(**found_log))
            except CMDBError as err:
                LOGGER.error(err)
                raise LogManagerGetError(err) from err
        return log_list


    def get_log(self, public_id: int):
        """TODO: document"""
        try:
            return ExportdJobLog.from_data(self._get(
                collection=ExportdMetaLog.COLLECTION,
                public_id=public_id
            ))
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise LogManagerGetError(err) from err


    def get_logs_by(self, sort='public_id', **requirements):
        """TODO: document"""
        ack = []
        try:
            logs = self._get_many(collection=ExportdMetaLog.COLLECTION, sort=sort, **requirements)
            for log in logs:
                ack.append(ExportdJobLog.from_data(log))
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise LogManagerGetError(err) from err
        return ack


    def insert_log(self, action: LogAction, log_type: str, **kwargs) -> int:
        """TODO: document"""
        # Get possible public id
        log_init = {}
        available_id = self.dbm.get_next_public_id(collection=ExportdMetaLog.COLLECTION)
        log_init['public_id'] = available_id

        # set static values
        log_init['action'] = action.value
        log_init['action_name'] = action.name
        log_init['log_type'] = log_type
        log_init['log_time'] = datetime.now(timezone.utc)

        log_data = {**log_init, **kwargs}

        try:
            new_log = ExportdJobLog.from_data(log_data)
            ack = self._insert(ExportdMetaLog.COLLECTION, ExportdJobLog.to_json(new_log))
        except Exception as err:
            raise LogManagerInsertError(err) from err
        return ack


    def update_log(self, data) -> int:
        """TODO: document"""
        raise NotImplementedError


    def delete_log(self, public_id):
        """TODO: document"""
        try:
            ack = self._delete(ExportdMetaLog.COLLECTION, public_id)
        except CMDBError as err:
            LOGGER.error(err)
            raise LogManagerDeleteError(err) from err
        return ack


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
            founded_logs = self.dbm.find_all(ExportdMetaLog.COLLECTION, **query)
            for _ in founded_logs:
                job_list.append(ExportdLog.from_data(_))
        except (CMDBError, Exception) as err:
            LOGGER.error('Error in get_exportd_job_logs: %s',err)
            raise LogManagerGetError(err) from err
        return job_list

# --------------------------------------------------- ERROR CLASSES -------------------------------------------------- #

class LogManagerGetError(ObjectManagerGetError):
    """TODO: document"""
    def __init__(self, err):
        self.err = err
        super().__init__(err)


class LogManagerInsertError(ObjectManagerInsertError):
    """TODO: document"""
    def __init__(self, err):
        self.err = err
        super().__init__(err)


class LogManagerDeleteError(ObjectManagerDeleteError):
    """TODO: document"""
    def __init__(self, err):
        self.err = err
        super().__init__(err)
