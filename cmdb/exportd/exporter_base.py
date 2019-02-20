import cmdb.object_framework

class ExportJob:

    def __init__(self):
        self.__sources = []
        self.__destinations = []
        # ToDo: make configurable
        self.__sources.append(ExportSource())
        self.__destinations.append(ExportDestination())

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



class ExportSource:

    def __init__(self):
        self.__objects = []
        object_manager = cmdb.object_framework.get_object_manager()
        # ToDo: filter objects
        self.__objects = object_manager.get_all_objects()

    def get_objects(self):
        return self.__objects


class ExportDestination:

    def __init__(self):
        # ToDo: make configurable
        self.__external_system = ExternalSystemDummy()

    def get_external_system(self):
        return self.__external_system


class ExternalSystem:

    def __init__(self):
        pass

    def prepare_export(self):
        pass

    def add_object(self, cmdb_object):
        pass

    def finish_export(self):
        pass

class ExternalSystemDummy(ExternalSystem):

    def prepare_export(self):
        print("prepare export")

    def add_object(self, cmdb_object):
        print("add object")

    def finish_export(self):
        print("finish export")
