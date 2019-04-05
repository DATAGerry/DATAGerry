from cmdb.data_storage.database_connection import MongoConnector, Connector
from cmdb.data_storage.database_manager import DatabaseManagerMongo, DatabaseManager
from cmdb.data_storage.database_manager import NoDocumentFound


def get_pre_init_database() -> (DatabaseManager, DatabaseManagerMongo):
    """
    Get a database manager with parameters from system config reader
    Returns: DatabaseManager

    """
    from cmdb.data_storage import DatabaseManagerMongo, MongoConnector
    from cmdb.utils.system_reader import SystemConfigReader
    system_config_reader = SystemConfigReader()
    try:
        timeout = system_config_reader.get_value('connection_timeout', 'Database')
    except KeyError:
        timeout = MongoConnector.DEFAULT_CONNECTION_TIMEOUT
    return DatabaseManagerMongo(
        connector=MongoConnector(
            host=system_config_reader.get_value('host', 'Database'),
            port=int(system_config_reader.get_value('port', 'Database')),
            database_name=system_config_reader.get_value('database_name', 'Database'),
            timeout=timeout
        )
    )
