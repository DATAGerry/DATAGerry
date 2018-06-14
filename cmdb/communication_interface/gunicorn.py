"""
Server module for web-based services
"""
from gunicorn.app.base import BaseApplication


class HTTPServer(BaseApplication):
    """Basic server application"""

    def __init__(self, app, options=None):
        self.options = options or {}
        if 'host' in self.options and 'port' in self.options:
            self.options['bind'] = '%s:%s' % (self.options['host'], self.options['port'])
        if 'workers' not in self.options:
            self.options['workers'] = HTTPServer.number_of_workers()
        if 'worker_class' not in self.options:
            self.options['worker_class'] = 'gevent'
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
