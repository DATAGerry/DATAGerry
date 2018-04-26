from cmdb.application_utils.system_reader import SystemConfigReader, SystemSettingsReader

SYSTEM_CONFIG_READER = SystemConfigReader(
    config_name=SystemConfigReader.DEFAULT_CONFIG_NAME,
    config_location=SystemConfigReader.DEFAULT_CONFIG_LOCATION
)

from cmdb.data_storage import DATABASE_MANAGER
SYSTEM_SETTINGS_READER = SystemSettingsReader(
    database_manager=DATABASE_MANAGER
)
