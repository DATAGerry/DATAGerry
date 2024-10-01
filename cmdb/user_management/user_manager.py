# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
"""TODO: document"""
import logging

from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.security.security import SecurityManager
from cmdb.cmdb_objects.cmdb_base import CmdbManagerBase

from cmdb.user_management.models.user import UserModel
from cmdb.user_management.models.group import UserGroupModel
from cmdb.user_management.models.right import BaseRight
import cmdb.user_management.rights as all_rights

from cmdb.errors.database import NoDocumentFound
from cmdb.errors.manager.user_manager import UserManagerGetError,\
                                             UserManagerInsertError,\
                                             UserManagerUpdateError,\
                                             UserManagerDeleteError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                      UserManager                                                     #
# -------------------------------------------------------------------------------------------------------------------- #

class UserManager(CmdbManagerBase):
    """TODO: document"""

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.scm = SecurityManager(database_manager)
        self.rights = self._load_rights()
        super().__init__(database_manager)


    def get_new_id(self, collection: str) -> int:
        """TODO: document"""
        return self.dbm.get_next_public_id(collection)


    def get_users(self) -> list[UserModel]:
        """Get all users"""
        user_list = []
        for founded_user in self._get_many(collection=UserModel.COLLECTION):
            try:
                user_list.append(UserModel.from_data(founded_user))
            except Exception:
                #TODO: ERROR-FIX
                continue
        return user_list


    def get_users_by(self, sort='public_id', **requirements) -> list[UserModel]:
        """Get a list of users by requirement"""
        user_list = []
        users_in_database = self._get_many(collection=UserModel.COLLECTION, sort=sort, **requirements)
        for user in users_in_database:
            try:
                user_ = UserModel.from_data(user)
            except Exception as err:
                #TODO: ERROR-FIX
                LOGGER.error('[UserManager] Error while inserting database user into return list: %s',err)
                continue

            user_list.append(user_)

        return user_list


    def get_user_by(self, **requirements) -> UserModel:
        """Get user by requirement"""
        try:
            return UserModel.from_data(self._get_by(collection=UserModel.COLLECTION, **requirements))
        except NoDocumentFound as err:
            raise UserManagerGetError('UserModel not found!') from err


    def get_user_by_name(self, user_name) -> UserModel:
        """Get a user by his user_name"""
        return self.get_user_by(user_name=user_name)


    def update_user(self, public_id, update_params: dict):
        """TODO: document"""
        try:
            return self._update(collection=UserModel.COLLECTION, public_id=public_id, data=update_params)
        except Exception as err:
            #TODO: ERROR-FIX
            raise UserManagerUpdateError(f'Could not update user with ID: {public_id}') from err


    def update_users_by(self, query: dict, update: dict):
        """TODO: document"""
        try:
            return self._update_many(collection=UserModel.COLLECTION, query=query, update=update)
        except Exception as err:
            #TODO: ERROR-FIX
            raise UserManagerUpdateError(str(err)) from err


    def delete_user(self, public_id: int) -> bool:
        """TODO: document"""
        try:
            return self._delete(collection=UserModel.COLLECTION, public_id=public_id)
        except Exception as err:
            #TODO: ERROR-FIX
            raise UserManagerDeleteError(f'Could not delete user with ID: {public_id}') from err


    def delete_users_by(self, query: dict):
        """TODO: document"""
        try:
            return self.delete_many(collection=UserModel.COLLECTION, filter_query=query).acknowledged
        except Exception as err:
            #TODO: ERROR-FIX
            raise UserManagerDeleteError(str(err)) from err


    def get_groups(self) -> list:
        """TODO: document"""
        group_list = []
        for found_group in self._get_many(collection=UserGroupModel.COLLECTION):
            try:
                group_list.append(UserGroupModel(**found_group))
            except Exception:
                #TODO: ERROR-FIX
                LOGGER.debug("Error while group parser: %s",found_group)
                continue

        return group_list


    def get_group(self, public_id: int) -> UserGroupModel:
        """TODO: document"""
        try:
            founded_group = self._get(collection=UserGroupModel.COLLECTION, public_id=public_id)
            return UserGroupModel(**founded_group)
        except NoDocumentFound as err:
            raise UserManagerGetError('Group not found!') from err


    def get_group_by(self, **requirements) -> UserGroupModel:
        """TODO: document"""
        try:
            return UserGroupModel(**self._get_by(collection=UserGroupModel.COLLECTION, **requirements))
        except NoDocumentFound as err:
            raise UserManagerGetError('Group not found') from err


    def update_group(self, public_id, update_params: dict) -> bool:
        """TODO: document"""
        try:
            ack = self._update(collection=UserGroupModel.COLLECTION, public_id=public_id,
                               data=update_params)
        except Exception as err:
            #TODO: ERROR-FIX
            raise UserManagerUpdateError(str(err)) from err
        return ack


    def insert_group(self, insert_group: UserGroupModel) -> int:
        """TODO: document"""
        try:
            return self.dbm.insert(collection=UserGroupModel.COLLECTION, data=insert_group.__dict__)
        except Exception as err:
            #TODO: ERROR-FIX
            raise UserManagerInsertError(str(err)) from err


    def delete_group(self, public_id, user_action: str = None, options: dict = None) -> bool:
        """TODO: document"""
        try:
            delete_group: UserGroupModel = self.get_group(public_id)
        except UserManagerGetError as err:
            #TODO: ERROR-FIX
            raise UserManagerDeleteError(f'Could not find group with ID: {public_id}') from err

        try:
            ack = self.dbm.delete(collection=UserGroupModel.COLLECTION, public_id=public_id).acknowledged
        except Exception as err:
            #TODO: ERROR-FIX
            raise UserManagerDeleteError('Could not delete group') from err

        # Cleanup user
        users_in_group: list[UserModel] = self.get_users_by(**{'group_id': delete_group.get_public_id()})
        if len(users_in_group) > 0:
            if user_action == 'move':
                if not options.get('group_id'):
                    #TODO: ERROR-FIX
                    raise UserManagerDeleteError('Not move group was provided!')
                self.update_users_by(query={'group_id': delete_group.get_public_id()},
                                     update={'group_id': int(options.get('group_id'))})
            elif user_action == 'delete':
                self.delete_users_by({'group_id': delete_group.get_public_id()})
            else:
                #TODO: ERROR-FIX
                raise UserManagerDeleteError('No valid user action was provided')
        return ack


    def get_right_names_with_min_level(self, min_level):
        """TODO: document"""
        selected_levels = []
        for right in self.rights:
            if right.get_level() <= min_level:
                selected_levels.append(right.get_display_name())
        return selected_levels


    def get_all_rights(self):
        """TODO: document"""
        return self.rights


    def _load_rights(self):
        return self._load_right_tree(all_rights.__all__)


    def _load_right_tree(self, right_list) -> list:
        rights = list()
        for right in right_list:
            if isinstance(right, tuple) or isinstance(right, list):
                rights = rights + self._load_right_tree(right)
            else:
                rights.append(right)
        return rights


    def get_right_by_name(self, name) -> BaseRight:
        """TODO: document"""
        try:
            return next(right for right in self.rights if right.name == name)
        except Exception as exc:
            raise UserManagerGetError(name) from exc


    def group_has_right(self, group_id: int, right_name: str) -> bool:
        """TODO: document"""
        right_status = False

        try:
            selected_right = self.get_right_by_name(right_name)
            chosen_group = self.get_group(group_id)
        except UserManagerGetError:
            #TODO: ERROR-FIX
            return right_status

        right_status = chosen_group.has_right(right_name=right_name)

        if not right_status:
            right_status = chosen_group.has_extended_right(right_name=right_name)

        return right_status
