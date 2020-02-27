from cmdb.utils.error import CMDBError


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