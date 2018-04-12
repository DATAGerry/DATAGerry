"""
cmdb global init
"""

from cmdb.system_reader import SystemConfigReader, SystemSettingsReader
# Loading global system config reader
SYSTEM_CONFIG_READER = SystemConfigReader(
    config_name=SystemConfigReader.DEFAULT_CONFIG_NAME,
    config_location=SystemConfigReader.DEFAULT_CONFIG_LOCATION
)
# Loading global system settings reader
SYSTEM_SETTINGS_READER = SystemSettingsReader(
    database_manager=None
)
