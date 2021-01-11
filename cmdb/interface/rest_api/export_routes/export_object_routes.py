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

import logging

from flask import abort, jsonify, request
from cmdb.framework.cmdb_errors import TypeNotFoundError
from cmdb.exporter.config.config_type import ExporterConfig
from cmdb.exporter.writer.writer_base import SupportedExporterExtension, BaseExportWriter
from cmdb.interface.route_utils import make_response, login_required, insert_request_user
from cmdb.interface.blueprint import RootBlueprint
from cmdb.user_management import UserModel
from cmdb.utils.helpers import load_class

from cmdb.security.acl.permission import AccessControlPermission

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
file_blueprint = RootBlueprint('file_rest', __name__, url_prefix='/export/object')


@file_blueprint.route('/extensions', methods=['GET'])
@login_required
def get_export_file_types():
    return make_response(SupportedExporterExtension().convert_to())


@file_blueprint.route('/', methods=['GET'])
@login_required
@insert_request_user
def export_objects(request_user: UserModel):
    import json
    try:
        _filter = json.loads(request.args.get('filter', None))
        _class = request.args.get('classname', '')
        _zipping = request.args.get('zip', False) in ['true', 'True']
        _config = ExporterConfig(filter_query=_filter, options={'classname': _class, 'zip': _zipping})

        if _zipping:
            export_type_class = load_class('cmdb.exporter.exporter_base.' + 'ZipExportType')()
            file_export = BaseExportWriter(export_type_class, _config)
        else:
            export_type_class = load_class('cmdb.exporter.exporter_base.' + _class)()
            file_export = BaseExportWriter(export_type_class, _config)

        file_export.from_database(user=request_user, permission=AccessControlPermission.READ)
    except TypeNotFoundError as e:
        return abort(400, e.message)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as e:
        return abort(404, jsonify(message='Not Found', error=e.message))

    return file_export.export()


@file_blueprint.route('/<int:type_id>/<string:export_class>', methods=['GET'])
@login_required
@insert_request_user
def export_objects_by_type_id(type_id, export_class, request_user: UserModel):
    try:
        exporter_format_class = load_class('cmdb.exporter.exporter_base.' + export_class)
        _format = exporter_format_class()
        _filter = {'type_id': type_id}
        _config = ExporterConfig(filter_query=_filter)
        file_export = BaseExportWriter(_format, _config)
        file_export.from_database(user=request_user, permission=AccessControlPermission.READ)
    except TypeNotFoundError as e:
        return abort(400, e.message)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as e:
        return abort(404, jsonify(message='Not Found', error=e.message))

    return file_export.export()

