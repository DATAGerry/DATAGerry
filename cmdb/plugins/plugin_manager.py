import os
from cmdb.application_utils.logger import create_module_logger
logger = create_module_logger(__name__)


class PluginManager:

    PLUGIN_PATH = os.path.dirname(os.path.realpath(__file__))+'/'
    PLUGIN_DIRECTORIES = [
        'auth'
    ]

    def __init__(self, plugin_path=None, plugin_directories=None):
        self.plugin_path = plugin_path or self.PLUGIN_PATH
        self.plugin_directories = plugin_directories or self.PLUGIN_DIRECTORIES
        try:
            self.check_path_sets()
        except DefaultPluginDirsNotFound as e:
            logger.warning(e.message)

    def check_path_sets(self):
        error_list = []
        for pdir in self.plugin_directories:
            if not os.path.isdir(self.plugin_path+pdir) or not os.path.exists(self.plugin_path+pdir):
                error_list.append(pdir)
                self.plugin_directories.remove(pdir)
        if len(error_list) > 0:
            raise DefaultPluginDirsNotFound(error_list, self.plugin_path)

    def load_plugins(self):
        for plugin in self.plugin_directories:
            print(plugin)

    def import_module(self, module):
        import importlib
        importlib.import_module()

    def __repr__(self):
        from cmdb.application_utils.program_utils import debug_print
        return debug_print(self)


class DefaultPluginDirsNotFound(Exception):

    def __init__(self, plugin_names, path):
        self.message = 'The default plugin directories {} in {} were not found or a directory'.format(plugin_names, path)
