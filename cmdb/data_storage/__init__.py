from cmdb import SYSTEM_CONFIG_READER
from cmdb.data_storage.database_connection import MongoConnector
GLOBAL_DATABASE_MANAGER = MongoConnector(
    host=SYSTEM_CONFIG_READER.get_value('host', 'Database'),
    port=SYSTEM_CONFIG_READER.get_value('port', 'Database'),
    database_name=SYSTEM_CONFIG_READER.get_value('database_name', 'Database'),
    auth=SYSTEM_CONFIG_READER.get_all_values_from_section('DatabaseAuth')
)