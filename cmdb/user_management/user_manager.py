import logging
from cmdb.user_management.user_group import UserGroup
from cmdb.user_management.user import User
from cmdb.user_management.user_right import BaseRight, GLOBAL_IDENTIFIER
from cmdb.user_management.user_authentication import AuthenticationProvider, LocalAuthenticationProvider, \
    NoValidAuthenticationProviderError
from cmdb.data_storage import NoDocumentFound, DatabaseManagerMongo
from cmdb.data_storage.database_manager import DeleteResult
from cmdb.utils.security import SecurityManager
from cmdb.utils.error import CMDBError
import cmdb

LOGGER = logging.getLogger(__name__)


class UserManagement:
    MANAGEMENT_CLASSES = {
        'GROUP_CLASSES': UserGroup,
        'USER_CLASSES': User,
        'BASE_RIGHT_CLASSES': BaseRight
    }

    def __init__(self, database_manager: DatabaseManagerMongo, security_manager: SecurityManager):
        self.dbm = database_manager
        self.scm = security_manager
        self._authentication_providers = self._load_authentication_providers()
        self.rights = self._load_rights()

    def _load_authentication_providers(self) -> dict:
        return {
            'LocalAuthenticationProvider': LocalAuthenticationProvider
        }

    def get_highest_id(self, collection: str):
        return self.dbm.get_highest_id(collection)

    def get_authentication_provider(self, name: str):
        if issubclass(self._authentication_providers[name], AuthenticationProvider):
            return self._authentication_providers[name]()
        else:
            raise NoValidAuthenticationProviderError(self._authentication_providers[name])

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
            return UserGroup(**founded_group)
        except NoDocumentFound as e:
            raise GroupNotExistsError(public_id)

    def update_group(self, update_group: UserGroup) -> bool:
        try:
            ack = self.dbm.update(collection=UserGroup.COLLECTION, public_id=update_group.get_public_id(),
                                  data=update_group.to_database())
        except CMDBError as e:
            raise GroupNotNotUpdatedError(update_group.get_name(), e)
        return ack

    def insert_group(self, insert_group: UserGroup) -> int:
        try:
            return self.dbm.insert(collection=UserGroup.COLLECTION, data=insert_group.to_database())
        except Exception as e:
            raise GroupInsertError(insert_group.get_name())

    def delete_group(self, public_id) -> DeleteResult:
        try:
            return self.dbm.delete(collection=UserGroup.COLLECTION, public_id=public_id)
        except Exception as e:
            if cmdb.__MODE__ is not 'TESTING':
                LOGGER.warning(e)
            raise GroupDeleteError(public_id)

    def get_right_names_with_min_level(self, MIN_LEVEL):
        selected_levels = list()
        for right in self.rights:
            if right.get_level() <= MIN_LEVEL:
                selected_levels.append(right.get_name())
        return selected_levels

    def _load_rights(self):
        from cmdb.user_management.rights import __all__
        return self._load_right_tree(__all__)

    def _load_right_tree(self, right_list) -> list:
        rights = list()
        for right in right_list:
            if isinstance(right, tuple) or isinstance(right, list):
                rights = rights + self._load_right_tree(right)
            else:
                rights.append(right)
        return rights

    @staticmethod
    def get_security_levels():
        return BaseRight.get_levels()

    def get_right_by_name(self, name) -> BaseRight:
        try:
            return next(right for right in self.rights if right.name == name)
        except Exception:
            raise RightNotExistsError(name)

    def group_has_right(self, group_id: int, right_name: str) -> bool:
        right_status = False
        try:
            chosen_group = self.get_group(group_id)
        except GroupNotExistsError:
            return right_status

        right_status = chosen_group.has_right(right_name)
        if not right_status:
            try:
                right_status = self._has_parent_right(chosen_group, right_name)
            except Exception:
                return False
        return right_status

    def _has_parent_right(self, group, right_name) -> bool:

        parent_right_name = '{}.{}'.format('.'.join(right_name.split('.')[:-1]), GLOBAL_IDENTIFIER)
        try:
            parent_right = self.get_right_by_name(parent_right_name)
            if parent_right.is_master():
                return group.has_right(parent_right.get_name())
            else:
                return False
        except (RightNotExistsError, Exception) as e:
            LOGGER.debug("Right not found {}".format(e.message))
            return False

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
