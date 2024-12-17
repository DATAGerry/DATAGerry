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
from flask.testing import FlaskClient

from cmdb.security.token.generator import TokenGenerator
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
class RestAPITestSuite:
    """TODO: document"""
    COLLECTION: str = NotImplemented
    ROUTE_URL: str = NotImplemented


class RestAPITestClient(FlaskClient):
    """TODO: document"""

    def __init__(self, *args, **kwargs):
        self.database_manager = kwargs.pop('database_manager')
        self._token_generator = TokenGenerator(self.database_manager)
        token = None

        if kwargs.get('default_auth_user', None):
            default_auth_user = kwargs.pop('default_auth_user')
            token = self._token_generator.generate_token(payload={'user': {
                'public_id': default_auth_user.public_id
            }}).decode('UTF-8')

        super().__init__(*args, **kwargs)

        if token:
            self.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'

        self.content_type = 'application/json'


    def inject_auth(self, kwargs: dict) -> dict:
        """TODO: document"""
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
        """TODO: document"""
        kw['method'] = 'GET'
        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'
        kw = self.inject_auth(kw)

        return super().open(*args, **kw)


    def patch(self, *args, **kw):
        """TODO: document"""
        kw['method'] = 'PATCH'

        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'

        kw = self.inject_auth(kw)

        return super().open(*args, **kw)


    def post(self, *args, **kw):
        """TODO: document"""
        kw['method'] = 'POST'

        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'

        kw = self.inject_auth(kw)

        return super().open(*args, **kw)


    def head(self, *args, **kw):
        """TODO: document"""
        kw['method'] = 'HEAD'

        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'

        kw = self.inject_auth(kw)

        return super().open(*args, **kw)


    def put(self, *args, **kw):
        """TODO: document"""
        kw['method'] = 'PUT'

        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'

        kw = self.inject_auth(kw)

        return super().open(*args, **kw)


    def delete(self, *args, **kw):
        """TODO: document"""
        kw['method'] = 'DELETE'

        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'

        kw = self.inject_auth(kw)

        return super().open(*args, **kw)


    def options(self, *args, **kw):
        """TODO: document"""
        kw['method'] = 'OPTIONS'

        if not kw.get('content_type', None):
            kw['content_type'] = 'application/json'

        kw = self.inject_auth(kw)
        return super().open(*args, **kw)
