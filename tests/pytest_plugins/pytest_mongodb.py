# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
@copyright https://github.com/mdomke/pytest-mongodb
"""
import functools
import json
import os
import codecs

from bson import json_util
import mongomock
import pytest
import pymongo
import yaml

_cache = {}


def pytest_addoption(parser):
    parser.addini(
        name='mongodb_fixtures',
        help='Load these fixtures for tests',
        type='linelist')

    parser.addini(
        name='mongodb_fixture_dir',
        help='Try loading fixtures from this directory',
        default=os.getcwd())

    parser.addini(
        name='mongodb_engine',
        help='The database engine to use [mongomock]',
        default='mongomock')

    parser.addini(
        name='mongodb_host',
        help='The host where the mongodb-server runs',
        default='localhost')

    parser.addini(
        name='mongodb_dbname',
        help='The name of the database where fixtures are created [pytest]',
        default='pytest')

    parser.addini(
        name='db_config',
        help='optional path to config file',
        default='./etc/cmdb_test.conf')

    parser.addini(
        name='port',
        help='Port for the connection to the application',
        default=27017)

    parser.addini(
        name='timeout',
        help='The amount of time that an operation can take before it is aborted with an error',
        default=1000)

    parser.addoption(
        '--mongodb-fixture-dir',
        help='Try loading fixtures from this directory')

    parser.addoption(
        '--mongodb-engine',
        help='The database engine to use [mongomock]')

    parser.addoption(
        '--mongodb-host',
        help='The host where the mongodb-server runs')

    parser.addoption(
        '--mongodb-dbname',
        help='The name of the database where fixtures are created [pytest]')

    parser.addoption(
        '--db_config',
        help="Optional path to config file")

    parser.addoption(
        '--port',
        help="Port for the connection to the application ")

    parser.addoption(
        '--timeout',
        help='The amount of time that an operation can take before it is aborted with an error')


@pytest.fixture(scope='session')
def mongodb(pytestconfig):
    db_name = pytestconfig.getoption('mongodb_dbname') or pytestconfig.getini('mongodb_dbname')
    client = make_mongo_client(pytestconfig)
    db = client[db_name]
    clean_database(db)
    generate_collection(db)
    load_fixtures(db, pytestconfig)
    return db


def generate_collection(db):

    from cmdb.framework import __COLLECTIONS__ as __FRAMEWORK_COLLECTIONS
    from cmdb.user_management import __COLLECTIONS__ as __USER_COLLECTIONS
    collections = __FRAMEWORK_COLLECTIONS + __USER_COLLECTIONS
    for collection in collections:
        db.create_collection(collection.COLLECTION)
        db.get_collection(collection.COLLECTION).create_indexes(collection.get_index_keys())


def make_mongo_client(config):
    engine = config.getoption('mongodb_engine') or config.getini('mongodb_engine')
    host = config.getoption('mongodb_host') or config.getini('mongodb_host')
    if engine == 'pymongo':
        client = pymongo.MongoClient(host)
    else:
        client = mongomock.MongoClient(host)
    return client


def clean_database(db):
    for name in db.list_collection_names():
        db.drop_collection(name)


def load_fixtures(db, config):
    basedir = config.getoption('mongodb_fixture_dir') or config.getini('mongodb_fixture_dir')
    fixtures = config.getini('mongodb_fixtures')

    for file_name in os.listdir(basedir):
        collection, ext = os.path.splitext(os.path.basename(file_name))
        file_format = ext.strip('.')
        supported = file_format in ('json', 'yaml')
        selected = collection in fixtures if fixtures else True
        if selected and supported:
            path = os.path.join(basedir, file_name)
            load_fixture(db, collection, path, file_format)


def load_fixture(db, collection, path, file_format):
    if file_format == 'json':
        loader = functools.partial(json.load, object_hook=json_util.object_hook)
    elif file_format == 'yaml':
        loader = yaml.load
    else:
        return
    try:
        docs = _cache[path]
    except KeyError:
        with codecs.open(path, encoding='utf-8') as fp:
            _cache[path] = docs = loader(fp)

    for document in docs:
        db[collection].insert_one(document)


def mongo_engine():
    return pytest.config.getoption('mongodb_engine') or pytest.config.getini('mongodb_engine')


@pytest.fixture(scope='class')
def init_config_reader(pytestconfig):
    from cmdb.utils.system_reader import SystemConfigReader
    system_config_reader = SystemConfigReader()

    host = pytestconfig.getoption('mongodb_host') or pytestconfig.getini('mongodb_host')
    port = pytestconfig.getoption('port') or pytestconfig.getini('port')
    database_name = pytestconfig.getoption('mongodb_dbname') or pytestconfig.getini('mongodb_dbname')
    timeout = pytestconfig.getoption('timeout') or pytestconfig.getini('timeout')

    # Create a new section for database configuration if not available
    if 'Database' in system_config_reader.get_sections():
        pass
    else:
        system_config_reader.add_section('Database')
        system_config_reader.set('Database', 'host', host)
        system_config_reader.set('Database', 'port', port)
        system_config_reader.set('Database', 'database_name', database_name)
        system_config_reader.set('Database', 'connection_timeout', timeout)
