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
from flask import abort, request

from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.webhooks_event_manager import WebhooksEventManager

from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses import DefaultResponse, GetMultiResponse
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.models.user_model.user import UserModel
from cmdb.models.webhook_model.cmdb_webhook_event_model import CmdbWebhookEvent
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import (
    ManagerGetError,
    ManagerDeleteError,
    ManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

webhook_event_blueprint = APIBlueprint('webhook_events', __name__)

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@webhook_event_blueprint.route('/<int:public_id>', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_webhook_event(public_id: int, request_user: UserModel):
    """
    Retrieves the CmdbWebhookEvent with the given public_id
    
    Args:
        public_id (int): public_id of CmdbWebhookEvent which should be retrieved
        request_user (UserModel): User which is requesting the CmdbWebhookEvent
    """
    webhook_events_manager: WebhooksEventManager = ManagerProvider.get_manager(ManagerType.WEBHOOKS_EVENT_MANAGER,
                                                                               request_user)

    try:
        requested_webhook_event = webhook_events_manager.get_webhook_event(public_id)
    except ManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_webhook_event] ManagerGetError: %s", err.message)
        return abort(400, f"Could not retrieve Webhook Event with ID: {public_id}!")

    api_response = DefaultResponse(requested_webhook_event)

    return api_response.make_response()


@webhook_event_blueprint.route('/', methods=['GET', 'HEAD'])
@webhook_event_blueprint.parse_collection_parameters()
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_webhook_events(params: CollectionParameters, request_user: UserModel):
    """
    Returns all CmdbWebhookEvents based on the params

    Args:
        params (CollectionParameters): Parameters to identify documents in database
    Returns:
        (GetMultiResponse): All CmdbWebhookEvents considering the params
    """
    webhook_events_manager: WebhooksEventManager = ManagerProvider.get_manager(ManagerType.WEBHOOKS_EVENT_MANAGER,
                                                                               request_user)

    try:
        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbWebhookEvent] = webhook_events_manager.iterate(builder_params)
        webhook_event_list: list[dict] = [webhook_event_.__dict__ for webhook_event_ in iteration_result.results]

        api_response = GetMultiResponse(webhook_event_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        request.method == 'HEAD')
    except ManagerIterationError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_webhook_events] ManagerIterationError: %s", err.message)
        return abort(400, "Could not retrieve Webhook Events!")

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@webhook_event_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def delete_webhook_event(public_id: int, request_user: UserModel):
    """
    Deletes the CmdbWebhookEvent with the given public_id
    
    Args:
        public_id (int): public_id of CmdbWebhookEvent which should be retrieved
        request_user (UserModel): User which is requesting the CmdbWebhookEvent
    """
    webhook_events_manager: WebhooksEventManager = ManagerProvider.get_manager(ManagerType.WEBHOOKS_EVENT_MANAGER,
                                                                               request_user)

    try:
        webhook_event_instance: CmdbWebhookEvent = webhook_events_manager.get_webhook_event(public_id)

        if not webhook_event_instance:
            return abort(400, f"Could not retrieve Webhook with ID: {public_id}!")

        #TODO: REFACTOR-FIX
        ack: bool = webhook_events_manager.delete({'public_id':public_id})
    except ManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[delete_webhook_event] ManagerGetError: %s", err.message)
        return abort(400, f"Could not retrieve Webhook Event with ID: {public_id}!")
    except ManagerDeleteError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[delete_webhook_event] ManagerDeleteError: %s", err)
        return abort(400, f"Could not delete Webhook Event with ID: {public_id}!")

    api_response = DefaultResponse(ack)

    return api_response.make_response()
