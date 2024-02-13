# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
Collection of different helper classes and functions
"""
import re
import os
import sys
import importlib
import pprint
# -------------------------------------------------------------------------------------------------------------------- #

def debug_print(self):
    """
    pretty formatting of error/debug output
    Args:
        self: access the instance attribute

    Returns:
        (str): pretty formatted string of debug informations
    """
    return f'Class: {self.__class__.__name__} \nDict:\n{pprint.pformat(self.__dict__)}'


def get_config_dir():
    """
    get configuration directory
    Returns:
        (str): path to the configuration files
    """
    return os.path.join(os.path.dirname(__file__), '../../etc/')


def load_class(classname):
    """ load and return the class with the given classname """
    # extract class from module
    pattern = re.compile("(.*)\.(.*)")
    match = pattern.fullmatch(classname)
    if match is None:
        raise Exception(f"Could not load class {classname}")
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
    """TODO: document"""
    if s in ('True', 'true'):
        return True

    if s in ('False', 'false'):
        return False

    if s is True:
        return True

    if s is False:
        return False

    raise ValueError


def process_bar(name, total, progress):
    """
    Displays or updates a console progress bar.
    Args:
        name: Process bar name
        total: max. processes
        progress: current process
    """
    through_of = f"\t| [{progress}/{total}]"
    bar_length, status = 50, ""
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(bar_length * progress))
    text = '\r{}:[{}] {:.0f}% {} {} \n'.format(
        name,
        "#" * block + "-" * (bar_length - block),
        round(progress * 100, 0),
        through_of,
        status)
    sys.stdout.write(text)
    sys.stdout.flush()
