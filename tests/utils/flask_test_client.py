from flask.testing import FlaskClient

from cmdb.security.token.generator import TokenGenerator


class RestAPITestSuite:
    COLLECTION: str = NotImplemented
    ROUTE_URL: str = NotImplemented


class RestAPITestClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        self.database_manager = kwargs.pop('database_manager')
        self._token_generator = TokenGenerator(self.database_manager)

        token = None
        if kwargs.get('default_auth_user', None):
            default_auth_user = kwargs.pop('default_auth_user')
            token = self._token_generator.generate_token(payload={'user': {
                'public_id': default_auth_user.public_id
            }}).decode('UTF-8')
        super(RestAPITestClient, self).__init__(*args, **kwargs)
        if token:
            self.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        self.content_type = 'application/json'

    def inject_auth(self, kwargs: dict) -> dict:
        if kwargs.get('unauthorized', None):
            kwargs['environ_overrides'] = {
                'HTTP_AUTHORIZATION': ''
            }
            kwargs.pop('unauthorized')
        elif kwargs.get('user', None):
            token = self._token_generator.generate_token(payload={'user': {
                'public_id': kwargs.pop('user').public_id
            }}).decode('UTF-8')
            kwargs['environ_overrides'] = {
                'HTTP_AUTHORIZATION': f'Bearer {token}'
            }
        return kwargs

    def get(self, *args, **kw):
        kw['method'] = 'GET'
        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'
        kw = self.inject_auth(kw)
        return super(RestAPITestClient, self).open(*args, **kw)

    def patch(self, *args, **kw):
        kw['method'] = 'PATCH'
        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'
        kw = self.inject_auth(kw)
        return super(RestAPITestClient, self).open(*args, **kw)

    def post(self, *args, **kw):
        kw['method'] = 'POST'
        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'
        kw = self.inject_auth(kw)
        return super(RestAPITestClient, self).open(*args, **kw)

    def head(self, *args, **kw):
        kw['method'] = 'HEAD'
        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'
        kw = self.inject_auth(kw)
        return super(RestAPITestClient, self).open(*args, **kw)

    def put(self, *args, **kw):
        kw['method'] = 'PUT'
        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'
        kw = self.inject_auth(kw)
        return super(RestAPITestClient, self).open(*args, **kw)

    def delete(self, *args, **kw):
        kw['method'] = 'DELETE'
        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'
        kw = self.inject_auth(kw)
        return super(RestAPITestClient, self).open(*args, **kw)

    def options(self, *args, **kw):
        kw['method'] = 'OPTIONS'
        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'
        kw = self.inject_auth(kw)
        return super(RestAPITestClient, self).open(*args, **kw)
