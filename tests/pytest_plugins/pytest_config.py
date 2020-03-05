def pytest_addoption(parser):
    parser.addini(
        name='config-path',
        help='path to test config file',
        default='../../etc/cmdb_test.conf')
    parser.addoption(
        '--config-path',
        help='path to test config file')
