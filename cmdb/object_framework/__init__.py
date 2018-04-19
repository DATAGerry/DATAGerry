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
from cmdb.object_framework.cmdb_object_type_category import CmdbTypeCategory
from cmdb.object_framework.cmdb_object_field_type import CmdbFieldType
from cmdb.object_framework.cmdb_object_manager import CmdbObjectManager
from cmdb.data_storage import DATABASE_MANAGER

OBJECT_MANAGER = CmdbObjectManager(
    database_manager=DATABASE_MANAGER
)
