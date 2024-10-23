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
"""
Server module for web-based services
"""
import logging
import multiprocessing
from gunicorn.app.base import BaseApplication

from cmdb.database.mongo_database_manager import MongoDatabaseManager

from cmdb import __MODE__, __CLOUD_MODE__
import cmdb.process_management.service
from cmdb.interface.net_app import create_app
from cmdb.interface.docs import create_docs_server
from cmdb.interface.rest_api import create_rest_api
from cmdb.utils.system_config import SystemConfigReader
from cmdb.utils.logger import get_logging_conf
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class WebCmdbService(cmdb.process_management.service.AbstractCmdbService):
    """CmdbService: Webapp"""

    def __init__(self):
        super().__init__()
        self._name = "webapp"
        self._eventtypes = ["cmdb.webapp.#"]
        self._threaded_service = False
        self._multiprocessing = True
        self.__webserver_proc = None


    def _run(self):
        # get queue for sending events
        if __CLOUD_MODE__:
            event_queue = None
        else:
            event_queue = self._event_manager.get_send_queue()

        dbm = MongoDatabaseManager(
            **SystemConfigReader().get_all_values_from_section('Database')
        )


        # get WSGI app
        app = DispatcherMiddleware(
            app=create_app(),
            mounts={
                '/docs': create_docs_server(),
                '/rest': create_rest_api(dbm, event_queue)
            }
        )

        # get gunicorn options
        options = SystemConfigReader().get_all_values_from_section('WebServer')

        # start gunicorn as own process
        webserver = HTTPServer(app, options)
        self.__webserver_proc = multiprocessing.Process(target=webserver.run)
        self.__webserver_proc.start()
        self.__webserver_proc.join()


    def _shutdown(self, signam, frame):
        self.__webserver_proc.terminate()
        self.stop()


    def _handle_event(self, event):
        """ignore incomming events"""


class HTTPServer(BaseApplication):
    """Basic server main_application"""

    def __init__(self, app, options=None):
        self.options = options or {}
        if 'host' in self.options and 'port' in self.options:
            self.options['bind'] = '%s:%s' % (self.options['host'], self.options['port'])
        if 'workers' not in self.options:
            self.options['workers'] = HTTPServer.number_of_workers()
        self.options['worker_class'] = 'sync'
        self.options['disable_existing_loggers'] = False
        self.options['logconfig_dict'] = get_logging_conf()
        self.options['timeout'] = 120
        self.options['daemon'] = True
        if __MODE__ in ('DEBUG','TESTING'):
            self.options['reload'] = True
            self.options['check_config'] = True
            LOGGER.debug("Gunicorn starting with auto reload option")
        LOGGER.info("Interfaces started @ http://%s:%s",self.options['host'], self.options['port'])
        self.application = app
        super().__init__()


    def load_config(self):
        config = dict([(key, value) for key, value in self.options.items()
                       if key in self.cfg.settings and value is not None])
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


    def load(self):
        return self.application


    @staticmethod
    def number_of_workers() -> int:
        """TODO: document"""
        return (multiprocessing.cpu_count() * 2) + 1


class DispatcherMiddleware:
    """TODO: document"""

    def __init__(self, app, mounts=None):
        self.app = app
        self.mounts = mounts or {}


    def __call__(self, environ, start_response):
        script = environ.get('PATH_INFO', '')
        path_info = ''
        while '/' in script:
            if script in self.mounts:
                app = self.mounts[script]
                break
            script, last_item = script.rsplit('/', 1)
            path_info = f'/{last_item}{path_info}'
        else:
            app = self.mounts.get(script, self.app)
        original_script_name = environ.get('SCRIPT_NAME', '')
        environ['SCRIPT_NAME'] = original_script_name + script
        environ['PATH_INFO'] = path_info
        return app(environ, start_response)
