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

from flask import abort, request, current_app

from cmdb.framework.cmdb_link import CmdbLink
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerInsertError
from cmdb.interface.rest_api.framework_routes.object_routes import object_blueprint
from cmdb.interface.route_utils import make_response, NestedBlueprint, insert_request_user, login_required, \
    right_required
from cmdb.user_management import User

with current_app.app_context():
    object_manager = current_app.object_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
link_rest = NestedBlueprint(object_blueprint, url_prefix='/link')


@link_rest.route('/<int:public_id>/', methods=['GET'])
@link_rest.route('/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_link(public_id: int, request_user: User):
    try:
        ack = []
    except ObjectManagerGetError:
        return abort(404)
    return make_response(ack)


@link_rest.route('/primary/<int:public_id>/', methods=['GET'])
@link_rest.route('/secondary/<int:public_id>', methods=['GET'])
def get_link_by_partner(public_id: int):
    return get_link(public_id)


@link_rest.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.framework.object.add')
def add_link(request_user: User):
    try:
        new_link_params = {**request.json}
    except TypeError:
        return abort(400)

    try:
        ack = object_manager.insert_link(new_link_params)
    except ObjectManagerInsertError:
        return abort(400)
    return make_response(ack)
