from cmdb.plugins.plugin_system import PluginModuleBase, PluginBase


class ExamplePluginBase(PluginBase):

    def __init__(self, plugin_name: str):
        self.plugin_name = plugin_name
        super(PluginBase, self).__init__(self, plugin_name, 'example')

    def function_not_implemented(self):
        raise NotImplementedError()

    def function_override(self):
        raise NotImplementedError()

    def parent_function(self):
        return self.plugin_name


example_module_base = PluginModuleBase(
    package='tests.plugins.example',
    include_paths=None,
    default_file='__init__.py'
)
