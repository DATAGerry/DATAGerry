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
    from tests.plugins.example import example_module_base

    plugin_loader = PluginLoader(example_module_base.main_module, example_module_base.package)
    # should load all plugins inside plugins.example
    loaded_plugins = plugin_loader.load_plugins()
    assert len(loaded_plugins) == 1
    example_plugin = loaded_plugins[0]
    assert type(example_plugin) == ModuleType


def test_plugin_module_base():
    # basic tests
    example_module_base1 = PluginModuleBase(
        package='tests.plugins.example'
    )
    assert example_module_base1.package == 'tests.plugins.example'
    example_module_base2 = PluginModuleBase(
        package='tests.plugins.example',
        include_paths='/tests/plugins/example/',
        default_file='test.py'
    )
    assert example_module_base2.default_file == 'test.py'
    assert example_module_base2.include_paths == '/tests/plugins/example/'

    # Init tests inside plugin dir
    from .plugins.example import example_module_base
    assert example_module_base.package == 'tests.plugins.example'


def test_plugin_base():
    test_base = PluginBase(plugin_name='example', plugin_type='example')
    assert test_base.plugin_name == 'example'
    assert test_base.plugin_type == 'example'

    with pytest.raises(ValueError):
        PluginBase(plugin_name='example', plugin_type='example2')


def test_plugin():
    from tests.plugins.example.test_plugin import TestPlugin

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
        package='tests.plugins.example'
    )
    test_base_folder = '/tests/plugins/'
    plugin_manager = PluginManager(test_base_folder, example_module_base)

    assert plugin_manager.plugin_base_folder == test_base_folder
    test_base = plugin_manager.base_list[0]
    assert type(test_base) == PluginModuleBase
    assert test_base.package == 'tests.plugins.example'
    # should have loaded example plugins
    assert len(test_base.plugins) == 1
