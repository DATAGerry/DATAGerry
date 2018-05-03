"""
This module presents the core system of the CMDB.
All initializations and specifications for creating objects,
object types and their fields are controlled here.
Except for the manager, this module can be used completely modular.
The respective DAO is used to apply the attributes and to convert
the elements for the database.
"""
from cmdb.object_framework.cmdb_dao import CmdbDAO
from cmdb.object_framework.cmdb_object import CmdbObject
from cmdb.object_framework.cmdb_object_type import CmdbType
from cmdb.object_framework.cmdb_object_category import CmdbTypeCategory
from cmdb.object_framework.cmdb_object_field_type import CmdbFieldType
from cmdb.object_framework.cmdb_object_manager import CmdbObjectManager
from cmdb.data_storage.database_connection import MongoConnector
from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.application_utils import SYSTEM_CONFIG_READER

OBJECT_MANAGER = CmdbObjectManager(
    database_manager=DatabaseManagerMongo(
    connector=MongoConnector(
        host=SYSTEM_CONFIG_READER.get_value('host', 'Database'),
        port=int(SYSTEM_CONFIG_READER.get_value('port', 'Database')),
        database_name=SYSTEM_CONFIG_READER.get_value('database_name', 'Database'),
        timeout=MongoConnector.DEFAULT_CONNECTION_TIMEOUT
    )
)

)
