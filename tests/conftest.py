
import pytest
from flask import Flask

pytest_plugins = 'tests/pytest_plugins/pytest_mongodb'


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config.testing = True
    app.debug = True
    register_route(app)

    return app.test_client()


def register_route(app):
    from cmdb.interface.rest_api.search_routes import search_routes
    app.register_blueprint(search_routes)
