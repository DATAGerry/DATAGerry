# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from typing import List

from cmdb.data_storage.database_manager import NoDocumentFound, DatabaseManagerMongo
from cmdb.framework.cmdb_base import CmdbManagerBase, ManagerGetError, ManagerInsertError, ManagerUpdateError, \
    ManagerDeleteError
from cmdb.user_management.user import User
from cmdb.user_management.user_group import UserGroup
from cmdb.user_management.user_right import BaseRight
from cmdb.utils import get_security_manager
from cmdb.utils.error import CMDBError
from cmdb.utils.security import SecurityManager
from cmdb.utils.system_reader import SystemConfigReader

LOGGER = logging.getLogger(__name__)


class UserManager(CmdbManagerBase):

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.scm = SecurityManager(database_manager)
        self.rights = self._load_rights()
        super(UserManager, self).__init__(database_manager)

    def search(self):
        pass

    def get_new_id(self, collection: str) -> int:
        return self.dbm.get_next_public_id(collection)

    def count_user(self) -> int:
        """Get number of users"""
        return self._count(collection=User.COLLECTION)

    def get_user(self, public_id: int) -> User:
        """Get user by public id"""
        try:
            result = User(**self._get(collection=User.COLLECTION, public_id=public_id))
        except (CMDBError, Exception) as err:
            raise UserManagerGetError(err)
        return result

    def get_users(self) -> List[User]:
        """Get all users"""
        user_list = []
        for founded_user in self._get_many(collection=User.COLLECTION):
            try:
                user_list.append(User(**founded_user))
            except CMDBError:
                continue
        return user_list

    def get_users_by(self, sort='public_id', **requirements) -> List[User]:
        """Get a list of users by requirement"""
        user_list = []
        users_in_database = self._get_many(collection=User.COLLECTION, sort=sort, **requirements)
        for user in users_in_database:
            try:
                user_ = User(**user)
            except CMDBError as err:
                LOGGER.error(f'[UserManager] Error while inserting database user into return list: {err}')
                continue
            user_list.append(user_)
        return user_list

    def get_user_by(self, **requirements) -> User:
        """Get user by requirement"""
        try:
            return User(**self._get_by(collection=User.COLLECTION, **requirements))
        except NoDocumentFound:
            raise UserManagerGetError(f'User not found')

    def get_user_by_name(self, user_name) -> User:
        """Get a user by his user_name"""
        return self.get_user_by(user_name=user_name)

    def insert_user(self, user: User) -> int:
        """
        TODO: Refactor for dict use
        """
        try:
            return self.dbm.insert(collection=User.COLLECTION, data=user.to_database())
        except (CMDBError, Exception):
            raise UserManagerInsertError(f'Could not insert {user.get_username()}')

    def update_user(self, public_id, update_params: dict):
        try:
            return self._update(collection=User.COLLECTION, public_id=public_id, data=update_params)
        except (CMDBError, Exception):
            raise UserManagerUpdateError(f'Could not update user with ID: {public_id}')

    def update_users_by(self, query: dict, update: dict):
        try:
            return self._update_many(collection=User.COLLECTION, query=query, update=update)
        except Exception as err:
            raise UserManagerUpdateError(err)

    def delete_user(self, public_id: int) -> bool:
        try:
            return self._delete(collection=User.COLLECTION, public_id=public_id)
        except Exception:
            raise UserManagerDeleteError(f'Could not delete user with ID: {public_id}')

    def delete_users_by(self, query: dict):
        try:
            return self._delete_many(collection=User.COLLECTION, filter_query=query).acknowledged
        except Exception as err:
            raise UserManagerDeleteError(err)

    def get_groups(self) -> list:
        group_list = []
        for founded_group in self._get_many(collection=UserGroup.COLLECTION):
            try:
                group_list.append(UserGroup(**founded_group))
            except CMDBError:
                LOGGER.debug("Error while group parser: {}".format(founded_group))
                continue
        return group_list

    def get_group(self, public_id: int) -> UserGroup:
        try:
            founded_group = self._get(collection=UserGroup.COLLECTION, public_id=public_id)
            return UserGroup(**founded_group)
        except NoDocumentFound as e:
            raise UserManagerGetError(e)

    def get_group_by(self, **requirements) -> UserGroup:
        try:
            return UserGroup(**self._get_by(collection=UserGroup.COLLECTION, **requirements))
        except NoDocumentFound:
            raise UserManagerGetError(f'Group not found')

    def update_group(self, public_id, update_params: dict) -> bool:
        try:
            ack = self._update(collection=UserGroup.COLLECTION, public_id=public_id,
                                  data=update_params)
        except (CMDBError, Exception) as e:
            LOGGER.error(e)
            raise UserManagerUpdateError(e)
        return ack

    def insert_group(self, insert_group: UserGroup) -> int:
        try:
            return self.dbm.insert(collection=UserGroup.COLLECTION, data=insert_group.to_database())
        except Exception:
            raise UserManagerInsertError(insert_group.get_name())

    def delete_group(self, public_id, user_action: str = None, options: dict = None) -> bool:
        try:
            delete_group: UserGroup = self.get_group(public_id)
        except UserManagerGetError:
            raise UserManagerDeleteError(f'Could not find group with ID: {public_id}')

        if not delete_group.is_deletable():
            raise UserManagerDeleteError(f'Group {delete_group.get_label()} is not deletable!')

        try:
            ack = self.dbm.delete(collection=UserGroup.COLLECTION, public_id=public_id).acknowledged
        except Exception:
            raise UserManagerDeleteError(f'Could not delete group')

        # Cleanup user
        users_in_group: [User] = self.get_users_by(**{'group_id': delete_group.get_public_id()})
        if len(users_in_group) > 0:
            if user_action == 'move':
                if not options.get('group_id'):
                    raise UserManagerDeleteError(f'Not move group was provided!')
                self.update_users_by(query={'group_id': delete_group.get_public_id()},
                                     update={'$set': {'group_id': int(options.get('group_id'))}})
            elif user_action == 'delete':
                self.delete_users_by({'group_id': delete_group.get_public_id()})
            else:
                raise UserManagerDeleteError(f'No valid user action was provided')
        return ack

    def get_right_names_with_min_level(self, min_level):
        selected_levels = []
        for right in self.rights:
            if right.get_level() <= min_level:
                selected_levels.append(right.get_name())
        return selected_levels

    def get_all_rights(self):
        return self.rights

    @staticmethod
    def get_right_tree():
        from cmdb.user_management.rights import __all__
        return __all__

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
            raise UserManagerGetError(name)

    def group_has_right(self, group_id: int, right_name: str) -> bool:
        right_status = False
        try:
            selected_right = self.get_right_by_name(right_name)
            chosen_group = self.get_group(group_id)
        except UserManagerGetError:
            return right_status

        right_status = chosen_group.has_right(right_name=right_name)
        if not right_status:
            right_status = chosen_group.has_extended_right(right_name=right_name)
        return right_status


class UserManagerGetError(ManagerGetError):

    def __init__(self, err):
        super(UserManagerGetError, self).__init__(err)


class UserManagerInsertError(ManagerInsertError):

    def __init__(self, err):
        super(UserManagerInsertError, self).__init__(err)


class UserManagerUpdateError(ManagerUpdateError):

    def __init__(self, err):
        super(UserManagerUpdateError, self).__init__(err)


class UserManagerDeleteError(ManagerDeleteError):

    def __init__(self, err):
        super(UserManagerDeleteError, self).__init__(err)