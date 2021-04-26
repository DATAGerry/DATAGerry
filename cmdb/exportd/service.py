# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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

import logging
import cmdb.process_management.service
import cmdb.exportd.exporter_base
import time
import sched

from cmdb.event_management.event import Event
from threading import Thread
from datetime import datetime
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.exportd.exportd_job.exportd_job_manager import ExportdJobManagement
from cmdb.exportd.exportd_job.exportd_job import ExecuteState
from cmdb.database.managers import DatabaseManagerMongo
from cmdb.utils.system_config import SystemConfigReader
from cmdb.exportd.exportd_logs.exportd_log_manager import ExportdLogManager
from cmdb.exportd.exportd_logs.exportd_log_manager import LogManagerInsertError, LogAction, ExportdJobLog
from cmdb.user_management.managers.user_manager import UserManager

LOGGER = logging.getLogger(__name__)
scheduler = sched.scheduler(time.time, time.sleep)


class ExportdService(cmdb.process_management.service.AbstractCmdbService):
    def __init__(self):
        super(ExportdService, self).__init__()
        self._name = "exportd"
        self._eventtypes = ["cmdb.core.object.#",
                            "cmdb.core.objects.#",
                            "cmdb.core.objecttype.#",
                            "cmdb.core.objecttypes.#",
                            "cmdb.exportd.#"]

    def _run(self):
        LOGGER.info("{}: start run".format(self._name))
        while not self._event_shutdown.is_set():
            scheduler.run()
            time.sleep(1)
        LOGGER.info("{}: end run".format(self._name))

    def _handle_event(self, event: Event):
        LOGGER.debug("event received: {}".format(event.get_type()))
        self.handler(event)

    def __schedule_job(self, event: Event):
        pass

    def handler(self, event: Event):
        # get type of Event
        event_type = event.get_type()

        # get public_id from Event
        event_param_id = event.get_param("id")

        # Remove duplicate entries in the Queue of upcoming events
        for q in scheduler.queue:
            arg = q.argument[0]
            if "cmdb.core.object" in event_type and event_param_id == arg.get_param("id"):
                scheduler.cancel(q)

            elif "cmdb.exportd" in event_type and event_param_id == arg.get_param("id"):
                scheduler.cancel(q)

        if event.get_param("active"):
            scheduler.enter(10, 1, self.start_thread, argument=(event,))

        elif "cmdb.exportd.deleted" != event_type:
            scheduler.enter(5, 1, self.start_thread, argument=(event, ))

    @staticmethod
    def start_thread(event: Event):
        event_type = event.get_type()
        # start new threads

        if "cmdb.exportd.run_manual" == event_type:
            new_thread = ExportdThread(event=event, state=True)
            new_thread.start()

        elif "cmdb.core.object" in event_type:
            new_thread = ExportdThread(event=event, state=False)
            new_thread.start()

        elif "cmdb.exportd" in event_type:
            new_thread = ExportdThread(event=event, state=event.get_param("active") in ['true', True])
            new_thread.start()


class ExportdThread(Thread):

    def __init__(self, event: Event, state: bool = False):

        scr = SystemConfigReader()
        database_options = scr.get_all_values_from_section('Database')
        database = DatabaseManagerMongo(**database_options)

        super(ExportdThread, self).__init__()
        self.job = None
        self.job_id = int(event.get_param("id"))
        self.type_id = int(event.get_param("type_id")) if event.get_param("type_id") else None
        self.user_id = int(event.get_param("user_id"))
        self.event = event
        self.is_active = state
        self.exception_handling = None

        self.object_manager = CmdbObjectManager(database_manager=database)
        self.log_manager = ExportdLogManager(database_manager=database)
        self.exportd_job_manager = ExportdJobManagement(database_manager=database)
        self.user_manager = UserManager(database_manager=database)

    def run(self):
        try:
            if self.type_id:
                for obj in self.exportd_job_manager.get_job_by_event_based(True):
                    if next((item for item in obj.get_sources() if item["type_id"] == self.type_id), None):
                        if obj.get_active() and obj.scheduling["event"]["active"]:
                            self.job = obj
                            self.worker()
            elif self.is_active:
                self.job = self.exportd_job_manager.get_job(self.job_id)
                self.worker()
        except Exception as ex:
            LOGGER.error(ex)
            return ex

    def worker(self):
        cur_user = None
        try:
            # update job for UI
            self.job.state = ExecuteState.RUNNING.name
            self.job.last_execute_date = datetime.utcnow()

            # get current user
            cur_user = self.user_manager.get(self.user_id)

            self.exportd_job_manager.update_job(self.job, self.user_manager.get(self.user_id), event_start=False)
            # execute Exportd job
            job = cmdb.exportd.exporter_base.ExportdManagerBase(job=self.job, event=self.event,
                                                                object_manager=self.object_manager,
                                                                log_manager=self.log_manager)
            job.execute(cur_user.get_public_id(), cur_user.get_display_name())

        except Exception as err:
            LOGGER.error(err)
            self.exception_handling = err
            # Generate Error log
            try:
                log_params = {
                    'job_id': self.job.get_public_id(),
                    'state': False,
                    'user_id': cur_user.get_public_id(),
                    'user_name': cur_user.get_display_name(),
                    'event': self.event.get_type(),
                    'message': ['Successful'] if not err else err.args,
                }
                self.log_manager.insert_log(action=LogAction.EXECUTE, log_type=ExportdJobLog.__name__, **log_params)
            except LogManagerInsertError as err:
                LOGGER.error(err)
        finally:
            # update job for UI
            self.job.state = ExecuteState.SUCCESSFUL.name if not self.exception_handling else ExecuteState.FAILED.name
            self.exportd_job_manager.update_job(self.job, self.user_manager.get(self.user_id), event_start=False)



