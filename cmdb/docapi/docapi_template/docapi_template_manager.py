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
"""TODO: document"""
import logging
from typing import Union
from datetime import datetime, timezone

from cmdb.event_management.event import Event
from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.framework.cmdb_base import CmdbManagerBase
from cmdb.manager.managers import ManagerQueryBuilder
from cmdb.framework.results import IterationResult
from cmdb.manager import ManagerIterationError
from cmdb.search import Pipeline
from cmdb.user_management import UserModel
from cmdb.docapi.docapi_template.docapi_template import DocapiTemplate

from cmdb.errors.docapi import DocapiGetError, DocapiInsertError, DocapiUpdateError, DocapiDeleteError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class DocapiTemplateManager(CmdbManagerBase):
    """TODO: document"""
    def __init__(self, database_manager: DatabaseManagerMongo, event_queue=None):
        self.dbm = database_manager
        self.builder = ManagerQueryBuilder()
        self.collection = DocapiTemplate.COLLECTION
        self._event_queue = event_queue
        super().__init__(database_manager)


    def get_new_id(self) -> int:
        """TODO: document"""
        return self.dbm.get_next_public_id(DocapiTemplate.COLLECTION)


    def get_template(self, public_id: int) -> DocapiTemplate:
        """TODO: document"""
        try:
            result = self.dbm.find_one(collection=DocapiTemplate.COLLECTION, public_id=public_id)
        except Exception as err:
            LOGGER.debug("DocapiGetError: %s", err)
            raise DocapiGetError(err) from err
        return DocapiTemplate(**result)


    def get_templates(self,
                      filter: dict,
                      limit: int,
                      skip: int,
                      sort: str,
                      order: int,
                      *args,
                      **kwargs) -> IterationResult[DocapiTemplate]:
        """TODO: document"""
        try:
            query: Pipeline = self.builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order)
            count_query: Pipeline = self.builder.count(filter=filter)
            aggregation_result = list(self._aggregate(self.collection, query))
            total_cursor = self._aggregate(self.collection, count_query)
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
            templates = self._get_many(collection=DocapiTemplate.COLLECTION, limit=0, **requirements)
            for template in templates:
                ack.append(DocapiTemplate(**template))
            return ack
        except Exception as err:
            LOGGER.debug("DocapiGetError: %s", err)
            raise DocapiGetError(err) from err


    def get_template_by_name(self, **requirements) -> DocapiTemplate:
        """TODO: document"""
        try:
            templates = self._get_many(collection=DocapiTemplate.COLLECTION, limit=1, **requirements)
            if len(templates) > 0:
                return DocapiTemplate(**templates[0])

            raise DocapiGetError('More than 1 type matches this requirement')
        except Exception as err:
            LOGGER.debug("DocapiGetError: %s", err)
            raise DocapiGetError(err) from err


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
                LOGGER.debug("DocapiInsertError: %s", err)
                raise DocapiInsertError(err) from err

        elif isinstance(data, DocapiTemplate):
            new_object = data
        try:
            ack = self.dbm.insert(
                collection=DocapiTemplate.COLLECTION,
                data=new_object.to_database()
            )
            if self._event_queue:
                event = Event("cmdb.docapi.added", {"id": new_object.get_public_id(),
                                                    "active": new_object.get_active(),
                                                    "user_id": new_object.get_author_id()})
                self._event_queue.put(event)
        except Exception as err:
            LOGGER.debug("DocapiInsertError: %s", err)
            raise DocapiInsertError(err) from err
        return ack


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
            raise DocapiUpdateError(f'Could not update template with ID: {data.get_public_id()}')
        update_object.last_execute_date = datetime.now(timezone.utc)
        ack = self._update(
                collection=DocapiTemplate.COLLECTION,
                public_id=update_object.get_public_id(),
                data=update_object.to_database()
            )

        if self._event_queue:
            event = Event("cmdb.docapi.updated", {"id": update_object.get_public_id(),
                                                  "active": update_object.get_active(),
                                                  "user_id": request_user.get_public_id()})
            self._event_queue.put(event)

        return ack.acknowledged


    def delete_template(self, public_id: int, request_user: UserModel) -> bool:
        """TODO: document"""
        try:
            ack = self._delete(collection=DocapiTemplate.COLLECTION, public_id=public_id)
            if self._event_queue:
                event = Event("cmdb.docapi.deleted", {"id": public_id, "active": False,
                                                      "user_id": request_user.get_public_id()})
                self._event_queue.put(event)
            return ack
        except Exception as err:
            LOGGER.debug("DocapiDeleteError: %s", err)
            raise DocapiDeleteError(f'Could not delete template with ID: {public_id}') from err
