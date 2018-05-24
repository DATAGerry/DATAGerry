from cmdb.application_utils.system_reader import SystemConfigReader, SystemSettingsReader
from cmdb.application_utils.system_writer import SystemSettingsWriter
from cmdb.application_utils.security import SecurityManager, TokenManager
from cmdb.application_utils.logger import log

SYSTEM_CONFIG_READER = SystemConfigReader(
    config_name=SystemConfigReader.DEFAULT_CONFIG_NAME,
    config_location=SystemConfigReader.DEFAULT_CONFIG_LOCATION
)


def get_system_config_reader():
    return SystemConfigReader(
        config_name=SystemConfigReader.DEFAULT_CONFIG_NAME,
        config_location=SystemConfigReader.DEFAULT_CONFIG_LOCATION
    )


def get_system_settings_writer(database_manager):
    return SystemSettingsWriter(
        database_manager=database_manager
    )


def get_system_settings_reader(database_manager):
    return SystemSettingsReader(
        database_manager=database_manager
    )