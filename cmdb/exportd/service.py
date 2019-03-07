import logging
import time
import cmdb.process_management.service
import cmdb.exportd.exporter_base

LOGGER = logging.getLogger(__name__)

class ExportdService(cmdb.process_management.service.AbstractCmdbService):

    def __init__(self):
        super(ExportdService, self).__init__()
        self._name = "exportd"
        self._eventtypes = ["cmdb.core.object.#", "cmdb.exportd.#"]

    def _run(self):
        # ToDo: for testing only
        #time.sleep(5)
        #self.__schedule_job()
        pass

    def _handle_event(self, event):
        event_type = event.get_type()
        # ToDo: schedule jobs
        if event_type == "cmdb.core.object.listed":
            self.__schedule_job()

    def __schedule_job(self):
        # ToDo: schedule job only and handle execution in _run() (own thread)
        job = cmdb.exportd.exporter_base.ExportJob()
        job.execute()
