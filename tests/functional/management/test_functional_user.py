
class TestManagementUser:
    ROUTE_URL = '/users'

    def test_user_get(self, rest_api):
        assert rest_api.get(f'{self.ROUTE_URL}/').status_code == 200
