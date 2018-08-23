class NoUserFoundExceptions(Exception):
    """Exception if user was not found in the database"""
    def __init__(self, username):
        self.message = "No user with the username or the id {} was found in database".format(username)


class WrongTypeException(Exception):
    """Exception if type was wrong"""
    def __init__(self):
        super().__init__()


class WrongPassException(Exception):
    """Exception if wrong password"""
    def __init__(self):
        super().__init__()


class UserHasNotRequiredRight(Exception):
    """Exception if user has not the right for an action"""
    def __init__(self, user, right):
        self.message = "The user {} has not the required right level {} to view this page".format(user.user_name, right)
