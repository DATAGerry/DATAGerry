# DATAGERRY - OpenSource Enterprise CMDB
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
import cmdb.process_management.service
import cmdb.exportd.exporter_base
import time
import sched

from threading import Thread
from datetime import datetime
from cmdb.exportd.exportd_job.exportd_job_manager import exportd_job_manager
from cmdb.exportd.exportd_job.exportd_job import ExecuteState
from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.utils.system_reader import SystemConfigReader
from cmdb.exportd.exportd_logs.exportd_log_manager import ExportdLogManager
from cmdb.exportd.exportd_logs.exportd_log_manager import LogManagerInsertError, LogAction, ExportdJobLog
from cmdb.user_management.user_manager import UserManager
from cmdb.utils.security import SecurityManager


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

    def _handle_event(self, event):
        LOGGER.debug("event received: {}".format(event.get_type()))
        self.handler(event)

    def __schedule_job(self, event):
        pass

    def handler(self, event):
        # get type of Event
        event_type = event.get_type()

        # get public_id from Event
        event_param_id = event.get_param("id")

        # get type_id public_id from Event
        event_param_type_id = event.get_param("type_id")

        # get Exportd Job state
        event_param_state = event.get_param("active")

        for q in scheduler.queue:
            if "cmdb.core.object" in event_type and event_param_type_id == q.argument[0].get_param("type_id"):
                scheduler.cancel(q)

            elif "cmdb.exportd" in event.get_type() and event_param_id == q.argument[0].get_param("id"):
                scheduler.cancel(q)

        if event_param_state:
            scheduler.enter(10, 1, self.start_thread, argument=(event,))
        elif "cmdb.exportd.deleted" != event_type and "cmdb.core.object.deleted" != event_type:
            scheduler.enter(5, 1, self.start_thread, argument=(event, ))

    @staticmethod
    def start_thread(event):
        event_type = event.get_type()
        # start new threads

        if "cmdb.exportd.run_manual" == event_type:
            new_thread = ExportdThread(event=event, state=True)
            new_thread.start()

        elif "cmdb.core.object" in event_type:
            new_thread = ExportdThread(event=event, state=False)
            new_thread.start()

        elif "cmdb.exportd" in event_type:
            new_thread = ExportdThread(event=event, state=event.get_param("active"))
            new_thread.start()


class ExportdThread(Thread):

    def __init__(self, event, state=False):
        super(ExportdThread, self).__init__()
        self.job = None
        self.job_id = event.get_param("id")
        self.type_id = event.get_param("type_id")
        self.user_id = event.get_param("user_id")
        self.event = event
        self.is_active = state
        self.exception_handling = None

        scr = SystemConfigReader()
        database_options = scr.get_all_values_from_section('Database')
        self.__dbm = DatabaseManagerMongo(
            **database_options
        )
        self.log_manager = ExportdLogManager(
            database_manager=self.__dbm)
        self.user_manager = UserManager(database_manager=self.__dbm)

    def run(self):
        try:
            if self.type_id:
                for obj in exportd_job_manager.get_job_by_event_based(True):
                    if next((item for item in obj.get_sources() if item["type_id"] == self.type_id), None):
                        if obj.get_active() and obj.scheduling["event"]["active"]:
                            self.job = obj
                            self.worker()
            elif self.is_active:
                self.job = exportd_job_manager.get_job(self.job_id)
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
            cur_user = self.user_manager.get_user(self.user_id)

            exportd_job_manager.update_job(self.job, self.user_manager.get_user(self.user_id), event_start=False)
            # execute Exportd job
            job = cmdb.exportd.exporter_base.ExportdManagerBase(self.job)
            job.execute(self.event, cur_user.get_public_id(), cur_user.get_name())

        except Exception as err:
            LOGGER.error(err)
            self.exception_handling = err
            # Generate Error log
            try:
                log_params = {
                    'job_id': self.job.get_public_id(),
                    'state': False,
                    'user_id': cur_user.get_public_id(),
                    'user_name': cur_user.get_name(),
                    'event': self.event.get_type(),
                    'message': ['Successful'] if not err else err.args,
                }
                self.log_manager.insert_log(action=LogAction.EXECUTE, log_type=ExportdJobLog.__name__, **log_params)
            except LogManagerInsertError as err:
                LOGGER.error(err)
        finally:
            # update job for UI
            self.job.state = ExecuteState.SUCCESSFUL.name if not self.exception_handling else ExecuteState.FAILED.name
            exportd_job_manager.update_job(self.job, self.user_manager.get_user(self.user_id), event_start=False)



