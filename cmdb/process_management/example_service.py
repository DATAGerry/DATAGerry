import time
import cmdb.process_management.service

class ExampleService(cmdb.process_management.service.AbstractCmdbService):

    def __init__(self):
        super(ExampleService, self).__init__()
        self._name = "service1"
        self._eventtypes = ["cmdb.core.#", "cmdb.service1.#"]
    
    def _run(self):
        print("{}: start run".format(self._name))
        while not self._event_shutdown.is_set():
            time.sleep(10)
        print("{}: end run".format(self._name))

    def _handle_event(self, event):
        print("{}: event received: {}".format(self._name, event))
