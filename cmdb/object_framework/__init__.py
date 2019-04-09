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
from cmdb.object_framework.cmdb_object_category import CmdbCategory
from cmdb.object_framework.cmdb_object_field_type import CmdbFieldType
from cmdb.object_framework.cmdb_object_status import CmdbObjectStatus
from cmdb.object_framework.cmdb_object_link import CmdbObjectLink
from cmdb.object_framework.cmdb_collection import CmdbCollection, CmdbCollectionTemplates

# List of init collections
__COLLECTIONS__ = [
    CmdbObject,
    CmdbType,
    CmdbCategory,
    CmdbObjectStatus,
    CmdbObjectLink,
    CmdbCollection,
    CmdbCollectionTemplates
]

