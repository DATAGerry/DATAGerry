from cmdb.user_management.user_rights import UserRight
from cmdb.user_management.user_groups import UserGroup
from cmdb.user_management.user import User
from cmdb.user_management.user_authentication import LocalAuthenticationProvider
from cmdb.data_storage import NoDocumentFound, DatabaseManagerMongo
from cmdb.data_storage.database_manager import DeleteResult
from cmdb.utils import get_logger
import cmdb

LOGGER = get_logger()


class UserManagement:
    MANAGEMENT_CLASSES = {
        'RIGHT_CLASSES': UserRight,
        'GROUP_CLASSES': UserGroup,
        'USER_CLASSES': User
    }

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.dbm = database_manager

    def _get_user(self, public_id: int):
        return self.dbm.find_one(collection=User.COLLECTION, public_id=public_id)

    def get_user(self, public_id: int) -> User:
        result = self._get_user(public_id)
        if not result:
            raise NoUserFoundExceptions(public_id)
        return User(**result)

    def insert_user(self, user_name: str, group_id: int, password=None,
                    first_name=None, last_name=None, authenticator=LocalAuthenticationProvider) -> int:
        from datetime import datetime
        new_public_id = self.dbm.get_highest_id(collection=User.COLLECTION)+1
        authenticator = authenticator.__class__.__name__
        try:
            self.get_group(public_id=group_id)
        except GroupNotExistsError:
            raise UserInsertError(user_name)

        insert_user = User(
            public_id=new_public_id,
            user_name=user_name,
            group_id=group_id,
            registration_time=datetime.utcnow(),
            password=password,
            first_name=first_name or "",
            last_name=last_name or "",
            authenticator=authenticator
        )
        try:
            return self.dbm.insert(collection=User.COLLECTION, data=insert_user.to_database())
        except Exception as e:
            if cmdb.__MODE__ is not 'TESTING':
                LOGGER.warn(e)
            raise UserInsertError(insert_user.get_username())

    def delete_user(self, public_id: int) -> DeleteResult:
        try:
            return self.dbm.delete(collection=User.COLLECTION, public_id=public_id)
        except Exception as e:
            if cmdb.__MODE__ is not 'TESTING':
                LOGGER.warn(e)
            raise UserDeleteError(public_id)

    def get_group(self, public_id: int) -> UserGroup:
        formatted_filter = {'public_id': public_id}
        try:
            founded_group = self.dbm.find_one_by(collection=UserGroup.COLLECTION, filter=formatted_filter)
            return UserGroup(**founded_group)
        except NoDocumentFound:
            raise GroupNotExistsError(public_id)

    def insert_group(self, name: str, label: str = None, rights: list = []) -> int:
        new_public_id = self.dbm.get_highest_id(collection=UserGroup.COLLECTION)+1
        insert_group = UserGroup(
            name=name,
            label=label or name.title(),
            rights=rights or [],
            public_id=new_public_id
        )
        try:
            return self.dbm.insert(collection=UserGroup.COLLECTION, data=insert_group.to_database())
        except Exception as e:
            if cmdb.__MODE__ is not 'TESTING':
                LOGGER.warn(e)
            raise GroupInsertError(insert_group.get_name())

    def delete_group(self, public_id) -> DeleteResult:
        try:
            return self.dbm.delete(collection=UserGroup.COLLECTION, public_id=public_id)
        except Exception as e:
            if cmdb.__MODE__ is not 'TESTING':
                LOGGER.warn(e)
            raise GroupDeleteError(public_id)

    """
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
        formatted_filter = {'name': name}
        try:
            return self.dbm.find_one_by(collection=UserGroup.COLLECTION, filter=formatted_filter)
        except NoDocumentFound:
            raise GroupNotFound(name)



    def user_has_right(self, user, right):
        founded_group = self.dbm.find_one(collection=UserGroup.COLLECTION, filter={'name': user.group})
        founded_right = self.dbm.find_one(collection=UserRight.COLLECTION, filter={'name': right})
        if founded_right['name'] in founded_group['rights']:
            return True
        return False
    """


class GroupDeleteError(Exception):
    def __init__(self, name):
        super().__init__()
        self.message = "The following group could not be deleted: {}".format(name)


class UserDeleteError(Exception):
    def __init__(self, name):
        super().__init__()
        self.message = "The following user could not be deleted: {}".format(name)


class NoUserFoundExceptions(Exception):
    """Exception if user was not found in the database"""

    def __init__(self, username):
        self.message = "No user with the username or the id {} was found in database".format(username)


class GroupNotExistsError(Exception):
    def __init__(self, name):
        super().__init__()
        self.message = "The following group does not exists: {}".format(name)


class GroupInsertError(Exception):
    def __init__(self, name):
        super().__init__()
        self.message = "The following group could not be added: {}".format(name)


class UserInsertError(Exception):
    def __init__(self, name):
        super().__init__()
        self.message = "The following user could not be added: {}".format(name)
