import os
import re

from cmdb.utils.system_reader import SystemReader


class SystemEnvironmentReader(SystemReader):
    """
    Settings reader loads settings from environment variables
    """

    def __init__(self):
        # get all environment variables and store them in config dict
        self.__config = {}
        pattern = re.compile("DATAGERRY_(.*)_(.*)")
        for key in os.environ.keys():
            match = pattern.fullmatch(key)
            if match:
                section = match.group(1)
                name = match.group(2)
                value = os.environ[key]
                # save value in config dict
                if section not in self.__config:
                    self.__config[section] = {}
                self.__config[section][name] = value
        super(SystemEnvironmentReader, self).__init__()

    def get_value(self, name, section):
        return self.__config[section][name]

    def get_sections(self):
        return self.__config.keys()

    def get_all_values_from_section(self, section):
        return self.__config[section]

    def setup(self):
        raise NotImplementedError