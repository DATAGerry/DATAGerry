# Net|CMDB - OpenSource Enterprise CMDB
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

import pytest
from cmdb.plugins.plugin_system import POSSIBLE_PLUGIN_TYPES, PluginBase, PluginLoader, PluginModuleBase, PluginManager


def test_system_init():
    # just some module init tests
    assert len(POSSIBLE_PLUGIN_TYPES) == 1
    # add plugin type 'example' for later tests
    POSSIBLE_PLUGIN_TYPES.append('example')
    assert len(POSSIBLE_PLUGIN_TYPES) == 2


def test_plugin_loader():
    from types import ModuleType
    from tests.fixtures.plugins.example import example_module_base

    plugin_loader = PluginLoader(example_module_base.main_module, example_module_base.package)
    # should load all plugins inside plugins.example
    loaded_plugins = plugin_loader.load_plugins()
    assert len(loaded_plugins) == 1
    example_plugin = loaded_plugins[0]
    assert type(example_plugin) == ModuleType


def test_plugin_module_base():
    # basic tests
    example_module_base1 = PluginModuleBase(
        package='tests.fixtures.plugins.example'
    )
    assert example_module_base1.package == 'tests.fixtures.plugins.example'
    example_module_base2 = PluginModuleBase(
        package='tests.fixtures.plugins.example',
        include_paths='/tests/fixtures/plugins/example/',
        default_file='test.py'
    )
    assert example_module_base2.default_file == 'test.py'
    assert example_module_base2.include_paths == '/tests/fixtures/plugins/example/'

    # Init tests inside plugin dir
    from tests.fixtures.plugins.example import example_module_base
    assert example_module_base.package == 'tests.fixtures.plugins.example'


def test_plugin_base():
    test_base = PluginBase(plugin_name='example', plugin_type='example')
    assert test_base.plugin_name == 'example'
    assert test_base.plugin_type == 'example'

    with pytest.raises(ValueError):
        PluginBase(plugin_name='example', plugin_type='example2')


def test_plugin():
    from tests.fixtures.plugins.example.test_plugin import TestPlugin

    test_plugin1 = TestPlugin()
    assert test_plugin1.plugin_name == 'Test_Plugin'
    assert test_plugin1.plugin_type == 'example'
    assert test_plugin1.new_function() is True
    assert test_plugin1.parent_function() == test_plugin1.plugin_name
    assert test_plugin1.function_override() is True
    with pytest.raises(NotImplementedError):
        test_plugin1.function_not_implemented()


def test_plugin_manager():
    example_module_base = PluginModuleBase(
        package='tests.fixtures.plugins.example'
    )
    test_base_folder = '/tests/fixtures/plugins/'
    plugin_manager = PluginManager(test_base_folder, example_module_base)

    assert plugin_manager.plugin_base_folder == test_base_folder
    test_base = plugin_manager.base_list[0]
    assert type(test_base) == PluginModuleBase
    assert test_base.package == 'tests.fixtures.plugins.example'
    # should have loaded example plugins
    assert len(test_base.plugins) == 1
