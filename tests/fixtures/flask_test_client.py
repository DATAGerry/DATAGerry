from flask.testing import FlaskClient


class RestAPITestClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        auth = kwargs.pop("auth")
        super(RestAPITestClient, self).__init__(*args, **kwargs)
        self.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {auth}'
