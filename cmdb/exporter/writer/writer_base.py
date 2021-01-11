# DATAGERRY - OpenSource Enterprise CMDB
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


from flask import Response, abort

from cmdb.framework.results import IterationResult
from cmdb.framework.cmdb_object import CmdbObject

from cmdb.user_management import UserModel
from cmdb.security.acl.permission import AccessControlPermission

from cmdb.exporter.config.config_type import ExporterConfig
from cmdb.exporter.format.format_base import BaseExporterFormat

from cmdb.database.managers import DatabaseManagerMongo
from cmdb.framework.cmdb_object_manager import CmdbObjectManager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

from cmdb.utils.helpers import load_class
from cmdb.utils.system_config import SystemConfigReader

object_manager = CmdbObjectManager(database_manager=DatabaseManagerMongo(
    **SystemConfigReader().get_all_values_from_section('Database')
))


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


class BaseExportWriter:

    def __init__(self, export_format: BaseExporterFormat, export_config: ExporterConfig):
        """init of FileExporter

        Args:
            export_format: In which format is exported (csv, json, xlsx, xml)
            export_config: Configuration parameters such as filter or zip export_format
        """
        self.export_format = export_format
        self.export_config = export_config
        self.data = []

    def from_database(self, user: UserModel, permission: AccessControlPermission):
        """Get all objects from the collection"""
        try:

            _query = self.export_config.filter_query

            self.data: IterationResult[CmdbObject] = object_manager.get_objects_by(user=user, permission=permission, **_query)
        except CMDBError as e:
            return abort(400, e)

    def export(self):
        import datetime
        import time

        conf_option = self.export_config.options
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H_%M_%S')
        if conf_option and conf_option['zip']:
            export = self.export_format.export(self.data, conf_option['classname'])
        else:
            export = self.export_format.export(self.data)
        return Response(
            export,
            mimetype="text/" + self.export_format.__class__.FILE_EXTENSION,
            headers={
                "Content-Disposition":
                    "attachment; filename=%s.%s" % (timestamp, self.export_format.__class__.FILE_EXTENSION)
            }
        )
