# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import logging
from typing import List

from cmdb.database.managers import DatabaseManagerMongo
from cmdb.database.errors.database_errors import NoDocumentFound
from cmdb.framework.cmdb_base import CmdbManagerBase, ManagerGetError, ManagerInsertError, ManagerUpdateError, \
    ManagerDeleteError
from cmdb.user_management.models.user import UserModel
from cmdb.user_management.models.group import UserGroupModel
from cmdb.user_management.models.right import BaseRight
from cmdb.utils.error import CMDBError
from cmdb.security.security import SecurityManager

LOGGER = logging.getLogger(__name__)


class UserManager(CmdbManagerBase):

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.scm = SecurityManager(database_manager)
        self.rights = self._load_rights()
        super(UserManager, self).__init__(database_manager)

    def get_new_id(self, collection: str) -> int:
        return self.dbm.get_next_public_id(collection)

    def get_users(self) -> List[UserModel]:
        """Get all users"""
        user_list = []
        for founded_user in self._get_many(collection=UserModel.COLLECTION):
            try:
                user_list.append(UserModel.from_data(founded_user))
            except CMDBError:
                continue
        return user_list

    def get_users_by(self, sort='public_id', **requirements) -> List[UserModel]:
        """Get a list of users by requirement"""
        user_list = []
        users_in_database = self._get_many(collection=UserModel.COLLECTION, sort=sort, **requirements)
        for user in users_in_database:
            try:
                user_ = UserModel.from_data(user)
            except CMDBError as err:
                LOGGER.error(f'[UserManager] Error while inserting database user into return list: {err}')
                continue
            user_list.append(user_)
        return user_list

    def get_user_by(self, **requirements) -> UserModel:
        """Get user by requirement"""
        try:
            return UserModel.from_data(self._get_by(collection=UserModel.COLLECTION, **requirements))
        except NoDocumentFound:
            raise UserManagerGetError(f'UserModel not found')

    def get_user_by_name(self, user_name) -> UserModel:
        """Get a user by his user_name"""
        return self.get_user_by(user_name=user_name)

    def update_user(self, public_id, update_params: dict):
        try:
            return self._update(collection=UserModel.COLLECTION, public_id=public_id, data=update_params)
        except (CMDBError, Exception):
            raise UserManagerUpdateError(f'Could not update user with ID: {public_id}')

    def update_users_by(self, query: dict, update: dict):
        try:
            return self._update_many(collection=UserModel.COLLECTION, query=query, update=update)
        except Exception as err:
            raise UserManagerUpdateError(err)

    def delete_user(self, public_id: int) -> bool:
        try:
            return self._delete(collection=UserModel.COLLECTION, public_id=public_id)
        except Exception:
            raise UserManagerDeleteError(f'Could not delete user with ID: {public_id}')

    def delete_users_by(self, query: dict):
        try:
            return self._delete_many(collection=UserModel.COLLECTION, filter_query=query).acknowledged
        except Exception as err:
            raise UserManagerDeleteError(err)

    def get_groups(self) -> list:
        group_list = []
        for founded_group in self._get_many(collection=UserGroupModel.COLLECTION):
            try:
                group_list.append(UserGroupModel(**founded_group))
            except CMDBError:
                LOGGER.debug("Error while group parser: {}".format(founded_group))
                continue
        return group_list

    def get_group(self, public_id: int) -> UserGroupModel:
        try:
            founded_group = self._get(collection=UserGroupModel.COLLECTION, public_id=public_id)
            return UserGroupModel(**founded_group)
        except NoDocumentFound as e:
            raise UserManagerGetError(e)

    def get_group_by(self, **requirements) -> UserGroupModel:
        try:
            return UserGroupModel(**self._get_by(collection=UserGroupModel.COLLECTION, **requirements))
        except NoDocumentFound:
            raise UserManagerGetError(f'Group not found')

    def update_group(self, public_id, update_params: dict) -> bool:
        try:
            ack = self._update(collection=UserGroupModel.COLLECTION, public_id=public_id,
                               data=update_params)
        except (CMDBError, Exception) as e:
            LOGGER.error(e)
            raise UserManagerUpdateError(e)
        return ack

    def insert_group(self, insert_group: UserGroupModel) -> int:
        try:
            return self.dbm.insert(collection=UserGroupModel.COLLECTION, data=insert_group.__dict__)
        except Exception:
            raise UserManagerInsertError(insert_group.name)

    def delete_group(self, public_id, user_action: str = None, options: dict = None) -> bool:
        try:
            delete_group: UserGroupModel = self.get_group(public_id)
        except UserManagerGetError:
            raise UserManagerDeleteError(f'Could not find group with ID: {public_id}')

        try:
            ack = self.dbm.delete(collection=UserGroupModel.COLLECTION, public_id=public_id).acknowledged
        except Exception:
            raise UserManagerDeleteError(f'Could not delete group')

        # Cleanup user
        users_in_group: [UserModel] = self.get_users_by(**{'group_id': delete_group.get_public_id()})
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
                selected_levels.append(right.get_display_name())
        return selected_levels

    def get_all_rights(self):
        return self.rights

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