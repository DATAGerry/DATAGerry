from cmdb.user_management.user_exceptions import NoUserFoundExceptions, WrongTypeException, UserHasNotRequiredRight
from cmdb.user_management.user_rights import UserRight
from cmdb.user_management.user_groups import UserGroup
from cmdb.user_management.user import User
from cmdb.user_management.user_authentication import *


class UserManagement:

    MANAGEMENT_CLASSES = {
        'RIGHT_CLASSES': UserRight,
        'GROUP_CLASSES': UserGroup,
        'USER_CLASSES': User
    }

    def __init__(self):
        from cmdb.data_storage import database_manager
        self.dbm = database_manager

    def _get_user(self, pre_filter, value):
        return self.dbm.find_one(collection=User.COLLECTION, filter={pre_filter: value})

    def get_next_public_id(self):
        latest_id = self.dbm.find_one(collection=User.COLLECTION, filter={}, sort=[('public_id', self.dbm.DESCENDING)])
        return int(latest_id['public_id'])+1

    def get_all_users(self):
        all_users = self.dbm.find_all(collection=User.COLLECTION)
        user_list = []
        for user in all_users:
            tmp_user = User(
                **user
            )
            user_list.append(tmp_user)
        return user_list

    def get_user_by_id(self, public_id):
        result = self._get_user('public_id', public_id)
        if not result:
            raise NoUserFoundExceptions(public_id)
        return User(**result)

    def get_user_by_username(self, user_name):
        result = self._get_user('user_name', user_name)
        if not result:
            raise NoUserFoundExceptions(user_name)
        return User(**result)

    def add_user(self, user):
        if not isinstance(user, User):
            raise WrongTypeException()
        try:
            new_user_id = self.dbm.insert(user.to_mongo(), user.COLLECTION)
        except Exception as es:
            raise es
        return new_user_id

    def change_user_pass(self, user, old_pass, new_pass):
        raise NotImplementedError

    def check_management_settings(self):
        for classes in UserManagement.MANAGEMENT_CLASSES.values():
            if self.dbm.is_empty_collection(classes.COLLECTION):
                classes.SETUP_CLASS().setup()

    def init_authentication_methods(self):
        from datetime import datetime
        from cmdb.user_management.user_authentication import LdapAuthenticationProvider
        ldap_con = LdapAuthenticationProvider()
        ldap_accounts = ldap_con.sync_ldap()
        all_users = self.get_all_users()
        user_names = [names.user_name for names in all_users]
        ldap_names = []
        for ldap_users in ldap_accounts:
            ldap_names.append(str(ldap_users.uid))
        user_not_in_db = list(set(ldap_names) - set(user_names))
        if len(user_not_in_db) > 0:
            for new_user in user_not_in_db:
                self.add_user(
                    User(
                        public_id=self.get_next_public_id(),
                        user_name=new_user,
                        authenticator='LdapAuthenticationProvider',
                        group='user',
                        registration_time=datetime.utcnow()
                    )
                )

    def user_has_right(self, user, right):
        founded_group = self.dbm.find_one(collection=UserGroup.COLLECTION, filter={'name': user.group})
        founded_right = self.dbm.find_one(collection=UserRight.COLLECTION, filter={'name': right})
        if founded_right['name'] in founded_group['rights']:
            return True
        else:
            raise UserHasNotRequiredRight(user, right)
