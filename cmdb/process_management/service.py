import signal
import sys
import threading
import time
import cmdb.event_management.event_manager

class AbstractCmdbService:

    def __init__(self):
        # service name
        self._name = "abstract-service"
        # define event types for subscription
        self._eventypes = ["cmdb.#"]
        # boolean: execute _run() method as own thread
        self._threaded_service = True
        
    def start(self):
        # init shutdown handling
        self._event_shutdown = threading.Event()
        signal.signal(signal.SIGTERM, self._shutdown)

        # start event manager
        self._event_manager = cmdb.event_management.event_manager.EventManagerAmqp(self._event_shutdown, self._handle_event, self._name, self._eventtypes)

        if self._threaded_service:
            # start daemon logic in own thread
            self._thread_service = threading.Thread(target=self._run, daemon=False)
            self._thread_service.start()
        else:
            self._run()

        # wait for shutdown, if daemon logic was terminated
        self._event_shutdown.wait()

    def _run(self):
        # daemon action - to be implemented
        # implemented action must check the self._even_shutdown flag for termination
        pass

    def _shutdown(self, signam, frame):
        self.stop()

    def stop(self):
        print("shutdown {} ...".format(self._name))
        # set shutdown event
        self._event_shutdown.set()
        # shutdown EventManager
        self._event_manager.shutdown()
        # wait for termination of service thread (max 5sec)
        if self._thread_service:
            print("wait for termination of service thread")
            self._thread_service.join(5)
            print("service thread terminated")
        # exit process
        sys.exit(0)

    def _handle_event(self, event):
        # action for handling events
        # this should only be a short running function
        # long running jobs should be started and handled by the _run() function
        pass
