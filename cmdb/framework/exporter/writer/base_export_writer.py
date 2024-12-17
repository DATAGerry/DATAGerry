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
"""TODO: document"""
import logging
import datetime
import time
from flask import Response

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.manager.objects_manager import ObjectsManager

from cmdb.models.user_model.user import UserModel
from cmdb.models.object_model.cmdb_object import CmdbObject
from cmdb.framework.rendering.render_list import RenderList
from cmdb.framework.rendering.render_result import RenderResult
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.framework.exporter.config.exporter_config import ExporterConfig
from cmdb.framework.exporter.format.base_exporter_format import BaseExporterFormat
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class  BaseExportWriter:
    """TODO: document"""

    def __init__(self, export_format: BaseExporterFormat, export_config: ExporterConfig):
        """init of FileExporter

        Args:
            export_format: In which format is exported (csv, json, xlsx, xml)
            export_config: Configuration parameters such as filter or zip export_format
        """
        self.export_format = export_format
        self.export_config = export_config
        self.data: list[RenderResult] = []


    def from_database(
            self,
            dbm: MongoDatabaseManager,
            user: UserModel,
            permission: AccessControlPermission
        ):
        """Get all objects from the collection"""
        objects_manager = ObjectsManager(dbm)

        export_params = self.export_config.parameters
        builder_params = BuilderParameters(criteria=export_params.filter,
                                           sort=export_params.sort,
                                           order=export_params.order)


        tmp_result: list[CmdbObject] = objects_manager.iterate(builder_params, user, permission).results

        self.data = RenderList(tmp_result,
                                user,
                                True,
                                objects_manager).render_result_list(raw=False)


    def export(self):
        """TODO: document"""

        conf_option = self.export_config.options
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H_%M_%S')
        export = self.export_format.export(self.data, conf_option)

        return Response(
            export,
            mimetype="text/" + self.export_format.__class__.FILE_EXTENSION,
            headers={
                "Content-Disposition":
                    f"attachment; filename={timestamp}.{self.export_format.__class__.FILE_EXTENSION}"
            }
        )
