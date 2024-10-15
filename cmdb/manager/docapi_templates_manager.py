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
This DocapiTemplatesManager handles the DocAPI interface to the database
"""
import logging
from queue import Queue
from typing import Union
from datetime import datetime, timezone

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.base_manager import BaseManager

from cmdb.event_management.event import Event
from cmdb.manager.query_builder.base_query_builder import BaseQueryBuilder
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.docapi.docapi_template.docapi_template import DocapiTemplate
from cmdb.user_management.models.user import UserModel
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import ManagerIterationError
from cmdb.errors.docapi import DocapiGetError, DocapiInsertError, DocapiUpdateError, DocapiDeleteError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 DocapiManager - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class DocapiTemplatesManager(BaseManager):
    """
    This DocapiTemplatesManager handles the DocAPI interface to the database
    """
    def __init__(self, dbm: MongoDatabaseManager, event_queue: Union[Queue, Event] = None, database:str = None):
        """
        Set the database connection and the queue for sending events

        Args:
            dbm (DatabaseManagerMongo): Database connection
            event_queue (Queue, Event): The queue for events in RabbitMQ
            database (str): name of database for cloud mode
        """
        self.event_queue = event_queue
        self.query_builder = BaseQueryBuilder()

        if database:
            dbm.connector.set_database(database)

        super().__init__(DocapiTemplate.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_template(self, data: Union[DocapiTemplate, dict]) -> int:
        """
        Insert new DocapiTemplate Object
        Args:
            data: init data
        Returns:
            Public ID of the new DocapiTemplate in database
        """
        if isinstance(data, dict):
            try:
                new_object = DocapiTemplate(**data)
            except Exception as err:
                #TODO: ERROR-FIX
                raise DocapiInsertError(str(err)) from err
        else:
            new_object = data

        try:
            ack = self.insert(new_object.to_database())
        except Exception as err:
            #TODO: ERROR-FIX
            raise DocapiInsertError(str(err)) from err
        try:
            if self.event_queue:
                event = Event("cmdb.docapi.added", {"id": new_object.get_public_id(),
                                                    "active": new_object.get_active(),
                                                    "user_id": new_object.get_author_id()})
                self.event_queue.put(event)
        except Exception as err:
            #TODO: ERROR-FIX
            raise DocapiInsertError(str(err)) from err

        return ack

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_new_docapi_public_id(self) -> int:
        """
        Gets the next couter for the public_id from database and increases it

        Returns:
            int: The next public_id for DocapiTemplate
        """
        return self.get_next_public_id()


    def get_template(self, public_id: int) -> DocapiTemplate:
        """TODO: document"""
        try:
            result = self.get_one(public_id)
        except Exception as err:
            #TODO: ERROR-FIX
            raise DocapiGetError(str(err)) from err

        return DocapiTemplate(**result)


    def get_templates(self, builder_params: BuilderParameters) -> IterationResult[DocapiTemplate]:
        """TODO: document"""
        try:
            query: list[dict] = self.query_builder.build(builder_params)
            count_query: list[dict] = self.query_builder.count(builder_params.get_criteria())

            aggregation_result = list(self.aggregate(query))
            total_cursor = self.aggregate(count_query)
            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']
        except Exception as err:
            raise ManagerIterationError(err) from err

        iteration_result: IterationResult[DocapiTemplate] = IterationResult(aggregation_result, total)
        iteration_result.convert_to(DocapiTemplate)

        return iteration_result


    def get_templates_by(self, **requirements):
        """TODO: document"""
        try:
            ack = []
            templates = self.get_many(**requirements)

            for template in templates:
                ack.append(DocapiTemplate(**template))

            return ack
        except Exception as err:
            #TODO: ERROR-FIX
            raise DocapiGetError(str(err)) from err


    def get_template_by_name(self, **requirements) -> DocapiTemplate:
        """TODO: document"""
        try:
            templates = self.get_many(collection=DocapiTemplate.COLLECTION, limit=1, **requirements)

            if len(templates) > 0:
                return DocapiTemplate(**templates[0])

            if not len(templates) == 0:
                raise DocapiGetError('More than 1 type matches this requirement')
        except Exception as err:
            #TODO: ERROR-FIX
            raise DocapiGetError(str(err)) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_template(self, data: Union[DocapiTemplate, dict], request_user: UserModel) -> str:
        """
        Update new DocapiTemplat Object
        Args:
            data: init data
            request_user: current user, to detect who triggered event
        Returns:
            Public ID of the DocapiTemplate in database
        """
        if isinstance(data, dict):
            update_object = DocapiTemplate(**data)
        elif isinstance(data, DocapiTemplate):
            update_object = data
        else:
            #TODO: ERROR-FIX
            raise DocapiUpdateError(f'Could not update template with ID: {data.get_public_id()}')

        update_object.last_execute_date = datetime.now(timezone.utc)

        ack = self.update(
                criteria={'public_id':update_object.get_public_id()},
                data=update_object.to_database()
              )

        try:
            if self.event_queue:
                event = Event("cmdb.docapi.updated", {"id": update_object.get_public_id(),
                                                    "active": update_object.get_active(),
                                                    "user_id": request_user.get_public_id()})
                self.event_queue.put(event)
        except Exception as err:
            LOGGER.debug("Event Error: %s, Type: %s", err, type(err))

        return ack.acknowledged

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_template(self, public_id: int, request_user: UserModel) -> bool:
        """TODO: document"""
        try:
            ack = self.delete({'public_id': public_id})
        except Exception as err:
            raise DocapiDeleteError(f'Could not delete template with ID: {public_id}') from err

        try:
            if self.event_queue:
                event = Event("cmdb.docapi.deleted", {"id": public_id, "active": False,
                                                    "user_id": request_user.get_public_id()})
                self.event_queue.put(event)
        except Exception:
            LOGGER.debug("Event Error: %s, Type: %s", err, type(err))

        return ack
