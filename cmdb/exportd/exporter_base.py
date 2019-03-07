import jinja2
import cmdb.object_framework
from cmdb.utils.error import CMDBError
from cmdb.utils.helpers import load_class

class ExportJob:

    def __init__(self):
        self.__sources = []
        self.__destinations = []
        self.__exportvars = {}
        # ToDo: read data from configuration
        # setup export variables
        exportvar_objectid = ExportVariable("objectid", "{{id}}")
        exportvar_dummy1 = ExportVariable("dummy1", "{{fields.first_name}} {{fields.last_name}}")
        exportvar_dummy2 = ExportVariable("dummy2", "{{fields.last_name}} {{id}}")
        self.__exportvars = {
            "objectid": exportvar_objectid,
            "dummy1": exportvar_dummy1,
            "dummy2": exportvar_dummy2
        }
        # setup sources
        self.__sources.append(ExportSource())
        # setup destinations
        destination_parms = {
            "ip": "192.168.0.123",
            "user": "admin",
            "password": "admin"
        }
        export_destination = ExportDestination(
            "cmdb.exportd.exporter_base.ExternalSystemDummy", 
            destination_parms, 
            self.__exportvars
        )
        self.__destinations.append(export_destination)

    def execute(self):
        # get cmdb objects from all sources
        cmdb_objects = set()
        for source in self.__sources:
            cmdb_objects.update(source.get_objects())

        # for every destination: do export
        for destination in self.__destinations:
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
        # get object manager
        om = cmdb.object_framework.get_object_manager()

        # get value template
        value_template = self.__value_tpl_default
        object_type_id = cmdb_object.get_type_id()
        if object_type_id in self.__value_tpl_types:
            value_template = self.__value_tpl_types[object_type_id]

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

    def __init__(self):
        self.__objects = []
        object_manager = cmdb.object_framework.get_object_manager()
        # ToDo: filter objects
        self.__objects = object_manager.get_all_objects()

    def get_objects(self):
        return self.__objects


class ExportDestination:

    def __init__(self, class_external_system, destination_parms, export_vars):
        self.__destination_parms = destination_parms
        self.__export_vars = export_vars
        external_system_class = load_class(class_external_system)
        self.__external_system = external_system_class(self.__destination_parms, self.__export_vars)

    def get_external_system(self):
        return self.__external_system


class ExternalSystem:

    def __init__(self, destination_parms, export_vars):
        self._destination_parms = destination_parms
        self._export_vars = export_vars

    def prepare_export(self):
        pass

    def add_object(self, cmdb_object):
        pass

    def finish_export(self):
        pass


class ExternalSystemDummy(ExternalSystem):

    def __init__(self, destination_parms, export_vars):
        super(ExternalSystemDummy, self).__init__(destination_parms, export_vars)
        # init destination vars
        self.__ip = self._destination_parms.get("ip", None)
        self.__user = self._destination_parms.get("user", None)
        self.__password = self._destination_parms.get("password", None)
        if not (self.__ip and self.__user and self.__password):
            raise ExportJobConfigException()
        # init export vars
        self.__objectid = self._export_vars.get("objectid", ExportVariable("objectid", ""))
        self.__dummy1 = self._export_vars.get("dummy1", ExportVariable("dummy1", ""))
        self.__dummy2 = self._export_vars.get("dummy2", ExportVariable("dummy2", ""))
        self.__dummy3 = self._export_vars.get("dummy3", ExportVariable("dummy3", ""))
        self.__dummy4 = self._export_vars.get("dummy4", ExportVariable("dummy4", ""))

    def prepare_export(self):
        print("prepare export")
        print("destination parms: ip={} user={} password={}".format(self.__ip, self.__user, self.__password))

    def add_object(self, cmdb_object):
        # print values of export variables
        object_id = self.__objectid.get_value(cmdb_object)
        dummy1 = self.__dummy1.get_value(cmdb_object)
        dummy2 = self.__dummy2.get_value(cmdb_object)
        dummy3 = self.__dummy3.get_value(cmdb_object)
        dummy4 = self.__dummy4.get_value(cmdb_object)
        print("object {}".format(object_id))
        print("dummy1: {}; dummy2: {}; dummy3: {}; dummy4: {}".format(dummy1, dummy2, dummy3, dummy4))
        print("")


    def finish_export(self):
        print("finish export")


class ExportJobConfigException(CMDBError):
    def __init__(self):
        super().__init__()
        self.message = 'missing parameters for ExportDestination'
