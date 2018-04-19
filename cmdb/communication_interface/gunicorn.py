"""
Server module for web-based services
"""
from gunicorn.app.base import BaseApplication


class HTTPServer(BaseApplication):
    """
    Basic server application
    """
    def __init__(self, app, options=None):
        """
        init server configs
        :param app: app object - default flask instance
        :param options: parameters for app start
        """
        self.options = options or {}
        if 'workers' not in self.options:
            self.options['workers'] = HTTPServer.number_of_workers()
        self.application = app
        super(HTTPServer, self).__init__()

    def init(self, parser, opts, args):
        """
        basic initialisation parser
        :param parser:
        :param opts:
        :param args:
        :return:
        """
        pass

    def load_config(self):
        """
        loading the config into cfg
        :return:
        """
        config = dict([(key, value) for key, value in self.options.items() if key in self.cfg.settings and value is not None])
        print(config)
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        """
        loads set application
        :return: application instance
        """
        return self.application

    @staticmethod
    def number_of_workers():
        """
        calculate number of workers based on cpu count
        :return:
        """
        import multiprocessing
        return (multiprocessing.cpu_count() * 2) + 1
