# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
"""
Process Manager
Manager for handling CMDB processes
"""
import logging
import multiprocessing
import threading
from cmdb.utils.helpers import load_class
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class ProcessManager:
    """Handling CMDB processes

    The CMDB app consists of multiple processes (e.g. webapp, syncd).
    The process managers starts and stops theses processes in the
    correct order.
    """

    def __init__(self):
        """Create a new instance of the ProcessManager"""
        # service definitions (in correct order)
        self.__service_defs = []
        self.__service_defs.append(CmdbProcess("exportd", "cmdb.exportd.service.ExportdService"))
        self.__service_defs.append(CmdbProcess("webapp", "cmdb.interface.gunicorn.WebCmdbService"))

        # processlist
        self.__process_list = []

        # process controller
        self.__process_controllers = []

        # shutdown flag
        self.__flag_shutdown = threading.Event()
        self._loaded = False



    def start_app(self) -> bool:
        """start all services from service definitions"""
        for service_def in self.__service_defs:
            service_name = service_def.get_name()
            service_class = load_class(service_def.get_class())
            process = multiprocessing.Process(target=service_class().start, name=service_name)
            process.start()
            self.__process_list.append(process)
            # start process controller
            proc_controller = ProcessController(process, self.__flag_shutdown, self.stop_app)
            proc_controller.start()
            self.__process_controllers.append(proc_controller)
        return True



    def stop_app(self):
        """stop all services"""
        self.__flag_shutdown.set()
        # go through processes in different order
        for process in reversed(self.__process_list):
            process.terminate()



    def get_loading_status(self):
        """TODO: document"""
        return self._loaded


class CmdbProcess:
    """Definition of a CmdbProcess"""

    def __init__(self, name, classname):
        """Create a new instance

        Args:
            name(str): name of the process
            classname(str): classname of the process
        """
        self.__name = name
        self.__classname = classname



    def get_name(self):
        """return the process name

        Returns:
            str: name of the process
        """
        return self.__name



    def get_class(self):
        """return the class name

        Returns:
            str: name of the class
        """
        return self.__classname


class ProcessController(threading.Thread):
    """Controlls the state of a process"""

    def __init__(self, process, flag_shutdown, cb_shutdown):
        """Creates a new instance
        
        Args:
            process(multiprocessingProcess): process to control
            flag_shutdown(threading.Event): shutdown flag
            cb_shutdown(func): callback function if a process crashed
        """
        super().__init__()
        self.__process = process
        self.__flag_shutdown = flag_shutdown
        self.__cb_shutdown = cb_shutdown



    def run(self):
        self.__process.join()
        # terminate app, if process crashed
        if not self.__flag_shutdown.is_set():
            self.__cb_shutdown()
