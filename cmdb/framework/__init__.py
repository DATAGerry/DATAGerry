# -*- coding: utf-8 -*-
# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
This module presents the core system of the CMDB.
All initializations and specifications for creating objects,
object types and their fields are controlled here.
Except for the managers, this module can be used completely modular.
The respective DAO is used to apply the attributes and to convert
the elements for the database.
"""
from cmdb.framework.cmdb_dao import CmdbDAO
from cmdb.framework.cmdb_object import CmdbObject
from cmdb.framework.models import TypeModel
from cmdb.framework.models import CategoryModel
from cmdb.framework.models import ObjectLinkModel
from cmdb.framework.models.log import CmdbLog, CmdbObjectLog, CmdbMetaLog

CmdbLog.register_log_type(CmdbObjectLog.__name__, CmdbObjectLog)

# List of init collections
__COLLECTIONS__ = [
    CmdbObject,
    TypeModel,
    CategoryModel,
    CmdbMetaLog,
    ObjectLinkModel
]

