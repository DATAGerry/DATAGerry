import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--mongodb-host', action='store', default='localhost', help='Host of mongodb test instance'
    )
    parser.addoption(
        '--mongodb-port', action='store', default=27017, help='Port of mongodb test instance'
    )
    parser.addoption(
        '--mongodb-database', action='store', default='data-quality', help='Database of mongodb test instance'
    )
