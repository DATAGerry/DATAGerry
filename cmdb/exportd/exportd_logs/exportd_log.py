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
from cmdb.framework import CmdbLog
from cmdb.framework.utils import Model

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
    MODEL: Model = 'ExportdLog'

    def __init__(self, public_id, log_type, log_time: datetime, action: LogAction, action_name: str):
        self.log_type = log_type
        self.log_time: datetime = log_time
        self.action: LogAction = action
        self.action_name = action_name
        super(ExportdMetaLog, self).__init__(public_id=public_id)


class ExportdJobLog(ExportdMetaLog):
    UNKNOWN_USER_STRING = 'Unknown'

    def __init__(self, public_id: int, log_type, log_time: datetime, action: LogAction, action_name: str,
                 job_id: int, state: bool = None, user_id: int = None, user_name: str = None, event: str = None,
                 message=None):
        self.job_id = job_id
        self.state = state
        self.user_id = user_id
        self.user_name = user_name or self.UNKNOWN_USER_STRING
        self.event = event
        self.message = message
        super(ExportdJobLog, self).__init__(public_id=public_id, log_type=log_type, log_time=log_time, action=action,
                                            action_name=action_name)

    @classmethod
    def from_data(cls, data: dict, *args, **kwargs) -> "ExportdJobLog":
        """Create a instance of ExportdJobLog from database values"""
        return cls(
            public_id=data.get('public_id'),
            job_id=data.get('job_id'),
            state=data.get('state', None),
            user_name=data.get('user_name', None),
            user_id=data.get('user_id', None),
            event=data.get('event', None),
            log_time=data.get('log_time', None),
            log_type=data.get('log_type', None),
            message=data.get('message', None),
            action=data.get('action', None),
            action_name=data.get('action_name', None)
        )

    @classmethod
    def to_json(cls, instance: "ExportdJobLog") -> dict:
        """Convert a ExportdJobLog instance to json conform data"""
        return {
            'public_id': instance.public_id,
            'job_id': instance.job_id,
            'state': instance.state,
            'user_name': instance.user_name,
            'user_id': instance.user_id,
            'event': instance.event,
            'log_time': instance.log_time,
            'log_type': instance.log_type,
            'message': instance.message,
            'action': instance.action,
            'action_name': instance.action_name,
        }


class ExportdLog(CmdbLog):
    REGISTERED_LOG_TYPE = {}
    DEFAULT_LOG_TYPE = ExportdJobLog
