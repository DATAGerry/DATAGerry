import logging
from cmdb.user_management.user_group import UserGroup
from cmdb.user_management.user import User
from cmdb.user_management.user_right import BaseRight, GLOBAL_IDENTIFIER
from cmdb.data_storage import NoDocumentFound, DatabaseManagerMongo
from cmdb.data_storage.database_manager import DeleteResult
from cmdb.utils.error import CMDBError
import cmdb

LOGGER = logging.getLogger(__name__)


class UserManagement:
    MANAGEMENT_CLASSES = {
        'GROUP_CLASSES': UserGroup,
        'USER_CLASSES': User,
        'BASE_RIGHT_CLASSES': BaseRight
    }

    def __init__(self, database_manager: DatabaseManagerMongo, security_manager):
        self.dbm = database_manager
        self.scm = security_manager
        self.rights = self._load_rights()

    def _get_user(self, public_id: int):
        return self.dbm.find_one(collection=User.COLLECTION, public_id=public_id)

    def get_user(self, public_id: int) -> User:
        result = self._get_user(public_id)
        if not result:
            raise NoUserFoundExceptions(public_id)
        return User(**result)

    def get_all_users(self):
        user_list = []
        for founded_user in self.dbm.find_all(collection=User.COLLECTION):
            try:
                user_list.append(User(**founded_user))
            except CMDBError:
                LOGGER.debug("Error while user parser: {}".format(founded_user))
                continue
        return user_list

    def get_user_by_name(self, user_name) -> User:
        formatted_filter = {'user_name': user_name}
        try:
            return User(**self.dbm.find_one_by(collection=User.COLLECTION, filter=formatted_filter))
        except NoDocumentFound:
            raise NoUserFoundExceptions(user_name)

    def insert_user(self, user: User) -> int:
        try:
            self.get_group(public_id=user.group_id)
        except GroupNotExistsError as e:
            LOGGER.error(e.message)
            raise UserInsertError(user.get_username())
        try:
            return self.dbm.insert(collection=User.COLLECTION, data=user.to_database())
        except (CMDBError, Exception) as e:
            if cmdb.__MODE__ is not 'TESTING':
                LOGGER.error(e.message)
            raise UserInsertError(user.get_username())

    def delete_user(self, public_id: int) -> DeleteResult:
        try:
            return self.dbm.delete(collection=User.COLLECTION, public_id=public_id)
        except Exception as e:
            if cmdb.__MODE__ is not 'TESTING':
                LOGGER.warning(e)
            raise UserDeleteError(public_id)

    def get_all_groups(self) -> list:
        group_list = []
        for founded_group in self.dbm.find_all(collection=UserGroup.COLLECTION):
            try:
                group_list.append(UserGroup(**founded_group))
            except CMDBError:
                LOGGER.debug("Error while group parser: {}".format(founded_group))
                continue
        return group_list

    def get_group(self, public_id: int) -> UserGroup:
        try:
            founded_group = self.dbm.find_one(collection=UserGroup.COLLECTION, public_id=public_id)
            LOGGER.debug("Group Found {}".format(founded_group))
            return UserGroup(**founded_group)
        except NoDocumentFound as e:
            LOGGER.debug("Group find error {}".format(e.message))
            raise GroupNotExistsError(public_id)

    def update_group(self, update_group: UserGroup) -> bool:
        try:
            ack = self.dbm.update(collection=UserGroup.COLLECTION, public_id=update_group.get_public_id(),
                                  data=update_group.to_database())
        except CMDBError as e:
            raise GroupNotNotUpdatedError(update_group.get_name(), e)
        return ack

    def insert_group(self, name: str, label: str = None, rights: list = []) -> int:
        new_public_id = self.dbm.get_highest_id(collection=UserGroup.COLLECTION) + 1
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
                LOGGER.warning(e)
            raise GroupDeleteError(public_id)

    @staticmethod
    def _load_rights():
        from cmdb.user_management.rights import __all__
        rights = []
        for right_list in __all__:
            for right in right_list:
                rights.append(right)
        return rights

    def group_has_right(self, group_id: int, right_name: str) -> bool:
        right_status = False
        try:
            chosen_group = self.get_group(group_id)
        except (GroupNotExistsError, Exception):
            return right_status
        right_status = chosen_group.has_right(right_name)
        if not right_status:
            try:
                # check for global right
                parent_right = '{}.{}'.format('.'.join(right_name.split('.')[:-1]), GLOBAL_IDENTIFIER)
                LOGGER.debug("Parent global right: {}".format(parent_right))
                right_status = chosen_group.has_right(parent_right)
            except Exception:
                return False
        return right_status

    def user_group_has_right(self, user: User, right_name: str) -> bool:
        try:
            return self.group_has_right(user.get_group(), right_name)
        except (CMDBError, Exception):
            return False


class GroupDeleteError(CMDBError):
    def __init__(self, name):
        super().__init__()
        self.message = "The following group could not be deleted: {}".format(name)


class UserDeleteError(CMDBError):
    def __init__(self, name):
        super().__init__()
        self.message = "The following user could not be deleted: {}".format(name)


class NoUserFoundExceptions(CMDBError):
    """Exception if user was not found in the database"""

    def __init__(self, username):
        self.message = "No user with the username or the id {} was found in database".format(username)


class GroupNotExistsError(CMDBError):
    def __init__(self, name):
        super().__init__()
        self.message = "The following group does not exists: {}".format(name)


class GroupNotNotUpdatedError(CMDBError):
    def __init__(self, name, error):
        super().__init__()
        self.message = "The following group could not be updated: {} | error: {}".format(name, error.message)


class RightNotExistsError(CMDBError):
    def __init__(self, name):
        super().__init__()
        self.message = "The following right does not exists: {}".format(name)


class GroupInsertError(CMDBError):
    def __init__(self, name):
        super().__init__()
        self.message = "The following group could not be added: {}".format(name)


class UserInsertError(CMDBError):
    def __init__(self, name):
        super().__init__()
        self.message = "The following user could not be added: {}".format(name)


class WrongTypeException(Exception):
    """Exception if input_type was wrong"""

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
