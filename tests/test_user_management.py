from cmdb.user_management import User
from cmdb.user_management.user_authentication import LocalAuthenticationProvider


def test_user_init():
    from datetime import date
    test_user = User(
        public_id=1,
        user_name='TestUser',
        password='f59d50183b60ce883b3c35ed9254dd178a8b02e6cb1f426b539eacb2a1ddb34d',
        group=None,
        registration_time=date.today()
    )
    assert test_user.get_authenticator() == LocalAuthenticationProvider
