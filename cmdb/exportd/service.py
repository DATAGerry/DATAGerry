import cmdb.process_management.service
import cmdb.exportd.exporter_base
from cmdb.utils import get_logger

LOGGER = get_logger()

class ExportdService(cmdb.process_management.service.AbstractCmdbService):

    def __init__(self):
        super(ExportdService, self).__init__()
        self._name = "exportd"
        self._eventtypes = ["cmdb.core.object.#", "cmdb.exportd.#"]

    def _run(self):
        pass

    def _handle_event(self, event):
        event_type = event.get_type()
        if event_type == "cmdb.core.object.listed":
            self.__schedule_job()

    def __schedule_job(self):
        # ToDo: schedule job only and handle execution in _run() (own thread)
        job = cmdb.exportd.exporter_base.ExportJob()
        job.execute()
