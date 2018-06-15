def debug_print(self):
    import pprint
    return 'Class: %s \nDict:\n%s' % \
           (self.__class__.__name__, pprint.pformat(self.__dict__))