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

import jinja2

from cmdb.data_storage.database_manager import DatabaseManagerMongo, MongoConnector
from cmdb.exportd.exportd_job.exportd_job_manager import ExportdJobManagement
from cmdb.exportd.exportd_job.exportd_job import ExportdJob
from cmdb.utils.error import CMDBError
from cmdb.utils.helpers import load_class
from cmdb.utils.system_reader import SystemConfigReader
from cmdb.framework.cmdb_object_manager import CmdbObjectManager


class ExportJob(ExportdJobManagement):

    def __init__(self, job: ExportdJob):
        self.job = job
        self.exportvars = self.__get_exportvars()
        self.destinations = self.__get__destinations()
        scr = SystemConfigReader()
        database_manager = DatabaseManagerMongo(
            connector=MongoConnector(
                **scr.get_all_values_from_section('Database')
            )
        )
        self.__object_manager = CmdbObjectManager(
            database_manager=database_manager
        )
        self.sources = self.__get_sources()
        super(ExportJob, self).__init__(database_manager)

    def __get_exportvars(self):
        exportvars = {}
        for variable in self.job.get_variables():
            exportvars.update(
                {variable["name"]: ExportVariable(variable["name"], variable["default"], variable["templates"])})
        return exportvars

    def __get_sources(self):
        sources = []
        sources.append(ExportSource(self.job, object_manager=self.__object_manager))
        return sources

    def __get__destinations(self):
        destinations = []
        destination_params = {}
        for destination in self.job.get_destinations():
            for param in destination["parameter"]:
                destination_params.update({param["name"]: param["value"]})

            export_destination = ExportDestination(
                "cmdb.exportd.externals.external_systems.{}".format(destination["className"]),
                destination_params,
                self.exportvars
            )
            destinations.append(export_destination)

        return destinations

    def execute(self):
        # get cmdb objects from all sources
        cmdb_objects = set()
        for source in self.sources:
            cmdb_objects.update(source.get_objects())

        # for every destination: do export
        for destination in self.destinations:
            external_system = destination.get_external_system()
            external_system.prepare_export()
            for cmdb_object in cmdb_objects:
                external_system.add_object(cmdb_object)
            external_system.finish_export()


class ExportVariable:

    def __init__(self, name, value_tpl_default, value_tpl_types={}):
        self.__name = name
        self.__value_tpl_default = value_tpl_default
        self.__value_tpl_types = value_tpl_types

    def get_value(self, cmdb_object):
        # get value template
        value_template = self.__value_tpl_default
        object_type_id = cmdb_object.get_type_id()

        for templ in self.__value_tpl_types:
            if templ['type'] != '' and object_type_id == int(templ['type']):
                value_template = templ['template']

        # objectdata for use in ExportVariable templates
        objectdata = {}
        objectdata["id"] = cmdb_object.get_public_id()
        # objectdata: object fields
        # ToDo: use rendered fields
        objectdata["fields"] = {}
        fields = cmdb_object.get_all_fields()
        for field in fields:
            field_name = field["name"]
            field_value = field["value"]
            objectdata["fields"][field_name] = field_value
        # ToDo: dereference objectrefs

        # render template
        template = jinja2.Template(value_template)
        output = template.render(objectdata)
        return output


class ExportSource:

    def __init__(self, job: ExportdJob, object_manager: CmdbObjectManager = None):
        self.__job = job
        self.__obm = object_manager
        self.__objects = self.__fetch_objects()

    def get_objects(self):
        return self.__objects

    def __fetch_objects(self):
        condition = []
        for source in self.__job.get_sources():
            for con in source["condition"]:
                if con["operator"] == "!=":
                    operator = {"$ne": con["value"]}
                else:
                    operator = con["value"]
                condition.append({"$and": [{"fields.name": con["name"]}, {"fields.value": operator}]})
        query = {"$or": condition}
        result = self.__obm.get_objects_by(sort="public_id", **query)

        return result


class ExportDestination:

    def __init__(self, class_external_system, destination_parms, export_vars):
        self.__destination_parms = destination_parms
        self.__export_vars = export_vars
        external_system_class = load_class(class_external_system)
        self.__external_system = external_system_class(self.__destination_parms, self.__export_vars)

    def get_external_system(self):
        return self.__external_system


class ExternalSystem:
    parameters = []

    def __init__(self, destination_parms, export_vars):
        self._destination_parms = destination_parms
        self._export_vars = export_vars

    def prepare_export(self):
        pass

    def add_object(self, cmdb_object):
        pass

    def finish_export(self):
        pass


class ExportJobConfigException(CMDBError):
    def __init__(self):
        super().__init__()
        self.message = 'missing parameters for ExportDestination'
