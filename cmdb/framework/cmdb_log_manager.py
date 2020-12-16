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
from datetime import datetime
from cmdb.security.acl.errors import AccessDeniedError
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.framework import CmdbLog, CmdbMetaLog, CmdbObjectLog, CmdbObject
from cmdb.framework.managers.type_manager import TypeManager, TypeModel
from cmdb.framework.cmdb_base import CmdbManagerBase
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerInsertError, ObjectManagerUpdateError, \
    ObjectManagerDeleteError
from cmdb.framework.cmdb_log import CMDBError, LOGGER, LogAction


class CmdbLogManager(CmdbManagerBase):

    def __init__(self, database_manager=None):
        self._type_manager = TypeManager(database_manager)
        super(CmdbLogManager, self).__init__(database_manager)

    def search(self):
        pass

    # CRUD functions
    def get_log(self, public_id: int, group_id: int):
        try:
            log = CmdbLog(**self._get(
                collection=CmdbMetaLog.COLLECTION,
                public_id=public_id
            ))

            type_id = CmdbObject(**self._get(
                collection=CmdbObject.COLLECTION,
                public_id=log.object_id
            )).type_id

            acl = self._type_manager.get(type_id).acl

            if acl and acl.activated:
                if group_id not in acl.groups.includes.keys():
                    raise AccessDeniedError('Request user is not authorized!')

                if 'READ' not in acl.groups.includes[group_id]:
                    raise AccessDeniedError('Request user is not authorized!')

            return log
        except AccessDeniedError:
            raise
        except (CMDBError, Exception) as err:
            LOGGER.error(err)
            raise LogManagerGetError(err)

    def get_logs_by(self, requirements=[]):
        ack = []
        try:
            logs = self._aggregate(collection=CmdbMetaLog.COLLECTION, pipeline=requirements)
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
            LOGGER.error(err)
            raise LogManagerInsertError(err)
        return ack

    def update_log(self, data) -> int:
        raise NotImplementedError

    def delete_log(self, public_id):
        try:
            ack = self._delete(CmdbMetaLog.COLLECTION, public_id)
        except CMDBError as err:
            LOGGER.error(err)
            raise LogManagerDeleteError(err)
        return ack

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
