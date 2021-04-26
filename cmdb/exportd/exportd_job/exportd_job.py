# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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

from enum import Enum
from cmdb.framework.cmdb_dao import CmdbDAO, NoPublicIDError
from cmdb.framework.utils import Collection, Model
from cmdb.exportd.exportd_job.exportd_job_base import JobManagementBase


class ExecuteState(Enum):
    SUCCESSFUL = 0
    INFO = 1
    WARNING = 2
    FAILED = 3
    RUNNING = 4


class ExportdJobType(Enum):
    PUSH = 0
    PULL = 1


class ExportdJob(JobManagementBase):
    """
    Exportd Job
    """
    COLLECTION: Collection = 'exportd.jobs'
    MODEL: Model = 'ExportDJob'

    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, name, label=None, description=None, active=None, author_id=None,
                 last_execute_date=None, sources=None, destination=None,
                 variables=None, scheduling=None, exportd_type=None, state=None, **kwargs):
        """
        Args:
            name: name of this job
            active: is job executable
            sources: consists of multiple objects of a specific object type and a specific status
            destination: is an external system, where you want to push the yourcmdb objects
            variables: has a name and gets its value out of fields of the objects
            **kwargs: optional params
        """
        self.name = name
        self.label = label
        self.description = description
        self.active = active or False
        self.author_id = author_id
        self.last_execute_date = last_execute_date
        self.sources = sources
        self.destination = destination
        self.variables = variables
        self.scheduling = scheduling
        self.state = state or 0
        self.exportd_type = exportd_type or ExportdJobType.PUSH.name
        super(ExportdJob, self).__init__(**kwargs)

    @classmethod
    def from_data(cls, data: dict) -> "ExportdJob":
        """Create a instance of ExportdJob from database values"""
        return cls(
            public_id=data.get('public_id'),
            name=data.get('name'),
            label=data.get('label', None),
            description=data.get('description', None),
            active=data.get('active', None),
            author_id=data.get('author_id', None),
            last_execute_date=data.get('last_execute_date', None),
            sources=data.get('sources', None),
            destination=data.get('destination', None),
            variables=data.get('variables', None),
            scheduling=data.get('scheduling', None),
            state=data.get('state', None),
            exportd_type=data.get('exportd_type', None),
        )

    @classmethod
    def to_json(cls, instance: "ExportdJob") -> dict:
        """Convert a job instance to json conform data"""
        return {
            'public_id': instance.public_id,
            'name': instance.name,
            'label': instance.label,
            'description': instance.description,
            'active': instance.active,
            'author_id': instance.author_id,
            'last_execute_date': instance.last_execute_date,
            'sources': instance.sources,
            'destination': instance.destination,
            'variables': instance.variables,
            'scheduling': instance.scheduling,
            'state': instance.state,
            'exportd_type': instance.exportd_type,
        }

    def get_public_id(self) -> int:
        """
        get the public id of current element

        Note:
            Since the models object is not initializable
            the child class object will inherit this function
            SHOULD NOT BE OVERWRITTEN!

        Returns:
            int: public id

        Raises:
            NoPublicIDError: if `public_id` is zero or not set

        """
        if self.public_id == 0 or self.public_id is None:
            raise NoPublicIDError()
        return self.public_id

    def get_name(self) -> str:
        """
        Get the name of the job
        Returns:
            str: display name
        """
        if self.name is None:
            return ""
        else:
            return self.name

    def get_label(self) -> str:
        """
        Get the label of the job
        Returns:
            str: display label
        """
        if self.label is None:
            return ""
        else:
            return self.label

    def get_active(self) -> bool:
        """
        Get active state of the job
        Returns:
            bool: is job executable
        """
        if self.active is None:
            return ""
        else:
            return self.active

    def get_sources(self):
        """
        Get all sources of the job
        Returns:
            list: all sources
        """
        return self.sources

    def get_destinations(self):
        """
        Get all destinations of the job
        Returns:
            list: all destinations
        """
        return self.destination

    def get_variables(self):
        """
        Get all variables of the job
        Returns:
            list: all variables
        """
        return self.variables

    def get_scheduling(self) -> dict:
        """
        Get scheduling of the job
        Returns:
            dict: Execution settings
        """
        return self.scheduling

    def get_state(self):
        """
        Get state of executation of the job
        Returns:
            str:
        """
        return self.state

    def get_exportd_typ(self):
        """
        Get type of executation of the job
        Returns:
            str:
        """
        return self.exportd_type

    def get_author_id(self):
        return self.author_id
