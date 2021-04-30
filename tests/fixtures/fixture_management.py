from datetime import datetime

import pytest

from cmdb.user_management import UserGroupModel, RightManager, UserModel


@pytest.fixture(scope="session")
def right_manager():
    from cmdb.user_management import rights
    return RightManager(rights)


@pytest.fixture(scope="session")
def full_access_group(right_manager: RightManager):
    return UserGroupModel(public_id=1, name='full', label='Full', rights=[right_manager.get('base.*')])


@pytest.fixture(scope="session")
def none_access_group():
    return UserGroupModel(public_id=2, name='none', label='None')


@pytest.fixture(scope="session")
def full_access_user(full_access_group: UserGroupModel):
    registration_time = datetime.now()
    return UserModel(public_id=1, user_name='full-access-user',
                     active=True, group_id=full_access_group.public_id,
                     registration_time=registration_time)


@pytest.fixture(scope="session")
def none_access_user(none_access_group: UserGroupModel):
    registration_time = datetime.now()
    return UserModel(public_id=2, user_name='none-access-user',
                     active=True, group_id=none_access_group.public_id,
                     registration_time=registration_time)
