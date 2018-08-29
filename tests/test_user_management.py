import pytest
from cmdb.user_management import User, UserManagement, UserGroup
from cmdb.user_management.user_authentication import LocalAuthenticationProvider


@pytest.fixture
def database_manager():
    import os
    from cmdb.data_storage.database_connection import MongoConnector
    from cmdb.data_storage.database_manager import DatabaseManagerMongo
    dbm = DatabaseManagerMongo(
        connector=MongoConnector(
            host=os.environ["TEST_HOST"],
            port=int(os.environ["TEST_PORT"]),
            database_name=os.environ['TEST_DATABASE'],
            timeout=100
        )
    )
    yield dbm
    dbm.delete_collection(UserGroup.COLLECTION)
    dbm.delete_collection(User.COLLECTION)


@pytest.fixture
def user_manager(database_manager) -> UserManagement:
    return UserManagement(
        database_manager=database_manager
    )


def test_manager_group(user_manager):
    from cmdb.user_management.user_manager import GroupDeleteError

    # INSERT
    group_id = user_manager.insert_group('testgroup', 'Testgroup')
    assert group_id == 1

    # GET
    get_group = user_manager.get_group(1)
    assert isinstance(get_group, UserGroup)
    assert get_group.get_public_id() == 1

    # DELETE
    delete_ack = user_manager.delete_group(1)
    assert delete_ack.deleted_count == 1
    with pytest.raises(GroupDeleteError):
        user_manager.delete_group(1)


def test_manager_user(user_manager):
    from cmdb.user_management.user_manager import UserDeleteError
    group_id = user_manager.insert_group('testgroup', 'Testgroup')

    # INSERT
    user_id  = user_manager.insert_user(
        user_name='test_user',
        group_id=group_id,
        password=None,
        first_name='Test',
        last_name='User',
        authenticator="LocalAuthenticationProvider"
    )

    # GET
    get_user = user_manager.get_user(public_id=user_id)
    assert isinstance(get_user, User)
    assert get_user.get_username() == 'test_user'

    # DELETE
    delete_ack = user_manager.delete_user(1)
    assert delete_ack.deleted_count == 1
    with pytest.raises(UserDeleteError):
        user_manager.delete_user(1)

    user_manager.delete_group(1)
