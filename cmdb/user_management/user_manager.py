from cmdb.user_management.user_rights import UserRight
from cmdb.user_management.user_groups import UserGroup
from cmdb.user_management.user import User
from cmdb.data_storage import NoDocumentFound


class UserManagement:

    MANAGEMENT_CLASSES = {
        'RIGHT_CLASSES': UserRight,
        'GROUP_CLASSES': UserGroup,
        'USER_CLASSES': User
    }

    def __init__(self, database_manager, security_manager):
        self.dbm = database_manager
        self.scm = security_manager

    def _get_user(self, public_id):
        return self.dbm.find_one(collection=User.COLLECTION, public_id=public_id)

    def get_all_users(self):
        all_users = self.dbm.find_all(collection=User.COLLECTION)
        user_list = []
        for user in all_users:
            tmp_user = User(
                **user
            )
            user_list.append(tmp_user)
        return user_list

    def get_all_groups(self):
        all_groups = self.dbm.find_all(collection=UserGroup.COLLECTION)
        group_list = []
        for group in all_groups:
            tmp_group = UserGroup(
                **group
            )
            group_list.append(tmp_group)
        return group_list

    def get_group_by_name(self, name):
        formatted_filter = {'name': name }
        try:
            return self.dbm.find_one_by(collection=UserGroup.COLLECTION, filter=formatted_filter)
        except NoDocumentFound:
            raise GroupNotFound(name)

    def get_user_by_id(self, public_id):
        result = self._get_user(public_id)
        if not result:
            raise NoUserFoundExceptions(public_id)
        return User(**result)

    def add_user(self, user_name, group, authenticator, password=""):
        import datetime
        if password != "":
            password = self.scm.generate_hmac(password)
        group = UserGroup(
            **self.get_group_by_name(group)
        )
        user_data = {
            'public_id': self.dbm.get_highest_id(collection=User.COLLECTION),
            'username': user_name,
            'password': password,
            'authenticator': authenticator,
            'group': group._id,
            'registration_time': datetime.datetime.utcnow()
        }
        insert_id = self.dbm.insert(collection=User.COLLECTION, data=user_data)
        try:
            User(**self.dbm.find_one(collection=User.COLLECTION, public_id=insert_id))
        except Exception as e:
            self.dbm.delete(collection=User.COLLECTION, public_id=insert_id)
            raise UserAddFailedException(user_name, e.message)
        return insert_id

    def user_has_right(self, user, right):
        founded_group = self.dbm.find_one(collection=UserGroup.COLLECTION, filter={'name': user.group})
        founded_right = self.dbm.find_one(collection=UserRight.COLLECTION, filter={'name': right})
        if founded_right['name'] in founded_group['rights']:
            return True
        return False


class NoUserFoundExceptions(Exception):
    """Exception if user was not found in the database"""
    def __init__(self, username):
        self.message = "No user with the username or the id {} was found in database".format(username)


class GroupNotFound(Exception):
    def __init__(self, name):
        super().__init__()
        self.message = "The following group does not exists: {}".format(name)


class UserAddFailedException(Exception):
    def __init__(self, username, error_msg):
        self.message = "User could not be added {} into database \n Error: {}"\
            .format(username, error_msg)
