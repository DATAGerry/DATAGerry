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
from flask import Response, abort

from cmdb.manager.objects_manager import ObjectsManager

from cmdb.cmdb_objects.cmdb_object import CmdbObject
from cmdb.framework.cmdb_render import RenderList, RenderResult
from cmdb.user_management.models.user import UserModel
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.exporter.config.config_type import ExporterConfig
from cmdb.exporter.format.format_base import BaseExporterFormat
from cmdb.utils.helpers import load_class
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                          SupportedExporterExtension - CLASS                                          #
# -------------------------------------------------------------------------------------------------------------------- #
class SupportedExporterExtension:
    """Supported export extensions for exporting (csv, json, xlsx, xml)"""


    def __init__(self, extensions=None):
        """
        Constructor of SupportedExporterExtension
        Args:
            extensions: List of export extension
        """
        arguments = extensions if extensions else []
        self.extensions = [*["CsvExportType", "JsonExportType", "XlsxExportType", "XmlExportType"], *arguments]


    def get_extensions(self):
        """Get list of supported export extension"""
        return self.extensions


    def convert_to(self):
        """Converts the supported export extension inside the list to a passed BaseExporterFormat list."""
        _list = []
        for type_element in self.get_extensions():
            type_element_class = load_class('cmdb.exporter.exporter_base.' + type_element)
            _list.append({
                'extension': type_element,
                'label': type_element_class.LABEL,
                'icon': type_element_class.ICON,
                'multiTypeSupport': type_element_class.MULTITYPE_SUPPORT,
                'helperText': type_element_class.DESCRIPTION,
                'active': type_element_class.ACTIVE
            })
        return _list

#CLASS-FIX
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


    def from_database(self, database_manager, user: UserModel, permission: AccessControlPermission):
        """Get all objects from the collection"""
        objects_manager = ObjectsManager(database_manager)

        export_params = self.export_config.parameters
        builder_params = BuilderParameters(criteria=export_params.filter,
                                           sort=export_params.sort,
                                           order=export_params.order)

        try:
            tmp_result: list[CmdbObject] = objects_manager.iterate(builder_params, user, permission).results

            self.data = RenderList(tmp_result,
                                   user,
                                   True,
                                   objects_manager).render_result_list(raw=False)
        except Exception:
            #ERROR-FIX
            return abort(400)


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
