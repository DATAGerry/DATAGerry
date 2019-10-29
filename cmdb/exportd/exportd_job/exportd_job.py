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

from cmdb.exportd.exportd_job.exportd_job_base import JobManagementBase


class ExportdJob(JobManagementBase):
    """
        Exportd Job
    """
    COLLECTION = 'exportd.jobs'
    REQUIRED_INIT_KEYS = [
        'name',
    ]

    def __init__(self, name, active, sources, destination, variables, **kwargs):
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
        self.active = active
        self.sources = sources
        self.destination = destination
        self.variables = variables
        super(ExportdJob, self).__init__(**kwargs)

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

    def get_active(self) -> bool:
        """
        Get active state of the job
        Returns:
            bool: is job executable
        """
        if self.name is None:
            return ""
        else:
            return self.name

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

