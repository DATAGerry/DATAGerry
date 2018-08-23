class UserManagementBase:

    COLLECTION = 'management.*'

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self):
        from cmdb.utils.helpers import debug_print
        return debug_print(self)
