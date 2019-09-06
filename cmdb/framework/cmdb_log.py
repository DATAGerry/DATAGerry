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

from cmdb.data_storage import get_pre_init_database
from cmdb.framework.cmdb_base import CmdbManagerBase
from cmdb.framework.cmdb_dao import CmdbDAO
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerInsertError, ObjectManagerUpdateError, \
    ObjectManagerDeleteError

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


class LogAction(Enum):
    CREATE = 0
    EDIT = 1
    ACTIVE_CHANGE = 2


class CmdbMetaLog(CmdbDAO):
    COLLECTION = 'framework.logs'
    REQUIRED_INIT_KEYS = [
        'log_type',
        'log_time',
        'action',
    ]

    def __init__(self, log_type, log_time: datetime, action: LogAction, **kwargs):
        self.log_type = log_type
        self.log_time: datetime = log_time
        self.action: LogAction = action
        super(CmdbMetaLog, self).__init__(**kwargs)


class CmdbObjectLog(CmdbMetaLog):
    UNKNOWN_USER_STRING = 'Unknown'
    REQUIRED_INIT_KEYS = [
                             'object_id',
                             'version',
                             'user_id'
                         ] + CmdbMetaLog.REQUIRED_INIT_KEYS

    def __init__(self, object_id: int, version, user_id: int, user_name: str = None, changes: list = None,
                 comment: str = None, render_state=None, **kwargs):
        self.object_id = object_id
        self.version = version
        self.user_id = user_id
        self.user_name = user_name or self.UNKNOWN_USER_STRING
        self.comment = comment
        self.changes = changes or []
        self.render_state = render_state
        super(CmdbObjectLog, self).__init__(**kwargs)


class CmdbLog:
    REGISTERED_LOG_TYPE = {}
    DEFAULT_LOG_TYPE = CmdbObjectLog

    @abstractclassmethod
    def register_log_type(cls, log_name, log_class):
        cls.REGISTERED_LOG_TYPE[log_name] = log_class

    def __new__(cls, *args, **kwargs):
        try:
            _log_class = cls.REGISTERED_LOG_TYPE[kwargs['log_type']]
        except (KeyError, ValueError):
            _log_class = cls.DEFAULT_LOG_TYPE
        return _log_class(*args, **kwargs)


class CmdbLogManager(CmdbManagerBase):
    def __init__(self, database_manager=None):
        super(CmdbLogManager, self).__init__(database_manager)

    # CRUD functions
    def get_log(self, public_id: int):
        try:
            return CmdbLog(**self._get(
                collection=CmdbMetaLog.COLLECTION,
                public_id=public_id
            ))
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise LogManagerGetError(err)

    def get_logs_by(self, sort='public_id', **requirements):
        ack = []
        try:
            logs = self._get_all(collection=CmdbMetaLog.COLLECTION, sort=sort, **requirements)
            for log in logs:
                ack.append(CmdbLog(**log))
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise LogManagerGetError(err)
        return ack

    def insert_log(self, action: LogAction, log_type: str, **kwargs) -> int:
        # Get possible public id
        log_init = {}
        available_id = self.dbm.get_next_public_id(collection=CmdbMetaLog.COLLECTION)
        log_init['public_id'] = available_id

        # set static values
        log_init['action'] = action.value
        log_init['action_name'] = action.name
        log_init['log_type'] = log_type
        log_init['log_time'] = datetime.utcnow()

        log_data = {**log_init, **kwargs}

        try:
            new_log = CmdbLog(**log_data)
            ack = self._insert(CmdbMetaLog.COLLECTION, new_log.to_database())
        except (CMDBError, Exception) as err:
            LOGGER.error(err.message)
            raise LogManagerInsertError(err)
        return ack

    def update_log(self, data) -> int:
        raise NotImplementedError

    def delete_log(self, data) -> int:
        raise NotImplementedError

    # FIND functions
    def get_object_logs(self, public_id: int) -> list:
        """
        Get corresponding logs to object.
        Args:
            public_id: Public id for logs

        Returns:
            List of object-logs
        """
        object_list: list = []
        try:
            query = {'filter': {'log_type': str(CmdbObjectLog.__name__), 'object_id': public_id}}
            founded_logs = self.dbm.find_all(CmdbMetaLog.COLLECTION, **query)
            for _ in founded_logs:
                object_list.append(CmdbLog(**_))
        except (CMDBError, Exception) as err:
            LOGGER.error(f'Error in get_object_logs: {err}')
            raise LogManagerGetError(err)
        return object_list


class LogManagerGetError(ObjectManagerGetError):

    def __init__(self, err):
        super(LogManagerGetError, self).__init__(err)


class LogManagerInsertError(ObjectManagerInsertError):

    def __init__(self, err):
        super(LogManagerInsertError, self).__init__(err)


class LogManagerUpdateError(ObjectManagerUpdateError):

    def __init__(self, err):
        super(LogManagerUpdateError, self).__init__(err)


class LogManagerDeleteError(ObjectManagerDeleteError):

    def __init__(self, err):
        super(LogManagerDeleteError, self).__init__(err)


log_manager = CmdbLogManager(
    database_manager=get_pre_init_database()
)
