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


@pytest.fixture(scope='function')
def mongodb(pytestconfig):
    dbname = pytestconfig.getoption('mongodb_dbname') or pytestconfig.getini('mongodb_dbname')
    client = make_mongo_client(pytestconfig)
    db = client[dbname]
    clean_database(db)
    generate_collection(db)
    load_fixtures(db, pytestconfig)
    return db


def generate_collection(db):
    from cmdb.object_framework import __COLLECTIONS__
    for collection in __COLLECTIONS__:
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
