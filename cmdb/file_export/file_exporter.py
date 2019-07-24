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

from flask import abort, Response
from cmdb.object_framework.cmdb_errors import ObjectNotFoundError, TypeNotFoundError
from cmdb.object_framework.cmdb_object_manager import object_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception


class FileExporter:

    def __init__(self, object_type, file_extension: str, public_id: str, **kwargs):
        """init of FileExporter

        Args:
            object_type: type of object e.g. CmdbObject or CmdbObject by CmdbType ID
            file_extension: current file file_extension for download file
            public_id: public id which implements the object / type
            **kwargs: additional data
        """
        self.object_type = object_type
        self.file_extension = file_extension
        self.public_id = public_id

        # extension_list: filled with allowed formats for user/s
        self.extension_list = [
            {'id': 'xml', 'label': 'XML', 'icon': 'fa-code', 'helperText': 'Export as XML', 'active': True},
            {'id': 'csv', 'label': 'CSV', 'icon': 'fa-table', 'helperText': 'Export as CSV (only of the same type)', 'active': True},
            {'id': 'json', 'label': 'JSON', 'icon': 'fa-file-text-o', 'helperText': 'Export as JSON', 'active': True},
            {'id': 'xls', 'label': 'XLS', 'icon': 'fa-file-excel-o', 'helperText': 'Export as XLS', 'active': True}
        ]

        # object_list: list of objects e.g CmdbObject or CmdbType
        self.object_list = []
        self.response = None
        super(FileExporter, self).__init__(**kwargs)

    #
    #   Getter and Setter
    #

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

    # TODO Check which formats are allowed for users
    def get_extension_list(self):
        """

        Returns: allowed formats (xml, csv, json etc.) for user/s

        """
        return self.extension_list

    # TODO Check which formats are allowed for users
    def set_extension_list(self, value):
        self.extension_list = value

    #
    #   Get values​from the database
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

    def add_to_extension_list(self, value):
        self.extension_list.append(value)

    def add_to_object_list(self, value):
        self.object_list.append(value)

    def export(self, mime_type: str, file_extension: str):
        import datetime
        import time

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H_%M_%S')
        return Response(
            self.response,
            mimetype=mime_type,
            headers={
                "Content-Disposition":
                    "attachment; filename=%s.%s" % (timestamp, file_extension)
            }
        )
