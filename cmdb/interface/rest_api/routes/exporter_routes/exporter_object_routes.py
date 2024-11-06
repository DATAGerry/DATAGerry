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
from flask import abort, jsonify, current_app

from cmdb.exporter.config.config_type import ExporterConfig
from cmdb.exporter.writer.writer_base import SupportedExporterExtension, BaseExportWriter
from cmdb.interface.route_utils import login_required, insert_request_user
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.rest_api.responses import GetSingleValueResponse
from cmdb.user_management.models.user import UserModel
from cmdb.utils.helpers import load_class
from cmdb.interface.rest_api.responses.helpers.api_parameters import CollectionParameters
from cmdb.security.acl.permission import AccessControlPermission

from cmdb.errors.type import TypeNotFoundError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

exporter_blueprint = APIBlueprint('exporter', __name__)

# -------------------------------------------------------------------------------------------------------------------- #

@exporter_blueprint.route('/extensions', methods=['GET'])
@login_required
def get_export_file_types():
    """TODO: document"""
    return GetSingleValueResponse(SupportedExporterExtension().convert_to()).make_response()


@exporter_blueprint.route('/', methods=['GET'])
@exporter_blueprint.parse_collection_parameters(view='native')
@insert_request_user
@exporter_blueprint.protect(auth=True, right='base.framework.object.view')
def export_objects(params: CollectionParameters, request_user: UserModel):
    """TODO: document"""
    try:
        _config = ExporterConfig(parameters=params, options=params.optional)
        _class = 'ZipExportType' if params.optional.get('zip', False) in ['true'] \
            else params.optional.get('classname', 'JsonExportType')
        exporter_class = load_class('cmdb.exporter.exporter_base.' + _class)()

        if current_app.cloud_mode:
            current_app.database_manager.connector.set_database(request_user.database)

        exporter = BaseExportWriter(exporter_class, _config)

        exporter.from_database(current_app.database_manager, request_user, AccessControlPermission.READ)
    except TypeNotFoundError:
        #ERROR-FIX
        return abort(400)
    except ModuleNotFoundError:
        #ERROR-FIX
        return abort(400)
    except Exception as err:
        LOGGER.debug("[export_objects] Exception: %s, Type: %s", err, type(err))
        return abort(404, jsonify(message='Not Found', error='Export objects Exception'))

    return exporter.export()
