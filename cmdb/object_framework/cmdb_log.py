from datetime import datetime
from cmdb.utils.error import CMDBError


class CmdbLog:
    POSSIBLE_COMMANDS = ('create', 'edit', 'delete')

    def __init__(self, author_id: int, action: str, message: str, log: list=None, date: str=None):
        """TODO: Security manager encrypt log"""
        self.author_id = author_id
        self.action = action
        self.message = message
        self.date = date or datetime.today()
        if log is None:
            self.log = None
        else:
            self.log = log

    def get_date(self) -> datetime:
        return self.date

    @property
    def action(self) -> str:
        return self._action

    @action.setter
    def action(self, value: str):
        if value not in CmdbLog.POSSIBLE_COMMANDS:
            raise ActionNotPossibleError(value)
        self._action = value

    def __repr__(self):
        from cmdb.utils.helpers import debug_print
        return debug_print(self)


class ActionNotPossibleError(CMDBError):

    def __init__(self, action):
        super().__init__()
        self.message = 'Object log could not be set - wrong action {}'.format(action)
