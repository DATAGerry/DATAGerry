from tests.plugins.example import ExamplePluginBase


class TestPlugin(ExamplePluginBase):

    def __init__(self, test=True):
        self.test = test
        super(ExamplePluginBase, self).__init__('Test_Plugin', 'example')

    def function_override(self):
        return self.test

    def new_function(self):
        return self.test
