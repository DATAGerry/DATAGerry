# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
This module represents the core system of the CMDB.
All initializations and specifications for creating objects,
object types and their fields are controlled here.
Except for the managers, this module can be used completely modular.
The respective DAO is used to apply the attributes and to convert
the elements for the database.
"""
from cmdb.models.object_model.cmdb_object import CmdbObject
from cmdb.models.location_model.cmdb_location import CmdbLocation
from cmdb.models.reports_model.cmdb_report import CmdbReport
from cmdb.models.reports_model.cmdb_report_category import CmdbReportCategory
from cmdb.models.section_template_model.cmdb_section_template import CmdbSectionTemplate
from cmdb.models.type_model.type import TypeModel
from cmdb.models.category_model.category import CategoryModel
from cmdb.models.object_link_model.link import ObjectLinkModel
from cmdb.models.log_model.cmdb_meta_log import CmdbMetaLog
from cmdb.models.log_model.cmdb_log import CmdbLog
from cmdb.models.log_model.cmdb_object_log import CmdbObjectLog
from cmdb.models.webhook_model.cmdb_webhook_model import CmdbWebhook
# -------------------------------------------------------------------------------------------------------------------- #

CmdbLog.register_log_type(CmdbObjectLog.__name__, CmdbObjectLog)

# List of init collections
__COLLECTIONS__ = [
    CmdbObject,
    TypeModel,
    CategoryModel,
    CmdbMetaLog,
    ObjectLinkModel,
    CmdbLocation,
    CmdbSectionTemplate,
    CmdbReportCategory,
    CmdbReport,
    CmdbWebhook,
]
