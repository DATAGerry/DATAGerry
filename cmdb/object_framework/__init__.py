# -*- coding: utf-8 -*-
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
from cmdb.object_framework.cmdb_object_status import CmdbObjectStatus
from cmdb.object_framework.cmdb_object_link import CmdbObjectLink
from cmdb.object_framework.cmdb_collection import CmdbCollection, CmdbCollectionTemplates
from cmdb.object_framework.cmdb_parser import CmdbParser
from cmdb.object_framework.cmdb_object_manager import CmdbObjectManager
from cmdb.object_framework.cmdb_log import CmdbLog
from cmdb.data_storage.database_manager import DatabaseManager

__COLLECTIONS__ = [
    CmdbObject,
    CmdbType,
    CmdbTypeCategory,
    CmdbFieldType,
    CmdbObjectStatus,
    CmdbObjectLink,
    CmdbCollection,
    CmdbCollectionTemplates
]


def get_object_manager(database_manager: DatabaseManager = None, event_queue=None) -> CmdbObjectManager:
    """
    auto init a instance of an object manager
    Returns (CmdbObjectManager): instance of object manager
    """
    from cmdb.data_storage import get_pre_init_database
    return CmdbObjectManager(
        database_manager=database_manager or get_pre_init_database(),
        event_queue=event_queue
    )
