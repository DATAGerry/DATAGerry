# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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

import logging
from datetime import datetime
from enum import Enum

from cmdb.framework.cmdb_dao import CmdbDAO
from cmdb.framework.utils import Collection, Model

LOGGER = logging.getLogger(__name__)


class LogAction(Enum):
    CREATE = 0
    EDIT = 1
    ACTIVE_CHANGE = 2
    DELETE = 3


class CmdbMetaLog(CmdbDAO):
    """
    CmdbLog
    """
    COLLECTION: Collection = 'framework.logs'
    MODEL: Model = 'CmdbLog'

    def __init__(self, public_id, log_type, log_time: datetime, action: LogAction, action_name: str):
        self.log_type = log_type
        self.log_time: datetime = log_time
        self.action: LogAction = action
        self.action_name = action_name
        super(CmdbMetaLog, self).__init__(public_id=public_id)


class CmdbObjectLog(CmdbMetaLog):
    DEFAULT_VERSION: str = '1.0.0'
    SCHEMA: dict = {
        'object_id': {
            'type': 'integer'
        },
        'public_id': {
            'type': 'integer'
        },
        'version': {
            'type': 'integer',
            'default': DEFAULT_VERSION
        },
        'user_id': {
            'type': 'integer'
        },
        'user_name': {
            'type': 'string',
            'required': True,
            'regex': r'(\w+)-*(\w)([\w-]*)'  # kebab case validation,
        },
        'render_state': {
            'type': 'string'
        },
        'log_type': {
            'type': 'string',
            'required': True,
        },
        'log_time': {
            'type': 'datetime',
            'required': True,
        },
        'changes': {
            'type': 'list',
            'empty': True,
            'default': []
        },
        'comment': {
            'type': 'string'
        },
        'action': {
            'type': 'integer',
            'required': True,
        },
        'action_name': {
            'type': 'string',
            'required': True
        },

    }

    UNKNOWN_USER_STRING = 'Unknown'

    def __init__(self, public_id: int, log_type, log_time: datetime, action: LogAction, action_name: str,
                 object_id: int, version, user_id: int, user_name: str = None, changes: list = None,
                 comment: str = None, render_state=None):
        self.object_id = object_id
        self.version = version
        self.user_id = user_id
        self.user_name = user_name or self.UNKNOWN_USER_STRING
        self.comment = comment
        self.changes = changes or []
        self.render_state = render_state
        super(CmdbObjectLog, self).__init__(public_id=public_id, log_type=log_type, log_time=log_time, action=action,
                                            action_name=action_name)

    @classmethod
    def from_data(cls, data: dict, *args, **kwargs) -> "CmdbObjectLog":
        """Create a instance of TypeModel from database values"""
        return cls(
            public_id=data.get('public_id'),
            object_id=data.get('object_id'),
            version=data.get('version', None),
            user_name=data.get('user_name'),
            user_id=data.get('user_id'),
            render_state=data.get('render_state'),
            log_time=data.get('log_time', None),
            log_type=data.get('log_type', None),
            changes=data.get('changes', None),
            comment=data.get('comment', None),
            action=data.get('action', None),
            action_name=data.get('action_name', None),
        )

    @classmethod
    def to_json(cls, instance: "CmdbObjectLog") -> dict:
        """Convert a type instance to json conform data"""
        return {
            'public_id': instance.public_id,
            'log_time': instance.log_time,
            'log_type': instance.log_type,
            'action': instance.action,
            'object_id': instance.object_id,
            'version': instance.version,
            'user_name': instance.user_name,
            'user_id': instance.user_id,
            'render_state': instance.render_state,
            'changes': instance.changes,
            'comment': instance.comment,
            'action_name': instance.action_name
        }


class CmdbLog:
    REGISTERED_LOG_TYPE = {}
    DEFAULT_LOG_TYPE = CmdbObjectLog

    @classmethod
    def __get_log_class(cls, *args, **kwargs):
        try:
            log_class = cls.REGISTERED_LOG_TYPE[kwargs['log_type']]
        except (KeyError, ValueError):
            log_class = cls.DEFAULT_LOG_TYPE
        return log_class

    @classmethod
    def register_log_type(cls, log_name, log_class):
        cls.REGISTERED_LOG_TYPE[log_name] = log_class

    @classmethod
    def from_data(cls, data: dict, *args, **kwargs):
        return cls.__get_log_class(**data).from_data(data, *args, **kwargs)

    def __new__(cls, *args, **kwargs):
        return cls.__get_log_class(*args, **kwargs)(*args, **kwargs)
