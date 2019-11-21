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

            if event_type == "cmdb.exportd.run_manual" and event_param_id == q.argument[0].get_param("id"):
                scheduler.cancel(q)

            elif "cmdb.core.object" in event_type:
                if event_param_type_id == q.argument[0].get_param("type_id"):
                    scheduler.cancel(q)

            elif "cmdb.exportd" in event.get_type():
                if event_param_id == q.argument[0].get_param("id"):
                    if "cmdb.exportd.deleted" == event_type:
                        scheduler.cancel(q)

                    elif event_param_state:
                        scheduler.cancel(q)

        if "cmdb.exportd.added" == event_type or "cmdb.exportd.updated" == event_type:
            if event_param_state:
                scheduler.enter(20, 1, self.start_thread, argument=(event,))

        elif "cmdb.exportd.deleted" != event_type and "cmdb.core.object.deleted" != event_type:
            scheduler.enter(10, 1, self.start_thread, argument=(event, ))

    @staticmethod
    def start_thread(event):
        event_type = event.get_type()
        # start new threads
        if event_type == "cmdb.exportd.run_manual":
            new_thread = ExportdThread(event.get_param("id"))
            new_thread.start()

        elif "cmdb.core.object" in event_type:
            new_thread = ExportdEventThread(event.get_param("type_id"))
            new_thread.start()

        elif "cmdb.exportd" in event_type:
            new_thread = ExportdThread(event.get_param("id"))
            new_thread.start()


class ExportdEventThread(Thread):

    def __init__(self, type_id):
        super(ExportdEventThread, self).__init__()
        self.type_id = type_id

    def run(self):
        for obj in exportd_job_manager.get_job_by_event_based(True):
            if next((item for item in obj.get_sources() if item["type_id"] == self.type_id), None):
                if obj.get_active() and obj.scheduling["event"]["active"]:
                    job = cmdb.exportd.exporter_base.ExportJob(obj)
                    job.execute()


class ExportdThread(Thread):

    def __init__(self, job_id):
        super(ExportdThread, self).__init__()
        self.job_id = job_id

    def run(self):
        obj = exportd_job_manager.get_job(self.job_id)

        # set job is running for UI
        obj.running = True
        obj.last_execute_date = datetime.utcnow()
        exportd_job_manager.update_job(obj)

        # execute Exportd job
        job = cmdb.exportd.exporter_base.ExportJob(obj)
        job.execute()

        # set job is running for UI
        obj.running = False
        exportd_job_manager.update_job(obj)

