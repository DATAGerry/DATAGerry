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

from flask import abort, jsonify, current_app
from cmdb.utils.helpers import load_class, get_module_classes
from cmdb.interface.route_utils import make_response, login_required
from cmdb.interface.blueprint import RootBlueprint

with current_app.app_context():
    exportd_manager = current_app.exportd_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
external_system = RootBlueprint('external_system', __name__, url_prefix='/externalsystem')


# DEFAULT ROUTES
@external_system.route('/', methods=['GET'])
@login_required
def get_external_system_list():
    return make_response(get_module_classes('cmdb.exportd.externals.external_systems'))


@external_system.route('/parameters/<string:class_external_system>', methods=['GET'])
# @login_required
def get_external_system_params(class_external_system):
    try:
        external_system_class = load_class("cmdb.exportd.externals.external_systems.{}".format(class_external_system))
        list_of_parameters = external_system_class.parameters
    except Exception as e:
        return abort(400, e)
    except CMDBError as e:
        return abort(404, jsonify(message='Not Found', error=e.message))
    return make_response(list_of_parameters)


@external_system.route('/variables/<string:class_external_system>', methods=['GET'])
# @login_required
def get_external_system_variables(class_external_system):
    try:
        external_system_class = load_class("cmdb.exportd.externals.external_systems.{}".format(class_external_system))
        list_of_parameters = external_system_class.variables
    except Exception as e:
        return abort(400, e)
    except CMDBError as e:
        return abort(404, jsonify(message='Not Found', error=e.message))
    return make_response(list_of_parameters)
