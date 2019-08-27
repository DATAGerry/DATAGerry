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
    package='tests.fixtures.plugins.example',
    include_paths=None,
    default_file='__init__.py'
)
