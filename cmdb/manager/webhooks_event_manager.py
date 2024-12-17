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
This module contains the implementation of the WebhooksEventManager
"""
import logging

from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.base_manager import BaseManager

from cmdb.models.webhook_model.cmdb_webhook_event_model import CmdbWebhookEvent
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import ManagerInsertError, ManagerGetError, ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                WebhooksManager - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class WebhooksEventManager(BaseManager):
    """
    The WebhooksEventManager handles the interaction between the Webhooks-API and the database
    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, database:str = None):
        """
        Set the database connection and the queue for sending events

        Args:
            dbm (MongoDatabaseManager): Database connection
        """
        if database:
            dbm.connector.set_database(database)

        super().__init__(CmdbWebhookEvent.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #


    def insert_webhook_event(self, data: dict) -> int:
        """
        Inserts a single CmdbWebhookEvent in the database

        Args:
            data (dict): Data of the new CmdbWebhookEvent

        Returns:
            int: public_id of the newly created CmdbWebhookEvent
        """
        try:
            new_webhook_event = CmdbWebhookEvent(**data)
        except Exception as err:
            #TODO: ERROR-FIX
            raise ManagerInsertError(err) from err

        try:
            ack = self.insert(new_webhook_event.__dict__)
            #TODO: ERROR-FIX
        except Exception as err:
            raise ManagerInsertError(err) from err

        return ack

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_webhook_event(self, public_id: int) -> CmdbWebhookEvent:
        """
        Retrives a CmdbWebhookEvent from the database with the given public_id

        Args:
            public_id (int): public_id of the CmdbWebhookEvent which should be retrieved
        Raises:
            ManagerGetError: Raised if the CmdbWebhookEvent could not be retrieved
        Returns:
            CmdbWebhookEvent: The requested CmdbWebhookEvent if it exists, else None
        """
        try:
            requested_webhook_event = self.get_one(public_id)
        except Exception as err:
            #TODO: ERROR-FIX
            raise ManagerGetError(f"Webhook with ID: {public_id}! 'GET' Error: {err}") from err

        if requested_webhook_event:
            requested_webhook_event = CmdbWebhookEvent.from_data(requested_webhook_event)

            return requested_webhook_event

        #TODO: ERROR-FIX
        raise ManagerGetError(f'Webhook with ID: {public_id} not found!')


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[CmdbWebhookEvent]:
        """
        Performs an aggregation on the database

        Args:
            builder_params (BuilderParameters): Contains input to identify the target of action
            user (UserModel, optional): User requesting this action
        Raises:
            ManagerIterationError: Raised when something goes wrong during the aggregate part
            ManagerIterationError: Raised when something goes wrong during the building of the IterationResult
        Returns:
            IterationResult[CmdbWebhookEvent]: Result which matches the Builderparameters
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)
        except ManagerGetError as err:
            #TODO: ERROR-FIX
            raise ManagerIterationError(err) from err

        try:
            iteration_result: IterationResult[CmdbWebhookEvent] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbWebhookEvent)
        except Exception as err:
            #TODO: ERROR-FIX
            raise ManagerIterationError(err) from err

        return iteration_result
