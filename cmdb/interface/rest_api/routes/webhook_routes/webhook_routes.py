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
"""
TODO: document
"""
import logging
from ast import literal_eval
from flask import abort

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.webhooks_manager import WebhooksManager

from cmdb.models.user_model.user import UserModel
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.route_utils import insert_request_user
from cmdb.interface.rest_api.responses import DefaultResponse

from cmdb.errors.manager import (
    ManagerInsertError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

webhook_blueprint = APIBlueprint('webhooks', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@webhook_blueprint.route('/', methods=['POST'])
@webhook_blueprint.parse_request_parameters()
@insert_request_user
def create_report(params: dict, request_user: UserModel):
    """
    Creates a CmdbReport in the database

    Args:
        params (dict): CmdbReport parameters
    Returns:
        int: public_id of the created CmdbReport
    """
    # reports_manager: WebhooksManager = ManagerProvider.get_manager(ManagerType.WEBHOOKS_MANAGER, request_user)

    # try:
    #     params['public_id'] = reports_manager.get_next_public_id()
    #     params['report_category_id'] = int(params['report_category_id'])
    #     params['type_id'] = int(params['type_id'])
    #     params['predefined'] = params['predefined'] in ["True", "true"]
    #     params['conditions'] = literal_eval(params['conditions'])
    #     params['selected_fields'] = literal_eval(params['selected_fields'])

    #     new_report_id = reports_manager.insert_report(params)
    # except ManagerInsertError as err:
    #     #TODO: ERROR-FIX
    #     LOGGER.debug("[create_report] ManagerInsertError: %s", err.message)
    #     return abort(400, "Could not create the report!")
    # except Exception as err:
    #     LOGGER.debug("[create_report] Exception: %s, Type: %s", err, type(err))

    # api_response = DefaultResponse(new_report_id)

    # return api_response.make_response()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #
