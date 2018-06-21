"""
Server module for web-based services
"""
from gunicorn.app.base import BaseApplication
from cmdb.application_utils.logger import DEFAULT_LOG_DIR, DEFAULT_FILE_EXTENSION


class HTTPServer(BaseApplication):
    """Basic server application"""

    CONFIG_DEFAULTS = dict(
        version=1,
        disable_existing_loggers=False,

        loggers={
            "gunicorn.error": {
                "level": "INFO",
                "handlers": ["error"],
                "propagate": True,
                "qualname": "gunicorn.error"
            },

            "gunicorn.access": {
                "level": "INFO",
                "handlers": ["access"],
                "propagate": True,
                "qualname": "gunicorn.access"
            }
        },
        handlers={
            "error": {
                "class": "logging.FileHandler",
                "formatter": "generic",
                "filename": DEFAULT_LOG_DIR + "webserver.error" + DEFAULT_FILE_EXTENSION
            },
            "access": {
                "class": "logging.FileHandler",
                "formatter": "generic",
                "filename": DEFAULT_LOG_DIR + "webserver.access" + DEFAULT_FILE_EXTENSION
            }
        },
        formatters={
            "generic": {
                "format": "[%(asctime)s] [%(levelname)-8s] --- %(message)s (%(filename)s)",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "class": "logging.Formatter"
            }
        }
    )

    def __init__(self, app, options=None):
        self.options = options or {}
        if 'host' in self.options and 'port' in self.options:
            self.options['bind'] = '%s:%s' % (self.options['host'], self.options['port'])
        if 'workers' not in self.options:
            self.options['workers'] = HTTPServer.number_of_workers()
        if 'worker_class' not in self.options:
            self.options['worker_class'] = 'gevent'
        self.options['logconfig_dict'] = HTTPServer.CONFIG_DEFAULTS
        #self.options['reload'] = True

        self.application = app
        super(HTTPServer, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in self.options.items()
                       if key in self.cfg.settings and value is not None])
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

    @staticmethod
    def number_of_workers() -> int:
        """calculate number of workers based on cpu

        Returns: number of workers

        """

        import multiprocessing
        return (multiprocessing.cpu_count() * 2) + 1


class DispatcherMiddleware:

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
            path_info = '/%s%s' % (last_item, path_info)
        else:
            app = self.mounts.get(script, self.app)
        original_script_name = environ.get('SCRIPT_NAME', '')
        environ['SCRIPT_NAME'] = original_script_name + script
        environ['PATH_INFO'] = path_info
        return app(environ, start_response)


