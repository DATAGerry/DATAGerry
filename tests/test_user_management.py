"""
TODO: MAKE NEW
"""

import pytest
from cmdb.object_framework.cmdb_dao import RequiredInitKeyNotFoundError
from cmdb.user_management.user_base import UserManagementBase
from cmdb.user_management.user import User, InvalidEmailError
from cmdb.user_management.user_group import UserGroup
from datetime import datetime


def test_user_base():
    with pytest.raises(RequiredInitKeyNotFoundError):
        UserManagementBase()
    base_test = UserManagementBase(public_id=1)
    assert base_test.get_public_id() == 1


def test_user():
    with pytest.raises(RequiredInitKeyNotFoundError):
        User(group_id=1, registration_time=datetime.utcnow(), password=None,
             first_name='Test', last_name='User', email='test@example.org', public_id=1)

    t_user = User(user_name='test_user', group_id=1, registration_time=datetime.utcnow(), password=None,
                  email='test@example.org', public_id=1)

    assert t_user.get_public_id() == 1
    assert t_user.get_name() == 'test_user'
    with pytest.raises(InvalidEmailError):
        User(user_name='test_user', group_id=1, registration_time=datetime.utcnow(), password=None,
             first_name='Test', last_name='User', email='test', public_id=1)


def test_group():
    with pytest.raises(RequiredInitKeyNotFoundError):
        UserGroup(name='test_group')

    ug = UserGroup(name='test_group', public_id=1)
    assert ug.get_label() == 'Test_Group'

