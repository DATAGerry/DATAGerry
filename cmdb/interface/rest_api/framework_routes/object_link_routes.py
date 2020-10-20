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
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerInsertError, ObjectManagerDeleteError
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.interface.rest_api.framework_routes.object_routes import object_blueprint
from cmdb.interface.route_utils import make_response, insert_request_user, login_required, \
    right_required
from cmdb.interface.blueprint import NestedBlueprint
from cmdb.user_management import UserModel

with current_app.app_context():
    object_manager: CmdbObjectManager = current_app.object_manager

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
def get_link(public_id: int, request_user: UserModel):
    try:
        return object_manager.get_link(public_id=public_id)
    except ObjectManagerGetError as err:
        return abort(404, err.message)


@link_rest.route('/partner/<int:public_id>/', methods=['GET'])
@link_rest.route('/partner/<int:public_id>', methods=['GET'])
def get_partner_links(public_id: int):
    try:
        link_list = object_manager.get_links_by_partner(public_id=public_id)
    except ObjectManagerGetError as err:
        LOGGER.error(f'[CmdbLinks] Error while getting partner links: {err}')
        return abort(404, err.message)
    LOGGER.debug(f'[CmdbLinks] Found link list: {link_list}')
    if len(link_list) == 0:
        return make_response(link_list, 204)
    return make_response(link_list)


@link_rest.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.framework.object.add')
def add_link(request_user: UserModel):
    try:
        new_link_params = {**request.json}
    except TypeError:
        return abort(400)

    try:
        ack = object_manager.insert_link(new_link_params)
    except ObjectManagerInsertError:
        return abort(400)
    return make_response(ack)


@link_rest.route('/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.framework.object.delete')
def remove_link(public_id: int, request_user: UserModel):
    try:
        ack = object_manager.delete_link(public_id)
    except ObjectManagerDeleteError as err:
        return abort(400, err.message)
    return make_response(ack)
