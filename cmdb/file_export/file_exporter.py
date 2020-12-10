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

from cmdb.database.managers import DatabaseManagerMongo
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.results import IterationResult
from cmdb.framework.cmdb_object import CmdbObject

from cmdb.file_export.export_types import ExportType
from cmdb.search.query.builder import Builder
from cmdb.user_management import UserModel

from cmdb.security.acl.permission import AccessControlPermission

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

from cmdb.utils.system_config import SystemConfigReader
from cmdb.utils.helpers import load_class

object_manager = CmdbObjectManager(database_manager=DatabaseManagerMongo(
    **SystemConfigReader().get_all_values_from_section('Database')
))


class SupportedExportTypes:
    """Supported export types for object-file export (csv, json, xlsx, xml)"""

    def __init__(self, extensions=None):
        """
        Constructor of SupportedExportTypes
        Args:
            extensions: List of file extension
        """
        arguments = extensions if extensions else []
        self.extensions = [*["CsvExportType", "JsonExportType", "XlsxExportType", "XmlExportType"], *arguments]

    def get_extensions(self):
        """Get list of supported export types"""
        return self.extensions

    def convert_to(self):
        """Converts the supported export types inside the list to a passed ExportType type list."""
        _list = []
        for type_element in self.get_extensions():
            type_element_class = load_class('cmdb.file_export.export_types.' + type_element)
            _list.append({
                'extension': type_element,
                'label': type_element_class.LABEL,
                'icon': type_element_class.ICON,
                'multiTypeSupport': type_element_class.MULTITYPE_SUPPORT,
                'helperText': type_element_class.DESCRIPTION,
                'active': type_element_class.ACTIVE
            })
        return _list


class FileExporter:

    def __init__(self, exporter_class: ExportType, ids, export_type=None, *args):
        """init of FileExporter

        Args:
            object_type: type of object e.g. CmdbObject or CmdbObject by TypeModel ID
            exporter_class: the ExportType class
            ids: public id which implements the object / type
            *args: additional data
        """
        self.export_type = export_type
        self.exporter_class = exporter_class
        self.ids = ids
        self.zip = False if len(args) == 0 else args[0]
        self.objects = []

    def from_database(self, user: UserModel, permission: AccessControlPermission):
        """Get all objects from the collection"""
        try:
            builder = Builder()

            if not isinstance(self.ids, list):
                self.ids = [self.ids]

            _in = builder.in_('public_id', self.ids)
            if self.export_type == 'type' or not self.export_type:
                _in = builder.in_('type_id', self.ids)

            result: IterationResult[CmdbObject] = object_manager.get_objects_by(user=user, permission=permission, **_in)
        except CMDBError:
            return abort(400)
        return result

    def export(self):
        import datetime
        import time

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H_%M_%S')
        if self.zip:
            export = self.exporter_class.export(self.objects, self.zip)
        else:
            export = self.exporter_class.export(self.objects)
        return Response(
            export,
            mimetype="text/" + self.exporter_class.__class__.FILE_EXTENSION,
            headers={
                "Content-Disposition":
                    "attachment; filename=%s.%s" % (timestamp, self.exporter_class.__class__.FILE_EXTENSION)
            }
        )
