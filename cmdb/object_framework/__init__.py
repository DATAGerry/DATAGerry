# -*- coding: utf-8 -*-
# dataGerry - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

