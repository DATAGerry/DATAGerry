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