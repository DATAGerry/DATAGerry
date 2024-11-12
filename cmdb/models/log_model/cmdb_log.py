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

from cmdb.models.log_model.cmdb_object_log import CmdbObjectLog
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                    CmdbLog - CLASS                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
class CmdbLog:
    """TODO: document"""
    REGISTERED_LOG_TYPE = {}
    DEFAULT_LOG_TYPE = CmdbObjectLog

    def __new__(cls, *args, **kwargs):
        return cls.__get_log_class(*args, **kwargs)(*args, **kwargs)


    @classmethod
    def __get_log_class(cls, **kwargs):
        try:
            log_class = cls.REGISTERED_LOG_TYPE[kwargs['log_type']]
        except (KeyError, ValueError):
            log_class = cls.DEFAULT_LOG_TYPE
        return log_class


    @classmethod
    def register_log_type(cls, log_name, log_class):
        """TODO: document"""
        cls.REGISTERED_LOG_TYPE[log_name] = log_class


    @classmethod
    def from_data(cls, data: dict, *args, **kwargs):
        """TODO: document"""
        return cls.__get_log_class(**data).from_data(data, *args, **kwargs)


    @classmethod
    def to_json(cls, instance: "CmdbLog") -> dict:
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
