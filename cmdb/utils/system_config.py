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
import os
from typing import Any

import configparser
from cmdb.utils.cast import auto_cast
from cmdb.utils.system_env_reader import SystemEnvironmentReader
from cmdb.utils.system_reader import SystemReader

from cmdb.errors.system_config import ConfigFileSetError,\
                                      ConfigFileNotFound,\
                                      ConfigNotLoaded,\
                                      SectionError,\
                                      KeySectionError
# -------------------------------------------------------------------------------------------------------------------- #

class SystemConfigReader:
    """
    System reader for local config file
    Options from config file can be overwritten by environment vars
    """
    DEFAULT_CONFIG_LOCATION = os.path.join(os.path.dirname(__file__), '../../etc/')
    DEFAULT_CONFIG_NAME = 'cmdb.conf'
    RUNNING_CONFIG_LOCATION = DEFAULT_CONFIG_LOCATION
    RUNNING_CONFIG_NAME = DEFAULT_CONFIG_NAME
    CONFIG_LOADED = True
    CONFIG_NOT_LOADED = False
    instance = None


    def __new__(cls, config_name=None, config_location=None):
        if not SystemConfigReader.instance:
            SystemConfigReader.instance = SystemConfigReader.SystemConfReader(config_name, config_location)
        return SystemConfigReader.instance


    def __getattr__(self, name):
        return getattr(self.instance, name)


    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

    #CLASS-FIX
    class SystemConfReader(SystemReader):
        """TODO: document"""
        DEFAULT_CONFIG_FILE_LESS = False
        CONFIG_LOADED = True
        CONFIG_NOT_LOADED = False


        def __init__(self, config_name, config_location):
            """
            init the system config reader
            Args:
                config_name: name of config file with extension
                config_location: directory of config file
            """
            self.config = configparser.ConfigParser()
            if config_name is None:
                self.config_file_less = True
                self.config_status = SystemConfigReader.CONFIG_LOADED
            else:
                self.config_file_less = self.DEFAULT_CONFIG_FILE_LESS
                self.config_status = SystemConfigReader.CONFIG_NOT_LOADED
                self.config_name = config_name
                self.config_location = config_location
                self.config_file = self.config_location + self.config_name
                self.config_status = self.setup()
            if self.config_status == SystemConfigReader.CONFIG_NOT_LOADED:
                raise ConfigFileNotFound(self.config_name)
            # load environment variables
            self.__envvars = SystemEnvironmentReader()


        def add_section(self, section):
            """
            Add a section to the config parser
            Notes:
                Only allowed if no config file was loaded
            Args:
                section: name of the section
            """
            if not self.config_file_less:
                raise ConfigFileSetError(self.config_file)
            self.config.add_section(section)


        def set(self, section, option, value):
            """
            Set a value inside of a sections
            Notes:
                Only allowed if no config file was loaded
            Args:
                section: name of section
                option: name of the option
                value: value of the option
            """
            if not self.config_file_less:
                raise ConfigFileSetError(self.config_file)
            self.config.set(section, option, value)


        def setup(self):
            """
            init configuration file
            Returns:
                loading status
            """
            try:
                self.read_config_file(self.config_file)
                return SystemConfigReader.CONFIG_LOADED
            except ConfigFileNotFound:
                return SystemConfigReader.CONFIG_NOT_LOADED


        def read_config_file(self, file):
            """
            helper function for file reading sets the path directly inside the config attribute
            Args:
                file: path to config file

            """
            if os.path.isfile(file):
                self.config.read(file)
            else:
                raise ConfigFileNotFound(self.config_name)


        def get_value(self, name: str, section: str, default: Any = None):
            """
            get a value from a given section
            Args:
                name: key of value
                section: section of the value
                default: default value
            Returns:
                value
            """
            # check if environment variable is set
            try:
                value = self.__envvars.get_value(name, section)
                return value
            except KeyError:
                pass

            # load option from config file
            if self.config_status == SystemConfigReader.CONFIG_LOADED:
                if self.config.has_section(section):
                    if name not in self.config[section]:
                        if default:
                            return default
                        raise KeyError(name)

                    return auto_cast(self.config[section][name])

                raise SectionError(section)

            raise ConfigNotLoaded(SystemConfigReader.RUNNING_CONFIG_NAME)


        def get_sections(self):
            """
            get all sections from config
            Returns:
                list of sections inside a config
            """
            if self.config_status == SystemConfigReader.CONFIG_LOADED:
                return self.config.sections()

            raise ConfigNotLoaded(SystemConfigReader.RUNNING_CONFIG_NAME)


        def get_all_values_from_section(self, section):
            """
            get all values from a section
            Args:
                section: section name

            Returns:
                key value dict of all elements inside section
            """
            # load env vars
            section_envvars = {}
            try:
                section_envvars = self.__envvars.get_all_values_from_section(section)
            except Exception:
                pass

            # get section from config
            section_conffile = {}
            if self.config_status == SystemConfigReader.CONFIG_LOADED:
                try:
                    if self.config.has_section(section):
                        section_conffile = dict(self.config.items(section))
                    else:
                        raise SectionError(section)
                except KeyError as err:
                    raise KeySectionError(section) from err
            else:
                raise ConfigNotLoaded(SystemConfigReader.RUNNING_CONFIG_NAME)

            # merge two the config dicts
            section_merged = section_conffile.copy()
            section_merged.update(section_envvars)
            return section_merged


        def status(self):
            """
            checks if config is loaded correctly
            Returns:
                True/False statement of loading status
            """
            if self.config_status:
                return self.CONFIG_LOADED
            return self.CONFIG_NOT_LOADED
