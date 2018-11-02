import importlib
import types
from cmdb.utils import get_logger
from cmdb.utils.error import CMDBError

CMDB_LOGGER = get_logger()

POSSIBLE_PLUGIN_TYPES = [
    'auth'
]


class PluginModuleBase:
    DEFAULT_MODULE_FILE = '__init__.py'

    def __init__(self, package, include_paths=None, default_file=DEFAULT_MODULE_FILE):
        self.package = package
        self.include_paths = include_paths or []
        self.plugins = []
        self.default_file = default_file
        try:
            self.main_module = importlib.import_module(self.package, self.default_file)
            importlib.invalidate_caches()
            self.plugin_loader = PluginLoader(self.main_module, self.package, self.include_paths)
            self.plugins = self.plugin_loader.load_plugins()
        except ImportError:
            raise PluginNotLoadedError(self.package)

    def get_main_module(self):
        return self.main_module

    def get_plugins(self):
        return self.plugins


class PluginManager:

    def __init__(self, single_init: PluginModuleBase = None):
        self.plugin_base_folder = 'cmdb/plugins/'
        self.base_list = []
        if single_init:
            self.base_list.append(single_init)
        else:
            self._init_module_bases()
        self._add_to_sys_path()

    def _init_module_bases(self):
        """TODO: Add other modules"""
        self.base_list.append(PluginModuleBase('cmdb.plugins.auth'))

    def _add_to_sys_path(self):
        """TODO Fixing"""
        for mod_base in self.base_list:
            for plugin in mod_base.plugins:
                CMDB_LOGGER.debug(plugin)
                # sys.path.insert(0, "path/pythonfiles")


class PluginLoader:

    def __init__(self, main_module: types.ModuleType, package, include_paths: list=[]):
        """TODO: Fixing Include Paths"""
        self.main_module = main_module
        self.package = package
        self.include_paths = include_paths

    def load_plugins(self):
        import pkgutil
        plugin_list = []
        for (module_loader, name, ispkg) in pkgutil.iter_modules([self.main_module.__path__[0]]):
            #plugin_list.append(importlib.import_module('.' + name, self.package))
            plugin_list.append(self.package)
            importlib.invalidate_caches()
        return plugin_list


class PluginBase:

    def __init__(self, plugin_name, plugin_type):
        self.plugin_name = plugin_name
        self.plugin_type = plugin_type

    @property
    def plugin_type(self) -> str:
        return self._plugin_type

    @plugin_type.setter
    def plugin_type(self, pos_type: str):
        if pos_type not in POSSIBLE_PLUGIN_TYPES:
            raise ValueError
        self._plugin_type = pos_type


class PluginNotLoadedError(CMDBError):

    def __init__(self, plugin_type):
        self.msg = 'Plugin of type {} could not be loaded'.format(plugin_type)
