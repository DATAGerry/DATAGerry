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
from cmdb.interface.blueprint import APIBlueprint
from cmdb.user_management import UserModel
from cmdb.utils.helpers import load_class

from cmdb.interface.api_parameters import CollectionParameters
from cmdb.security.acl.permission import AccessControlPermission

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
exporter_blueprint = APIBlueprint('exporter', __name__)


@exporter_blueprint.route('/extensions', methods=['GET'])
@login_required
def get_export_file_types():
    return make_response(SupportedExporterExtension().convert_to())


@exporter_blueprint.route('/', methods=['GET'])
@exporter_blueprint.protect(auth=True, right='base.framework.object.view')
@exporter_blueprint.parse_collection_parameters(view='native')
@insert_request_user
@insert_request_user
def export_objects(params: CollectionParameters, request_user: UserModel):
    try:
        _config = ExporterConfig(filter_query=params.filter, options=params.optional)
        _class = 'ZipExportType' if params.optional.get('zip', False) in ['true'] else params.optional.get('classname', '')

        exporter_class = load_class('cmdb.exporter.exporter_base.' + _class)()
        exporter = BaseExportWriter(exporter_class, _config)
        exporter.from_database(user=request_user, permission=AccessControlPermission.READ)
    except TypeNotFoundError as e:
        return abort(400, e.message)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as e:
        return abort(404, jsonify(message='Not Found', error=e.message))

    return exporter.export()
