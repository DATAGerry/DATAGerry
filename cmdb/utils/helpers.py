"""
Collection of different helper classes and functions
"""


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


def timing(f):
    from cmdb.utils import get_logger

    def wrap(*args):
        import time
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        get_logger().debug('CMDB took {:.3f}ms to start'.format((time2 - time1) * 1000.0))
        return ret

    return wrap
