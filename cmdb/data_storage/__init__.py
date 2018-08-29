from cmdb.data_storage.database_connection import MongoConnector
from cmdb.data_storage.database_manager import DatabaseManagerMongo, DatabaseManager
from cmdb.data_storage.database_manager import NoDocumentFound


def get_pre_init_database():
    from cmdb.data_storage import DatabaseManagerMongo, MongoConnector
    from cmdb.utils import get_system_config_reader
    system_config_reader = get_system_config_reader()
    return DatabaseManagerMongo(
        connector=MongoConnector(
                host=system_config_reader.get_value('host', 'Database'),
                port=int(system_config_reader.get_value('port', 'Database')),
                database_name=system_config_reader.get_value('database_name', 'Database'),
                timeout=MongoConnector.DEFAULT_CONNECTION_TIMEOUT
        )
    )
