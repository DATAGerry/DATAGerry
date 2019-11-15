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

"""
Collection of different helper classes and functions
"""
import re
import importlib


def debug_print(self):
    """
    pretty formatting of error/debug output
    Args:
        self: access the instance attribute

    Returns:
        (str): pretty formatted string of debug informations
    """
    import pprint
    return 'Class: %s \nDict:\n%s' % \
           (self.__class__.__name__, pprint.pformat(self.__dict__))


def get_config_dir():
    """
    get configuration directory
    Returns:
        (str): path to the configuration files
    """
    import os
    return os.path.join(os.path.dirname(__file__), '../../etc/')


def load_class(classname):
    """ load and return the class with the given classname """
    # extract class from module
    pattern = re.compile("(.*)\.(.*)")
    match = pattern.fullmatch(classname)
    if match is None:
        raise Exception("Could not load class {}".format(classname, ))
    module_name = match.group(1)
    class_name = match.group(2)
    loaded_module = importlib.import_module(module_name)
    loaded_class = getattr(loaded_module, class_name)
    return loaded_class


def get_module_classes(module_name):
    """
        Get all class of an module and return list of classes

    """
    import inspect

    class_list = []
    loaded_module = importlib.import_module(module_name)
    for key, data in inspect.getmembers(loaded_module, inspect.isclass):
        if module_name in str(data):
            class_list.append(key)
    return class_list


def str_to_bool(s):
    if s == 'True' or s == 'true':
        return True
    elif s == 'False' or s == 'false':
        return False
    elif s is True:
        return True
    elif s is False:
        return False
    else:
        raise ValueError
