# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
"""
Definition of all routes for section templates
"""
import logging

from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.route_utils import make_response, insert_request_user

from cmdb.user_management import UserModel
# -------------------------------------------------------------------------------------------------------------------- #


LOGGER = logging.getLogger(__name__)
section_template_blueprint = APIBlueprint('section_templates', __name__)



# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@section_template_blueprint.route('/', methods=['POST'])
@section_template_blueprint.protect(auth=True, right='base.framework.type.edit')
@insert_request_user
def create_location(params: dict, request_user: UserModel):
    """
    Creates a section template in the database

    Args:
        params (dict): section template parameters
        request_user (UserModel): User requesting the creation of a section template

    Returns:
        int: public_id of the created section template
    """
    return make_response(True)
