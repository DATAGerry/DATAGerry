# dataGerry - OpenSource Enterprise CMDB
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
from cmdb.utils.error import CMDBError


class SystemReader:
    """
    Reader super class
    """

    def get_value(self, name, section):
        """
        get specific value from a section
        Args:
            name: key name of value
            section: section identifer

        Returns:
            value
        """
        raise NotImplementedError

    def get_sections(self):
        """
        get all sections from config
        Returns:
            list of config names
        """
        raise NotImplementedError

    def get_all_values_from_section(self, section):
        """
        get list of all values in section
        Args:
            section: section key

        Returns:
            key/value list of all values inside a section
        """
        raise NotImplementedError

    def setup(self):
        """
        performs an setup on call
        Returns:
            setup informations
        """
        raise NotImplementedError


class SystemConfigReader:
    """
    System reader for local config file
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
            SystemConfigReader.instance = SystemConfigReader._SystemConfigReader(config_name, config_location)
        return SystemConfigReader.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

    class _SystemConfigReader(SystemReader):

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
            self.config = configparser.RawConfigParser()
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

        def get_value(self, name, section):
            """
            get a value from a given section
            Args:
                name: key of value
                section: section of the value

            Returns:
                value
            """
            if self.config_status == SystemConfigReader.CONFIG_LOADED:
                if self.config.has_section(section):
                    if name not in self.config[section]:
                        raise KeyError(name)
                    else:
                        return self.config[section][name]
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
            if self.config_status == SystemConfigReader.CONFIG_LOADED:
                try:
                    if self.config.has_section(section):
                        return dict(self.config.items(section))
                    else:
                        raise SectionError(section)
                except KeyError:
                    raise KeySectionError(section)
            else:
                raise ConfigNotLoaded(SystemConfigReader.RUNNING_CONFIG_NAME)

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
    SETUP_INITS = [
        {
            'TODO'
        }
    ]

    def __init__(self, database_manager):
        """
        init system settings reader
        Args:
            database_manager: database manager
        """
        self.dbm = database_manager

    def get_value(self, name, section):
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

    def get_all_values_from_section(self, section):
        """
        get all values from a section
        Args:
            section: section name

        Returns:
            key value dict of all elements inside section
        """
        return self.dbm.find_all(
            collection=SystemSettingsReader.COLLECTION,
            filter={'_id': section}
        )

    def setup(self):
        """
        get setup data
        Returns:
            setup dict
        """
        return SystemSettingsReader.SETUP_INITS


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
