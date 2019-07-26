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

import logging

from flask import request, abort
from cmdb.user_management.user_manager import user_manager
from cmdb.data_storage import get_pre_init_database
from cmdb.utils import get_security_manager
from cmdb.interface.route_utils import make_response, RootBlueprint

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

auth_routes = RootBlueprint('auth_rest', __name__, url_prefix='/auth')
LOGGER = logging.getLogger(__name__)


@auth_routes.route('/login', methods=['POST'])
def login_call():
    login_data = request.json
    LOGGER.debug(f"Login try for user {login_data['user_name']}")
    login_user = None
    login_user_name = login_data['user_name']
    login_password = login_data['password']
    correct = False
    try:
        login_user = user_manager.get_user_by_name(login_user_name)
        auth_method = user_manager.get_authentication_provider(login_user.get_authenticator())
        correct = auth_method.authenticate(
            user=login_user,
            password=login_password
        )
    except CMDBError as e:
        abort(401, e)
    if correct:
        login_user.token = get_security_manager(get_pre_init_database()).encrypt_token(login_user)
        return make_response(login_user)
    abort(401)
