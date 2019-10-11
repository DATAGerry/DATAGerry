# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import importlib
import types
from cmdb.utils.error import CMDBError

LOGGER = logging.getLogger(__name__)

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

    def __init__(self, base_folder='/cmdb/plugins/'):
        self.plugin_base_folder = base_folder
        self.base_list = {}
        self._init_module_bases()

    def _init_module_bases(self):
        self.base_list.update({'auth': PluginModuleBase('cmdb.plugins.auth')})

    def get_base(self, name) -> PluginModuleBase:
        return self.base_list[name]


class PluginLoader:

    def __init__(self, main_module: types.ModuleType, package, include_paths: list = None):
        self.main_module = main_module
        self.package = package
        self.include_paths = include_paths or []

    def load_plugins(self):
        import pkgutil
        plugin_list = []
        for (module_loader, name, ispkg) in pkgutil.iter_modules([self.main_module.__path__[0]]):
            plugin_list.append(importlib.import_module('.' + name, self.package))
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
