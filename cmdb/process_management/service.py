"""
CmdbService definition

"""
import signal
import sys
import threading
import cmdb.event_management.event_manager
from cmdb.utils import get_logger
LOGGER = get_logger()

class AbstractCmdbService:
    """Abstract definition of a CMDB service

    This abstract CmdbService must be implemented to start a process
    in a CMDB context.
    """

    def __init__(self):
        """Create a new instance"""
        # service name
        self._name = "abstract-service"
        # define event types for subscription
        self._eventtypes = ["cmdb.#"]
        # boolean: execute _run() method as own thread
        self._threaded_service = True
        # boolean: multiprocessing service
        self._multiprocessing = False

        # init variables
        self._event_shutdown = None
        self._event_manager = None
        self._thread_service = None

    def start(self):
        """service start"""
        LOGGER.info("start {} ...".format(self._name))

        # init shutdown handling
        self._event_shutdown = threading.Event()
        signal.signal(signal.SIGTERM, self._shutdown)

        # start event manager
        self._event_manager = cmdb.event_management.event_manager.EventManagerAmqp(self._event_shutdown,
                                                                                   self._handle_event,
                                                                                   self._name,
                                                                                   self._eventtypes,
                                                                                   self._multiprocessing)

        if self._threaded_service:
            # start daemon logic in own thread
            self._thread_service = threading.Thread(target=self._run, daemon=False)
            self._thread_service.start()
        else:
            self._run()

        # wait for shutdown, if daemon logic was terminated
        self._event_shutdown.wait()

        # shutdown daemon explicitly, if shutdown event was set
        self._shutdown(None, None)

    def _run(self):
        """daemon action - to be implemented
        implemented action must check the self._even_shutdown flag for termination
        """
        pass

    def _shutdown(self, signam, frame):
        """shutdown handler"""
        self.stop()

    def stop(self):
        """stop the service"""
        LOGGER.info("shutdown {} ...".format(self._name))
        # set shutdown event
        self._event_shutdown.set()
        # shutdown EventManager
        self._event_manager.shutdown()
        # wait for termination of service thread (max 5sec)
        if self._threaded_service and self._thread_service:
            LOGGER.debug("wait for termination of service thread")
            self._thread_service.join(5)
            LOGGER.debug("service thread terminated")
        # exit process
        LOGGER.info("shutdown {} completed".format(self._name))
        sys.exit(0)

    def _handle_event(self, event):
        """action for handling events

        this should only be a short running function
        long running jobs should be started and handled by the _run() function
        """
        pass
