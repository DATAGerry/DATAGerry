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
import json
import logging

from flask import abort, request, current_app

from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.route_utils import make_response, insert_request_user

from cmdb.user_management import UserModel

from cmdb.framework import CmdbSectionTemplate
from cmdb.framework.cmdb_section_template_manager import CmdbSectionTemplateManager
from cmdb.security.acl.permission import AccessControlPermission
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

section_template_blueprint = APIBlueprint('section_templates', __name__)

section_templates_manager = CmdbSectionTemplateManager(current_app.database_manager, current_app.event_queue)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@section_template_blueprint.route('/', methods=['POST'])
@section_template_blueprint.protect(auth=True, right='base.framework.type.edit')
@section_template_blueprint.parse_location_parameters()
@insert_request_user
def create_section_template(params: dict, request_user: UserModel):
    """
    Creates a section template in the database

    Args:
        params (dict): section template parameters
        request_user (UserModel): User requesting the creation of a section template

    Returns:
        int: public_id of the created section template
    """
    try:
        params['public_id'] = section_templates_manager.get_new_id(CmdbSectionTemplate.COLLECTION)
        params['is_global'] = params['is_global'] in ('true', 'True')
        params['fields'] = json.loads(params['fields'])
        params['type'] = 'section'

        created_section_template_id = section_templates_manager.insert_section_template(
                                                                    params,
                                                                    request_user,
                                                                    AccessControlPermission.CREATE
                                                                )
    except Exception:
        LOGGER.info("Exception in section_template_create")

    return make_response(created_section_template_id)
