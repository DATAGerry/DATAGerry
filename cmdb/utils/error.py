"""
Error super class
"""


class CMDBError(Exception):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        from cmdb.utils.helpers import debug_print
        return debug_print(self.message or self.msg)
