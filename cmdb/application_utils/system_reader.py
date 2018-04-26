"""
Collection of system readers which loads configuration files and settings
"""
import os


class SystemReader:
    """
    Reader super class
    """
    def get_value(self, name, section):
        """
        get specific value from a section
        :param name: key name of value
        :param section: section identifer
        :return: value
        """
        raise NotImplementedError

    def get_sections(self):
        """
        get all sections from config
        :return: list of config names
        """
        raise NotImplementedError

    def get_all_values_from_section(self, section):
        """
        get list of all values in section
        :param section key
        :return: key/value list of all values inside a section
        """
        raise NotImplementedError

    def setup(self):
        """
        performs an setup on call
        :return: setup informations
        """
        raise NotImplementedError


class SystemConfigReader(SystemReader):
    """
    System reader for local config file
    """
    DEFAULT_CONFIG_LOCATION = os.path.join(os.path.dirname(__file__), '../../etc/')
    DEFAULT_CONFIG_NAME = 'cmdb.conf'
    CONFIG_LOADED = True
    CONFIG_NOT_LOADED = False

    def __init__(self, config_name, config_location):
        """
        init the system config reader
        :param config_name: name of config file with extension
        :param config_location: directory of config file
        """
        import configparser
        self.config_status = SystemConfigReader.CONFIG_NOT_LOADED
        self.config = configparser.RawConfigParser()
        self.config_name = config_name
        self.config_location = config_location
        self.config_file = self.config_location + self.config_name
        self.config_status = self.setup()
        if self.config_status == SystemConfigReader.CONFIG_NOT_LOADED:
            raise ConfigFileNotFound(self.config_name)

    def setup(self):
        try:
            self.read_config_file(self.config_file)
            return SystemConfigReader.CONFIG_LOADED
        except ConfigFileNotFound:
            return SystemConfigReader.CONFIG_NOT_LOADED

    def read_config_file(self, file):
        """
        helper function for file reading
        sets the path directly inside the config attribute
        :param file: path to config file
        :return:
        """
        if os.path.isfile(file):
            self.config.read(file)
        else:
            raise ConfigFileNotFound(self.config_name)

    def get_value(self, name, section):
        """
        get a value from a given section
        :param name: key of value
        :param section: section of the value
        :return: value
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
            raise ConfigNotLoaded(SystemConfigReader.DEFAULT_CONFIG_NAME)

    def get_sections(self):
        """
        get all sections from config
        :return: list of sections inside a config
        """
        if self.config_status == SystemConfigReader.CONFIG_LOADED:
            return self.config.sections()
        else:
            raise ConfigNotLoaded(SystemConfigReader.DEFAULT_CONFIG_NAME)

    def get_all_values_from_section(self, section):
        """
        get all values from a section
        :param section: section name
        :return: key value dict of all elements inside section
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
            raise ConfigNotLoaded(SystemConfigReader.DEFAULT_CONFIG_NAME)

    def status(self):
        """
        checks if config is loaded correctly
        :return: True/False statement of loading status
        """
        if self.config_status:
            return self.CONFIG_LOADED
        return self.CONFIG_NOT_LOADED

    def __repr__(self):
        """
        Helper function for debugging
        :return:
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
        :param dbm: database manager
        """
        self.dbm = database_manager

    def get_value(self, name, section):
        """
        get a value from a given section
        :param name: key of value
        :param section: section of the value
        :return: value
        """
        return self.dbm.find_one_by(
            collection=SystemSettingsReader.COLLECTION,
            filter={'_id': section}
        )[name]

    def get_sections(self):
        """
        get all sections from config
        :return: list of sections inside a config
        """
        return self.dbm.find_all(
            collection=SystemSettingsReader.COLLECTION,
            projection={'_id': 1}
        )

    def get_all_values_from_section(self, section):
        """
        get all values from a section
        :param section: section name
        :return: key value dict of all elements inside section
        """
        return self.dbm.find_all(
            collection=SystemSettingsReader.COLLECTION,
            filter={'_id': section}
        )

    def setup(self):
        return SystemSettingsReader.SETUP_INITS


class ConfigFileNotFound(Exception):
    """
    Error if local file could not be loaded
    """
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.message = 'Configurations file: '+self.filename+' was not found!'


class ConfigNotLoaded(Exception):
    """
    Error if reader is not loaded
    """
    def __init__(self, filename):
        super().__init__()
        self.message = 'Configurations file: '+filename+' was not loaded correctly!'


class SectionError(Exception):
    """
    Error if section not exists
    """
    def __init__(self, name):
        super().__init__()
        self.message = 'The section '+name+' does not exist!'


class KeySectionError(Exception):
    """
    Error if key not exists in section
    """
    def __init__(self, name):
        super().__init__()
        self.message = 'The key '+name+' was not found!'
