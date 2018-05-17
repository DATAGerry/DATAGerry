"""
Global objects for database management
"""
from cmdb.application_utils.system_reader import SystemConfigReader
from cmdb.data_storage.database_connection import MongoConnector
from cmdb.data_storage.database_manager import DatabaseManagerMongo

database_reader = SystemConfigReader(
    config_name=SystemConfigReader.DEFAULT_CONFIG_NAME,
    config_location=SystemConfigReader.DEFAULT_CONFIG_LOCATION
)
DATABASE_MANAGER = DatabaseManagerMongo(
    connector=MongoConnector(
        host=database_reader.get_value('host', 'Database'),
        port=int(database_reader.get_value('port', 'Database')),
        database_name=database_reader.get_value('database_name', 'Database'),
        timeout=MongoConnector.DEFAULT_CONNECTION_TIMEOUT
    )
)
