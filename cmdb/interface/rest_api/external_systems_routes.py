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

from cmdb.exportd.exportd_job.exportd_job_manager import ExportdJobManager

from cmdb.utils.helpers import load_class, get_module_classes
from cmdb.interface.route_utils import make_response, login_required
from cmdb.interface.blueprint import RootBlueprint
# -------------------------------------------------------------------------------------------------------------------- #

with current_app.app_context():
    exportd_manager = ExportdJobManager(current_app.database_manager)

LOGGER = logging.getLogger(__name__)
external_system = RootBlueprint('external_system', __name__, url_prefix='/externalsystem')


# DEFAULT ROUTES
@external_system.route('/', methods=['GET'])
@login_required
def get_external_system_list():
    """TODO: document"""
    return make_response(get_module_classes('cmdb.exportd.externals.external_systems'))


@external_system.route('/parameters/<string:class_external_system>', methods=['GET'])
# @login_required
def get_external_system_params(class_external_system):
    """TODO: document"""
    try:
        external_system_class = load_class(f"cmdb.exportd.externals.external_systems.{class_external_system}")
        list_of_parameters = external_system_class.parameters
    except Exception as err:
        #TODO: ERROR-FIX
        LOGGER.debug(str(err))
        return abort(404, jsonify(message='Not Found', error='external system params'))

    return make_response(list_of_parameters)


@external_system.route('/variables/<string:class_external_system>', methods=['GET'])
# @login_required
def get_external_system_variables(class_external_system):
    """TODO: document"""
    try:
        external_system_class = load_class(f"cmdb.exportd.externals.external_systems.{class_external_system}")
        list_of_parameters = external_system_class.variables
    except Exception as error:
        #TODO: ERROR-FIX
        LOGGER.debug(str(error))
        return abort(404, jsonify(message='Not Found', error='external system variables'))

    return make_response(list_of_parameters)
