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

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.base_manager import BaseManager

from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.event_management.event import Event
from cmdb.exportd.exportd_job.exportd_job import ExportdJob
from cmdb.user_management.models.user import UserModel
from cmdb.framework.results import IterationResult

from cmdb.errors.manager.object_manager import ObjectManagerGetError
from cmdb.errors.manager.exportd_job_manager import ExportdJobManagerDeleteError,\
                                                    ExportdJobManagerUpdateError,\
                                                    ExportdJobManagerInsertError,\
                                                    ExportdJobManagerGetError
from cmdb.errors.manager import ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              ExportdJobsManager - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class ExportdJobsManager(BaseManager):
    """TODO: document"""

    def __init__(self, dbm: MongoDatabaseManager, event_queue=None, database: str = None):
        self.event_queue = event_queue

        if database:
            dbm.connector.set_database(database)

        super().__init__(ExportdJob.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_job(self, data: Union[ExportdJob, dict]) -> int:
        """
        Insert new ExportdJob Object
        Args:
            data: init data
        Returns:
            Public ID of the new ExportdJob in database
        """
        if isinstance(data, dict):
            try:
                new_object = ExportdJob(**data)
            except Exception as err:
                #ERROR-FIX
                raise ExportdJobManagerInsertError(str(err)) from err
        else:
            new_object = data

        try:
            ack = self.insert(new_object.to_database())
        except Exception as err:
            #ERROR-FIX
            raise ExportdJobManagerInsertError(str(err)) from err

        try:
            if self.event_queue:
                state = new_object.scheduling["event"]["active"] and new_object.get_active()
                event = Event("cmdb.exportd.added", {"id": new_object.get_public_id(),
                                                     "active": state,
                                                     "user_id": new_object.get_author_id(),
                                                     "event": 'automatic'})
                self.event_queue.put(event)
        except Exception as err:
            #ERROR-FIX
            LOGGER.debug("RabbitMQ error: %s", str(err))

        return ack

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_job(self, public_id: int) -> ExportdJob:
        """TODO: document"""
        try:
            result = self.get_one(public_id)
        except (ExportdJobManagerGetError, Exception) as err:
            #ERROR-FIX
            LOGGER.error(err)
            raise err

        return ExportdJob(**result)


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[ExportdJob]:
        """
        TODO: document
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            iteration_result: IterationResult[ExportdJob] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(ExportdJob)
        #ERROR-FIX
        except Exception as err:
            #ERROR-FIX
            raise ManagerIterationError(err) from err

        return iteration_result


    def get_all_jobs(self):
        """TODO: document"""
        job_list = []

        for found_job in self.find_all():
            try:
                job_list.append(ExportdJob(**found_job))
            except Exception:
                #ERROR-FIX
                continue

        return job_list


    def get_job_by_args(self, **requirements) -> ExportdJob:
        """TODO: document"""
        try:
            found_type_list = self.get_many(limit=1, **requirements)
            if len(found_type_list) > 0:
                return ExportdJob(**found_type_list[0])

            #ERROR-FIX
            raise ObjectManagerGetError(err='More than 1 type matches this requirement')
        except Exception as err:
            raise ObjectManagerGetError(str(err)) from err


    def get_job_by_event_based(self, state):
        """TODO: document"""
        formatted_filter = {'scheduling.event.active': state}
        job_list = []

        for founded_job in self.find_all(filter=formatted_filter):
            try:
                job_list.append(ExportdJob(**founded_job))
            except Exception:
                #ERROR-FIX
                continue

        return job_list


    def get_new_exportd_job_public_id(self) -> int:
        """
        Gets the next couter for the public_id from database and increases it

        Returns:
            int: The next public_id for ExportdJog
        """
        return self.get_next_public_id()

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_job(self, data: Union[dict, ExportdJob], request_user: UserModel, event_start=True) -> str:
        """
        Update new ExportdJob Object
        Args:
            data: init data
            request_user: current user, to detect who triggered event
            event_start: Controls whether an event should be started
        Returns:
            Public ID of the ExportdJob in database
        """
        if isinstance(data, dict):
            update_object = ExportdJob(**data)
        elif isinstance(data, ExportdJob):
            update_object = data
        else:
            #ERROR-FIX
            raise ExportdJobManagerUpdateError(f'Could not update job with ID: {data.get_public_id()}')

        update_object.last_execute_date = datetime.now(timezone.utc)

        ack = self.update(criteria={'public_id': update_object.get_public_id()}, data=update_object.to_database())

        try:
            if self.event_queue and event_start:
                state = update_object.scheduling["event"]["active"] and update_object.get_active()
                event = Event("cmdb.exportd.updated", {"id": update_object.get_public_id(),
                                                    "active": state,
                                                    "user_id": request_user.get_public_id(),
                                                    "event": 'automatic'})
                self.event_queue.put(event)
        except Exception as err:
            #ERROR-FIX
            LOGGER.debug("RabbitMQ error: %s", str(err))

        return ack.acknowledged

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_job(self, public_id: int, request_user: UserModel) -> bool:
        """TODO: document"""
        try:
            ack = self.delete({'public_id': public_id})
        except Exception as err:
            raise ExportdJobManagerDeleteError(f'Could not delete job with ID: {public_id}. Error: {err}') from err

        try:
            if self.event_queue:
                event = Event("cmdb.exportd.deleted", {"id": public_id, "active": False,
                                                       "user_id": request_user.get_public_id(),
                                                       "event": 'automatic'})
                self.event_queue.put(event)
        except Exception as err:
            #ERROR-FIX
            LOGGER.debug("RabbitMQ error: %s", str(err))

        return ack

# ------------------------------------------------- HELPER FUNCTIONS ------------------------------------------------- #

    def run_job_manual(self, public_id: int, request_user: UserModel) -> bool:
        """TODO: document"""
        try:
            if self.event_queue:
                event = Event("cmdb.exportd.run_manual", {"id": public_id,
                                                        "user_id": request_user.get_public_id(),
                                                        "event": 'manual'})
                self.event_queue.put(event)
        except Exception as err:
            #ERROR-FIX
            LOGGER.debug("RabbitMQ error: %s", str(err))

        return True
