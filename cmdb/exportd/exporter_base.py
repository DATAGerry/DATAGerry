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
import logging

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.exportd.exportd_job.exportd_job_manager import ExportdJobManagement
from cmdb.exportd.exportd_logs.exportd_log_manager import ExportdLogManager
from cmdb.exportd.exportd_job.exportd_job import ExportdJob
from cmdb.exportd.exportd_header.exportd_header import ExportdHeader
from cmdb.utils.error import CMDBError
from cmdb.utils.helpers import load_class
from cmdb.utils.system_reader import SystemConfigReader
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.exportd.exportd_logs.exportd_log_manager import LogManagerInsertError, LogAction, ExportdJobLog
from cmdb.framework.cmdb_render import CmdbRender, RenderList

LOGGER = logging.getLogger(__name__)


class ExportdManagerBase(ExportdJobManagement):

    def __init__(self, job: ExportdJob):
        self.job = job
        self.exportvars = self.__get_exportvars()
        self.destinations = self.__get__destinations()

        scr = SystemConfigReader()
        database_manager = DatabaseManagerMongo(
            **scr.get_all_values_from_section('Database')
        )
        self.__object_manager = CmdbObjectManager(
            database_manager=database_manager
        )
        self.log_manager = ExportdLogManager(
            database_manager=database_manager)

        self.sources = self.__get_sources()
        super(ExportdManagerBase, self).__init__(database_manager)

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

    def execute(self, event, user_id: int, user_name: str, log_flag: bool = True) -> ExportdHeader:
        # get cmdb objects from all sources
        cmdb_objects = set()
        exportd_header = ExportdHeader()
        for source in self.sources:
            cmdb_objects.update(source.get_objects())

        # for every destination: do export
        for destination in self.destinations:
            external_system = destination.get_external_system()
            external_system.prepare_export()

            for cmdb_object in cmdb_objects:
                # setup objectdata for use in ExportVariable templates
                template_data = self.__get_objectdata(cmdb_object, 3)
                external_system.add_object(cmdb_object, template_data)
            exportd_header = external_system.finish_export()

            if log_flag:
                try:
                    log_params = {
                        'job_id': self.job.get_public_id(),
                        'state': True,
                        'user_id': user_id,
                        'user_name': user_name,
                        'event': event.get_type(),
                        'message': external_system.msg_string,
                    }
                    self.log_manager.insert_log(action=LogAction.EXECUTE, log_type=ExportdJobLog.__name__, **log_params)
                except LogManagerInsertError as err:
                    LOGGER.error(err)
        return exportd_header

    def __get_objectdata(self, cmdb_object, iteration):
        data = {}
        data["id"] = cmdb_object.object_information['object_id']
        data["fields"] = {}
        for field in cmdb_object.fields:
            try:
                field_name = field["name"]
                if field["type"] == "ref" and field["value"] and iteration > 0:
                    # resolve type
                    iteration = iteration - 1
                    current_object = self.__object_manager.get_object(field["value"])
                    type_instance = self.__object_manager.get_type(current_object.get_type_id())
                    cmdb_render_object = CmdbRender(object_instance=current_object, type_instance=type_instance,
                                                    render_user=None, user_manager=None)
                    data["fields"][field_name] = self.__get_objectdata(cmdb_render_object.result(), iteration)
                else:
                    data["fields"][field_name] = field["value"]
            except Exception as e:
                pass
        return data


class ExportVariable:

    def __init__(self, name, value_tpl_default, value_tpl_types={}):
        self.__name = name
        self.__value_tpl_default = value_tpl_default
        self.__value_tpl_types = value_tpl_types

    def get_value(self, cmdb_object, template_data):
        # get value template
        value_template = self.__value_tpl_default
        object_type_id = cmdb_object.type_information['type_id']

        for templ in self.__value_tpl_types:
            if templ['type'] != '' and object_type_id == int(templ['type']):
                value_template = templ['template']

        # render template
        template = jinja2.Template(value_template)
        try:
            output = template.render(template_data)
            if output == 'None':
                output = ''
        except Exception as ex:
            LOGGER.warning(ex)
            output = ''
        return output


class ExportSource:

    def __init__(self, job: ExportdJob, object_manager: CmdbObjectManager = None):
        self.__job = job
        self.__obm = object_manager
        self.__objects = self.__fetch_objects()

    def get_objects(self):
        return self.__objects

    def __fetch_objects(self):
        query = []
        for source in self.__job.get_sources():
            condition = []
            for con in source["condition"]:
                if con["operator"] == "!=":
                    operator = {"$ne": con["value"]}
                else:
                    operator = con["value"]

                if operator in ['True', 'true']:
                    operator = True
                elif operator in ['False', 'false']:
                    operator = False
                else:
                    operator = operator

                condition.append({'fields': {"$elemMatch": {"name": con["name"], "value": operator}}})
                condition.append({'type_id': source["type_id"]})
                condition.append({'active': {'$eq': True}})
                query.append({"$and": condition})

            if not source["condition"]:
                query.append({'type_id': source["type_id"], 'active': {'$eq': True}})

        current_objects = self.__obm.get_objects_by(sort="public_id", **{'$or': query})
        result = (RenderList(current_objects, None).render_result_list())
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
    parameters = {}
    variables = {}

    def __init__(self, destination_parms, export_vars):
        # Set default if value is empty
        for key, val in destination_parms.items():
            if not bool(str(val).strip()):
                destination_parms[key] = [item['default'] for item in self.parameters if item['name'] == key][0]

        for item in self.parameters:
            if not destination_parms.get(item['name']):
                destination_parms.update({item['name']: item['default']})

        self._destination_parms = destination_parms
        self._export_vars = export_vars
        self.msg_string = ""

    def prepare_export(self):
        pass

    def add_object(self, cmdb_object, template_data):
        pass

    def finish_export(self) -> ExportdHeader:
        pass

    def error(self, msg):
        raise ExportJobConfigException(msg)

    def set_msg(self, msg):
        self.msg_string = msg


class ExportJobConfigException(CMDBError):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
