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

"""
Collection of system readers which loads configuration files and settings
"""
import os
import re
from typing import Any, Union, List

from cmdb.data_storage.database_manager import DatabaseManagerMongo, NoDocumentFound
from cmdb.utils.cast import auto_cast
from cmdb.utils.error import CMDBError


class SystemReader:
    """
    Reader super class
    """

    def get_value(self, name: str, section: str, default: Any = None) -> Any:
        """
        get specific value from a section
        Args:
            name: key name of value
            section: section identifier
            default: if value not found return default
        Returns:
            value
        """
        raise NotImplementedError

    def get_sections(self) -> List[str]:
        """
        get all sections from config
        Returns:
            list of config names
        """
        raise NotImplementedError

    def get_all_values_from_section(self, section: str) -> dict:
        """
        get list of all values in section
        Args:
            section: section key
        Returns:
            key/value list of all values inside a section
        """
        raise NotImplementedError


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
            SystemConfigReader.instance = SystemConfigReader.__SystemConfigReader(config_name, config_location)
        return SystemConfigReader.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

    class __SystemConfigReader(SystemReader):

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
            import configparser
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

        def get_section(self, section):
            return self.config.sections(section)

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
                    else:
                        return auto_cast(self.config[section][name])
                else:
                    raise SectionError(section)
            else:
                raise ConfigNotLoaded(SystemConfigReader.RUNNING_CONFIG_NAME)

        def get_sections(self):
            """
            get all sections from config
            Returns:
                list of sections inside a config
            """
            if self.config_status == SystemConfigReader.CONFIG_LOADED:
                return self.config.sections()
            else:
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
            except:
                pass

            # get section from config
            section_conffile = {}
            if self.config_status == SystemConfigReader.CONFIG_LOADED:
                try:
                    if self.config.has_section(section):
                        section_conffile = dict(self.config.items(section))
                    else:
                        raise SectionError(section)
                except KeyError:
                    raise KeySectionError(section)
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

        def __repr__(self):
            """
            Helper function for debugging
            """

            from pprint import pprint
            for names in self.get_sections():
                pprint(names + ": {}".format(self.config.items(names)))


class SystemSettingsReader(SystemReader):
    """
    Settings reader loads settings from database
    """
    COLLECTION = 'settings.conf'

    def __init__(self, database_manager: DatabaseManagerMongo):
        """
        init system settings reader
        Args:
            database_manager: database manager
        """
        self.dbm: DatabaseManagerMongo = database_manager
        super(SystemSettingsReader, self).__init__()

    def get_value(self, name, section) -> Union[dict, list]:
        """
        get a value from a given section
        Args:
            name: key of value
            section: section of the value

        Returns:
            value
        """
        return self.dbm.find_one_by(
            collection=SystemSettingsReader.COLLECTION,
            filter={'_id': section}
        )[name]

    def get_section(self, section_name: str) -> dict:
        query_filter = {'_id': section_name}
        return self.dbm.find_one_by(collection=SystemSettingsReader.COLLECTION, filter=query_filter)

    def get_sections(self):
        """
        get all sections from config
        Returns:
            list of sections inside a config
        """
        return self.dbm.find_all(
            collection=SystemSettingsReader.COLLECTION,
            projection={'_id': 1}
        )

    def get_all_values_from_section(self, section, default = None) -> dict:
        """
        get all values from a section
        Args:
            section: section name
            default: if no document was found

        Returns:
            key value dict of all elements inside section
        """
        try:
            section_values = self.dbm.find_one_by(
                collection=SystemSettingsReader.COLLECTION,
                filter={'_id': section}
            )
        except NoDocumentFound:
            if default:
                return default
            raise SectionError(section)
        return section_values

    def get_all(self) -> list:
        return self.dbm.find_all(collection=SystemSettingsReader.COLLECTION)

    def setup(self):
        """
        get setup data
        Returns:
            setup dict
        """
        return SystemSettingsReader.SETUP_INITS


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


class ConfigFileSetError(CMDBError):
    """
    Error if code tries to set values or sections while a config file is loaded
    """

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.message = 'Configurations file: ' + self.filename + ' was loaded. No manual editing of values are allowed!'


class ConfigFileNotFound(CMDBError):
    """
    Error if local file could not be loaded
    """

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.message = 'Configurations file: ' + self.filename + ' was not found!'


class ConfigNotLoaded(CMDBError):
    """
    Error if reader is not loaded
    """

    def __init__(self, filename):
        super().__init__()
        self.message = 'Configurations file: ' + filename + ' was not loaded correctly!'


class SectionError(CMDBError):
    """
    Error if section not exists
    """

    def __init__(self, name):
        super().__init__()
        self.message = 'The section ' + name + ' does not exist!'


class KeySectionError(CMDBError):
    """
    Error if key not exists in section
    """

    def __init__(self, name):
        super().__init__()
        self.message = 'The key ' + name + ' was not found!'


def get_system_config_reader() -> SystemConfigReader:
    """
    get a instance of the configuration file reader
    Returns:
        (SystemConfigReader): instance of SystemConfigReader

    """
    return SystemConfigReader(
        SystemConfigReader.DEFAULT_CONFIG_NAME,
        SystemConfigReader.DEFAULT_CONFIG_LOCATION
    )
