"""
Collection of different helper classes and functions
"""
import re
import importlib
from functools import wraps
from json import JSONEncoder
import cmdb.data_storage.database_utils


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


def timing(msg=None):
    """
    Time wrap function - Measures time of function duration
    Args:
        msg: output message

    Returns:
        wrap function
    """

    def _timing(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            import logging
            import time
            time1 = time.clock()
            ret = f(*args)
            time2 = time.clock()
            logging.getLogger(__name__).debug('{} {:.3f}ms'.format(msg, (time2 - time1) * 1000.0))
            return ret

        return wrap

    return _timing


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
