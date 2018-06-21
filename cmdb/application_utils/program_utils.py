def debug_print(self):
    import pprint
    return 'Class: %s \nDict:\n%s' % \
           (self.__class__.__name__, pprint.pformat(self.__dict__))


def get_config_dir():
    import os
    return os.path.join(os.path.dirname(__file__), '../../etc/')
