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

from cmdb.manager.exportd_job_manager import ExportdJobManager
from cmdb.manager.exportd_log_manager import ExportdLogManager
from cmdb.manager.cmdb_object_manager import CmdbObjectManager

from cmdb.event_management.event import Event
from cmdb.exportd.exportd_job.exportd_job import ExportdJob
from cmdb.exportd.exportd_header.exportd_header import ExportdHeader
from cmdb.utils.helpers import load_class
from cmdb.manager.exportd_log_manager import LogAction, ExportdJobLog
from cmdb.framework.cmdb_render import RenderList
from cmdb.templates.template_data import ObjectTemplateData
from cmdb.templates.template_engine import TemplateEngine
from cmdb.framework.cmdb_render import RenderResult

from cmdb.errors.manager.exportd_log_manager import ExportdLogManagerInsertError
from cmdb.errors.manager.exportd_job_manager import ExportJobConfigError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              ExportdManagerBase - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class ExportdManagerBase(ExportdJobManager):
    """TODO: document"""

    def __init__(self, job: ExportdJob,
                 object_manager: CmdbObjectManager,
                 log_manager: ExportdLogManager,
                 event: Event):
        self.job = job
        self.event = event
        self.variables = self.__get_exportvars()
        self.destinations = self.__get__destinations()
        self.object_manager = object_manager
        self.log_manager = log_manager
        self.sources = self.__get_sources()

        super().__init__(object_manager.dbm)


    def __get_exportvars(self):
        exportvars = {}

        for variable in self.job.get_variables():
            exportvars.update(
                {variable["name"]: ExportVariable(variable["name"], variable["default"], variable["templates"])})

        return exportvars


    def __get_sources(self):
        sources = []
        sources.append(ExportSource(self.job, object_manager=self.object_manager, event=self.event))

        return sources


    def __get__destinations(self):
        destinations = []
        destination_params = {}

        for destination in self.job.get_destinations():
            for param in destination["parameter"]:
                destination_params.update({param["name"]: param["value"]})

            export_destination = ExportDestination(
                f"cmdb.exportd.externals.external_systems.{destination['className']}",
                destination_params,
                self.variables,
                self.event
            )
            destinations.append(export_destination)

        return destinations


    def execute(self, user_id: int, user_name: str, log_flag: bool = True) -> ExportdHeader:
        """TODO. document"""
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
                template_data = ObjectTemplateData(self.object_manager, cmdb_object).get_template_data()
                external_system.add_object(cmdb_object, template_data)
            exportd_header = external_system.finish_export()

            if log_flag:
                try:
                    log_params = {
                        'job_id': self.job.get_public_id(),
                        'state': True,
                        'user_id': user_id,
                        'user_name': user_name,
                        'event': self.event.get_type(),
                        'message': external_system.msg_string,
                    }
                    self.log_manager.insert_log(action=LogAction.EXECUTE, log_type=ExportdJobLog.__name__, **log_params)
                except ExportdLogManagerInsertError as err:
                    #TODO: ERROR-FIX
                    LOGGER.error(err)

        return exportd_header


class ExportVariable:
    """TODO: document"""
    def __init__(self, name, value_tpl_default, value_tpl_types: dict = None):
        self.__name = name
        self.__value_tpl_default = value_tpl_default
        self.__value_tpl_types = value_tpl_types or {}


    def get_value(self, cmdb_object, template_data):
        """TODO: document"""
        # get value template
        value_template = self.__value_tpl_default
        object_type_id = cmdb_object.type_information['type_id']

        for templ in self.__value_tpl_types:
            if templ['type'] != '' and object_type_id == int(templ['type']):
                value_template = templ['template']

        # render template
        template_engine = TemplateEngine()
        try:
            output = template_engine.render_template_string(value_template, template_data)
            if output == 'None':
                output = ''
        except Exception as ex:
            LOGGER.warning(ex)
            output = ''

        return output


class ExportSource:
    """TODO: document"""
    def __init__(self, job: ExportdJob, object_manager: CmdbObjectManager, event: Event):
        self.__job = job
        self.event = event
        self.__obm = object_manager
        self.__objects = self.__fetch_objects()


    def get_objects(self):
        """TODO: document"""
        return self.__objects


    def __fetch_objects(self):
        """TODO: document"""
        query = []
        result = []
        condition = []
        subset: bool = self.__job.scheduling['event'].get('subset', False)

        if subset and self.event.get_param('event') in ['delete']:
            deleted = RenderResult()
            deleted.object_information['object_id'] = self.event.get_param('id')
            deleted.type_information['type_id'] = self.event.get_param('type_id')
            result.append(deleted)

        else:
            if subset and self.event.get_param('event') in ['insert', 'update']:
                condition.append({'public_id': self.event.get_param('id')})

            for source in self.__job.get_sources():
                temp = []
                for con in source["condition"]:
                    operator = con["operator"]
                    value = con["value"]

                    regex = {"$ne": con["value"]} if operator == "!=" else {"$regex": value, "$options": "si"}
                    regex = True if value in ['True', 'true'] else False if value in ['False', 'false'] else regex

                    temp.append({'fields': {"$elemMatch": {"name": con["name"], "value": regex}}})
                    temp.append({'type_id': source["type_id"]})
                    temp.append({'active': {'$eq': True}})
                    query.append({"$and": [*condition, *temp]})

                if not source["condition"]:
                    query.append({'type_id': source["type_id"], 'active': {'$eq': True}})

            current_objects = self.__obm.get_objects_by(sort="public_id", **{'$or': query})
            result = (RenderList(current_objects, None, database_manager=self.__obm.dbm,
                                 object_manager=self.__obm).render_result_list())

        return result


class ExportDestination:
    """TODO: document"""
    def __init__(self, class_external_system, destination_parms, export_vars, event=None):
        self.__destination_parms = destination_parms
        self.__export_vars = export_vars
        external_system_class = load_class(class_external_system)
        self.__external_system = external_system_class(self.__destination_parms, self.__export_vars, event)


    def get_external_system(self):
        """TODO: document"""
        return self.__external_system


class ExternalSystem:
    """TODO: document"""
    parameters = {}
    variables = {}

    def __init__(self, destination_parms, export_vars, event: Event = None):
        # Set default if value is empty
        for key, val in destination_parms.items():
            if not bool(str(val).strip()):
                destination_parms[key] = [item['default'] for item in self.parameters if item['name'] == key][0]

        for item in self.parameters:
            if not destination_parms.get(item['name']):
                destination_parms.update({item['name']: item['default']})

        self.event = event
        self._destination_parms = destination_parms
        self._export_vars = export_vars
        self.msg_string = ""


    def prepare_export(self):
        """TODO: document"""


    def add_object(self, cmdb_object, template_data):
        """TODO: document"""


    def finish_export(self) -> ExportdHeader:
        """TODO: document"""


    def error(self, err: str):
        """TODO: document"""
        raise ExportJobConfigError(err)


    def set_msg(self, msg):
        """TODO: document"""
        self.msg_string = msg
