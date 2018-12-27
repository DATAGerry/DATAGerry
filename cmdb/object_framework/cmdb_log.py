from datetime import datetime
from cmdb.utils.error import CMDBError


class CmdbLog:
    POSSIBLE_COMMANDS = ('create', 'edit')

    def __init__(self, author_id: int, action: str, message: str, state: str = None, date: (str, datetime) = None):
        """TODO: Security manager encrypt log"""
        self.author_id = author_id
        self.action = action
        self.message = message
        self.date = date or datetime.today()
        if state is None:
            self.state = None
        else:
            self.state = state

    def get_date(self) -> datetime:
        return self.date

    def get_action(self) -> str:
        return self.action

    def get_message(self) -> str:
        return self.message

    def get_state(self) -> str:
        return self.state

    def set_state(self, state):
        self.state = state

    def __repr__(self):
        from cmdb.utils.helpers import debug_print
        return debug_print(self)


class ActionNotPossibleError(CMDBError):

    def __init__(self, action):
        super().__init__()
        self.message = 'Object log could not be set - wrong action {}'.format(action)
