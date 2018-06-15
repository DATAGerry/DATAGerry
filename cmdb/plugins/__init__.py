"""Simple plugin system
based on: https://stackoverflow.com/questions/14510286/plugin-architecture-plugin-manager-vs-inspecting-from-plugins-import
          http://martyalchin.com/2008/jan/10/simple-plugin-framework/
"""
from cmdb.plugins.plugin_base import PluginType
from cmdb.plugins.plugin_manager import PluginManager
from cmdb.plugins import auth

plugin_manager = PluginManager(

)
