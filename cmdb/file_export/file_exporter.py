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

from flask import abort, Response

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.framework.cmdb_errors import ObjectNotFoundError, TypeNotFoundError
from cmdb.file_export.export_types import ExportType
from cmdb.framework.cmdb_object_manager import CmdbObjectManager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

from cmdb.utils.system_config import SystemConfigReader

object_manager = CmdbObjectManager(database_manager=DatabaseManagerMongo(
    **SystemConfigReader().get_all_values_from_section('Database')
))


class FileExporter:

    @staticmethod
    def get_filetypes():
        filetypes = ["CsvExportType", "JsonExportType", "XlsxExportType", "XmlExportType"]
        return filetypes

    def __init__(self, object_type, export_type: ExportType, public_id: str, **kwargs):
        """init of FileExporter

        Args:
            object_type: type of object e.g. CmdbObject or CmdbObject by CmdbType ID
            export_type: the ExportType object
            public_id: public id which implements the object / type
            **kwargs: additional data
        """
        self.object_type = object_type
        self.export_type = export_type
        self.public_id = public_id

        # object_list: list of objects e.g CmdbObject or CmdbType
        self.object_list = []
        self.response = None

    def get_object_type(self):
        """

        Returns: type of object e.g. CmdbObject, CmdbType or CmdbObject by CmdbType ID (object, type, object/type)

        """
        return self.object_type

    def get_object_list(self):
        """

        Returns: list of objects e.g CmdbObject or CmdbType

        """
        file_type = self.get_object_type()
        if 'object' == file_type:
            return self.get_object_by_id()
        elif 'type' == file_type:
            return self.get_type_by_id()
        return self.get_all_objects_by_type_id()

    def get_response(self):
        """

        Returns: Response element

        """
        return self.response

    def set_response(self, value):
        self.response = value

    #
    #   Get values from the database
    #

    def get_object_by_id(self):
        try:
            query = self._build_query({'public_id': self.public_id}, q_operator='$or')
            return object_manager.get_objects_by(sort="public_id", **query)
        except ObjectNotFoundError as e:
            return abort(400, e)
        except CMDBError:
            return abort(404)

    def get_all_objects_by_type_id(self):
        try:
            return object_manager.get_objects_by_type(self.public_id)
        except ObjectNotFoundError as e:
            return abort(400, e)
        except CMDBError:
            return abort(404)

    def get_type_by_id(self):
        try:
            query = self._build_query({'public_id': self.public_id}, q_operator='$or')
            return object_manager.get_types_by(sort="public_id", **query)
        except TypeNotFoundError as e:
            return abort(400, e)
        except CMDBError:
            return abort(404)

    #
    # Advanced methods
    #

    def _build_query(self, args, q_operator='$and'):
        query_list = []
        try:
            for key, value in args.items():
                for v in value.split(","):
                    try:
                        query_list.append({key: int(v)})
                    except (ValueError, TypeError):
                        return abort(400)
            return {q_operator: query_list}
        except CMDBError as e:
            abort(400, e)

    def add_to_object_list(self, value):
        self.object_list.append(value)

    def export(self):
        import datetime
        import time

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H_%M_%S')
        return Response(
            self.export_type.export(self.get_object_list()),
            mimetype="text/" + self.export_type.__class__.FILE_EXTENSION,
            headers={
                "Content-Disposition":
                    "attachment; filename=%s.%s" % (timestamp, self.export_type.__class__.FILE_EXTENSION)
            }
        )
