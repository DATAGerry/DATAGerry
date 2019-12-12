# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from abc import abstractclassmethod
from datetime import datetime
from enum import Enum

from cmdb.exportd.exportd_job.exportd_job_base import JobManagementBase

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


class LogAction(Enum):
    CREATE = 0
    EDIT = 1
    EXECUTE = 2
    DELETE = 3


class ExportdMetaLog(JobManagementBase):
    COLLECTION = 'exportd.logs'
    REQUIRED_INIT_KEYS = [
        'log_type',
        'log_time',
        'action',
    ]

    def __init__(self, log_type, log_time: datetime, action: LogAction, **kwargs):
        self.log_type = log_type
        self.log_time: datetime = log_time
        self.action: LogAction = action
        super(ExportdMetaLog, self).__init__(**kwargs)


class ExportdJobLog(ExportdMetaLog):
    UNKNOWN_USER_STRING = 'Unknown'
    REQUIRED_INIT_KEYS = [
                             'job_id',
                             'version',
                             'user_id'
                         ] + ExportdMetaLog.REQUIRED_INIT_KEYS

    def __init__(self, job_id: int, state: bool, user_id: int, user_name: str = None, event: str = None, message=None, **kwargs):
        self.job_id = job_id
        self.state = state
        self.user_id = user_id
        self.user_name = user_name or self.UNKNOWN_USER_STRING
        self.event = event
        self.message = message
        super(ExportdJobLog, self).__init__(**kwargs)


class ExportdLog:
    REGISTERED_LOG_TYPE = {}
    DEFAULT_LOG_TYPE = ExportdJobLog

    @abstractclassmethod
    def register_log_type(cls, log_name, log_class):
        cls.REGISTERED_LOG_TYPE[log_name] = log_class

    def __new__(cls, *args, **kwargs):
        try:
            _log_class = cls.REGISTERED_LOG_TYPE[kwargs['log_type']]
        except (KeyError, ValueError):
            _log_class = cls.DEFAULT_LOG_TYPE
        return _log_class(*args, **kwargs)


